from api.models import Page


def get_pages_from_json(json):
    pages_to_return = []
    response_pages = json.get("hits").get("hits")
    for page in response_pages:
        id = page.get("_id")
        page_info = page.get("_source")
        url = page_info.get("url")
        title = page_info.get("title")
        response_links = page_info.get("links")
        links = response_links
        content = page_info.get("content")
        pages_to_return.append(Page(id=id, url=url, title=title, links=links, content=content))

    return pages_to_return

#
# def get_links_from_json(json):
#     links_to_return = []
#     for link in json:
#         if link.get('link') and 'onion' in link.get('link'):
#             links_to_return.append(link)
#
#     return links_to_return
