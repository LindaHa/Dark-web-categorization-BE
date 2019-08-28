from pip._vendor import requests

from api.utils.caching_helpers import get_cached_all_pages, cache_all_pages
from api.utils.parsers import get_pages_from_json, get_scroll_id, get_hits
from api.models import Page
from typing import Dict, Union


CHUNK_SIZE = 500


class ElasticSearchRepository(object):
    def __init__(self, **kwargs):
        self.server = "http://147.251.124.23:9200/"
        self.end_point_url = self.server + "tor,i2p/"

    def basic_search(self, search_column, search_phrase) -> Union[Dict[str, Page], None]:
        payload = {
            "query": {
                # "multi_match": {
                #     "query": search_phrase,
                #     "fields": search_column
                # },
                "bool": {
                    "must": [
                        {
                            "match": {search_column: search_phrase}
                        }
                    ]
                }
            }
        }
        response = requests.post(self.end_point_url + "_search", json=payload)
        if response.status_code == 200:
            json = response.json()
            pages = get_pages_from_json(json)
            return pages
        else:
            return None

    def fetch_chunk(self, scroll_id) -> Union[str, None]:
        payload = {
            "scroll": "1m",
            "scroll_id": scroll_id
        }
        response = requests.post(self.server + "_search/scroll", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_all(self) -> Dict[str, Page]:
        all_pages_cached = get_cached_all_pages()
        if all_pages_cached:
            return all_pages_cached

        payload = {
            "size": CHUNK_SIZE,
            "query": {
                "match_all": {}
            }
        }

        response = requests.post(self.end_point_url + "_search?scroll=1m", json=payload)
        final_pages = {}
        if response.status_code == 200:
            json = response.json()
            scroll_id = get_scroll_id(json)
            final_pages = get_pages_from_json(json)
            hits = get_hits(json)
            i = 0

            while hits:
                chunk_json = self.fetch_chunk(scroll_id)

                scroll_id = get_scroll_id(chunk_json)
                hits = get_hits(chunk_json)
                pages = get_pages_from_json(chunk_json)

                if pages:
                    final_pages.update(pages)

                print(i)
                i += 1

        for fp in final_pages:
            final_pages[fp].content = ''

        # final_pages = guarantee_pages_for_links(final_pages)
        final_pages = removeLinksToNonScrapedPages(final_pages)

        total = 0
        total_starts_with = 0
        for fpage in final_pages:
            total += 1
            if final_pages[fpage].url.startswith('http://2op42f4qv2reca5b.onion'):
                total_starts_with += 1
        print("There is {} pages total, from which {} start with 'http://2op42f4qv2reca5b.onion'"
              .format(total, total_starts_with))

        cache_all_pages(final_pages)

        return final_pages


def guarantee_pages_for_links(pages: Dict[str, Page]) -> Dict[str, Page]:
    """
    :param pages: Original pages from the database with possible links to non-existent pages
    :type pages: Dict[Page]
    :return: Pages with links to guaranteed pages
    :rtype: Dict[Page]
    """
    guaranteed_pages = dict(pages)
    for page_url, page in pages.items():
        links = page.links
        for link in links:
            link_url = link.link
            link_page = guaranteed_pages.get(link_url)
            if not link_page:
                link_page = Page(id=link_url, url=link_url)
                guaranteed_pages[link_url] = link_page

    return guaranteed_pages


def removeLinksToNonScrapedPages(pages: Dict[str, Page]) -> Dict[str, Page]:
    """
    :param pages: Original pages from the database with possible links to non-existent pages
    :type pages: Dict[Page]
    :return: Pages with links that point only to existing pages
    :rtype: Dict[Page]
    """
    total_valid_links = 0
    total_links = 0
    for page_url in pages:
        page = pages[page_url]
        total_links += len(page.links)
        page.links = [link for link in page.links if link.link in pages]
        if len(page.links) != 0:
            links_count = len(page.links)
            total_valid_links += links_count
            print("found {} valid links".format(links_count))

    print("There was total of {} links from which {} were valid".format(total_links, total_valid_links))
    return pages
