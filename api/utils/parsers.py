from api.models import Page


def get_pages_from_json(json):
    pages_to_return = []
    response_pages = json.get("hits").get("hits")
    for page in response_pages:
        page_info = page.get("_source")
        url = page_info.get("url")
        if url is not None:
            page_id = page.get("_id")
            title = page_info.get("title")
            response_links = page_info.get("links")
            links = get_links_from_json(response_links)
            content = page_info.get("content")
            pages_to_return.append(Page(id=page_id, url=url, title=title, links=links, content=content))

    return pages_to_return


def get_links_from_json(json):
    links_to_return = []
    if json:
        for link in json:
            if link.get('link') and 'onion' in link.get('link'):
                links_to_return.append(link)

    return links_to_return
