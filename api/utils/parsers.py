from api.models import Page, Link
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
    pages_to_return = {}
    response_pages = get_hits(json)
    for page in response_pages:
        page_info = page.get("_source")
        url = page_info.get("url")
        if url is not None:
            page_id = page.get("_id")
            title = page_info.get("title")
            response_links = page_info.get("links")
            links = get_links_from_json(response_links)
            content = page_info.get("content")
            pages_to_return[url] = Page(id=page_id, url=url, title=title, links=links, content=content)
        else:
            print("cannot find url for source: {}".format(page_info))
    return pages_to_return


def get_links_from_json(json_links) -> List[Link]:
    links = []
    if json_links:
        for json_link in json_links:
            link_url = json_link.get("link")
            if link_url and not link_url.startswith("/"):
                link = Link(link=link_url, name=json_link.get("link_name"))
                links.append(link)
    return links
