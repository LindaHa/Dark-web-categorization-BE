from api.models import Page, Link


def get_hits(json):
    return json.get("hits").get("hits")


def get_scroll_id(json):
    return json.get("_scroll_id")


def get_total_in_db(json):
    return json.get("hits").get("total")


def taken_from_db(json):
    return json.get("shards").get("total")


def get_pages_from_json(json):
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
            pages_to_return[url] = (Page(id=page_id, url=url, title=title, links=links, content=content))
    return pages_to_return


def get_links_from_json(json_links):
    links = []
    if json_links:
        for json_link in json_links:
            link_url = json_link.get("link")
            if link_url and "onion" in link_url:
                link = Link(link=link_url, name=json_link.get("link_name"))
                links.append(link)
    return links
