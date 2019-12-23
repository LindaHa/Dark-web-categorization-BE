from pip._vendor import requests

from api.utils.caching_helpers import get_cached_all_pages, cache_all_pages, cache_json_pages, \
    get_cached_json_pages, cache_specific_content
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
            cache_json_pages((str(response.text)))
            return response.json()
        else:
            return None

    def fetch_all(self) -> Dict[str, Page]:
        all_pages_cached = get_cached_all_pages()
        if all_pages_cached:
            return all_pages_cached

        final_pages = {}
        payload = {
            "size": CHUNK_SIZE,
            "query": {
                "match_all": {}
            }
        }

        response = requests.post(self.end_point_url + "_search?scroll=1m", json=payload)
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

        for url, page in final_pages.items():
            cache_specific_content(url, page.content)
            page.content = ''

        # final_pages = guarantee_pages_for_links(final_pages)
        final_pages = remove_links_to_non_scraped_pages(final_pages)

        total = 0
        total_starts_with = 0
        for f_page in final_pages:
            total += 1
            if final_pages[f_page].url.startswith('http://2op42f4qv2reca5b.onion'):
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


def remove_links_to_non_scraped_pages(pages: Dict[str, Page]) -> Dict[str, Page]:
    """
    :param pages: Original pages from the database with possible links to non-existent pages
    :type pages: Dict[Page]
    :return: Pages with links that point only to existing pages
    :rtype: Dict[Page]
    """
    total_valid_links = 0
    total_links = 0

    domains = {}
    link_domains = {}
    all_links = {}
    not_scraped_links = {}
    for page_key in pages:
        domain = page_key.split(".onion")[0]
        page = pages[page_key]
        for link_key in page.links:
            link_key = link_key.link
            link_domain = link_key.split(".onion")[0]
            if link_key not in all_links:
                all_links[link_key] = link_key
            if link_domain not in link_domains:
                link_domains[link_domain] = link_domain
            if link_key not in pages and link_key not in not_scraped_links:
                not_scraped_links[link_key] = link_key
        if domain not in domains:
            domains[domain] = domains

    for page_url in pages:
        page = pages[page_url]
        total_links += len(page.links)
        page.links = [link for link in page.links if link.link in pages]
        if len(page.links) != 0:
            links_count = len(page.links)
            total_valid_links += links_count
            print("found {} valid links".format(links_count))

    print("There was total of {} links from which {} were valid".format(total_links, total_valid_links))
    print("There are {} unique domains.".format(len(domains)))
    print("There are {} unique link domains.".format(len(link_domains)))
    print("There are {} unique links.".format(len(all_links)))
    print("There are {} unique links which were not scraped.".format(len(not_scraped_links)))
    return pages
