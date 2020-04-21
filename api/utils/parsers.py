from api.classification.categorizer import Categorizer
from api.models import Page, Link, Category
from typing import Dict, List


def get_hits(json) -> str:
    return json.get("hits").get("hits")


def get_scroll_id(json) -> str:
    return json.get("_scroll_id")


def get_total_in_db(json) -> str:
    return json.get("hits").get("total")


def taken_from_db(json) -> str:
    return json.get("shards").get("total")


def get_pages_from_json(json) -> Dict[str, Page]:
    categorizer = Categorizer()
    pages_to_return = {}
    response_pages = get_hits(json)
    for page in response_pages:
        page_info = page.get("_source")
        url = page_info.get("raw_url")
        if is_url_valid(url):
            page_id = page.get("_id")
            title = page_info.get("title")
            response_links = page_info.get("links")
            last_updated = page_info.get("updated_on")
            links = get_links_from_json(response_links)
            content = page_info.get("content")
            category_name = categorizer.categorize(bytes(content, 'utf-8').decode('utf-8', 'ignore'))
            category = Category(
                    name=category_name,
                    occurrence=1,
            )
            pages_to_return[url] = Page(
                id=page_id,
                url=url,
                title=title,
                last_updated=last_updated,
                links=links,
                content=content,
                categories=[category]
            )
        else:
            print("cannot find url for source: {}".format(page_info))
    return pages_to_return


def get_links_from_json(json_links) -> List[Link]:
    links = {}
    if json_links:
        for json_link in json_links:
            link_url = json_link.get("link")
            if is_url_valid(link_url) and not link_url.startswith("/") and link_url not in links:
                link = Link(link=link_url, name=json_link.get("link_name"), occurrences=1)
                links[link_url] = link

    return [link for url, link in links.items()]


def is_url_valid(url: str) -> bool:
    """
    :param url: the url of a page
    :type url: str
    :return: returns true if the url is valid, false otherwise
    :rtype: bool
    """
    return not not url and not not url.strip() and ('.i2p' in url or '.onion' in url)
