from typing import List, Dict
from api.models import Group, PageDetails, Page, DetailsOptions
from api.utils.graph_helpers.shelving_helpers import get_shelved_pages


def get_group_details(group: Group, options: DetailsOptions) -> List[PageDetails]:
    """
    :param options: information of which details are to be returned
    :type options: DetailsOptions
    :param group: the group whose members' details are desired
    :type group: Group
    :return: a list of details described in options of all members of the given group
    :rtype: List[PageDetails]
    """
    details = get_pages_details(pages=group.members, options=options)
    return details


def get_pages_details(pages: Dict[str, Page], options: DetailsOptions, are_whole: bool = False) -> List[PageDetails]:
    """
    :param are_whole: a flag whether the received pages are whole (with content) or not
    :type are_whole: bool
    :param options: information of which details are to be returned
    :type options: DetailsOptions
    :param pages: pages whose details are desired
    :type pages: Dict[str, Page]
    :return: a list of details described in options of all members of the given group
    :rtype: List[PageDetails]
    """
    details = []
    shelved_pages = {}
    if options.content and not are_whole:
        shelved_pages = get_shelved_pages()

    for url, page in pages.items():
        page_detail = get_page_details(page=page, options=options, shelved_pages=shelved_pages)
        details.append(page_detail)

    return details


def get_page_details(page: Page, options: DetailsOptions, shelved_pages: Dict[str, Page]) -> PageDetails:
    """
    :param shelved_pages: whole pages (with content)
    :type shelved_pages: Dict[str, Page]
    :param options: information of which details are to be returned
    :type options: DetailsOptions
    :param page: the page which details are desired
    :type page: Page
    :return: returns the details of the given page
    :rtype: PageDetails
    """
    page_detail = PageDetails(url=page.url)
    if options.category:
        page_detail.category = page.categories[0].name
    if options.title:
        page_detail.title = page.title
    if options.content:
        if shelved_pages:
            page_detail.content = get_content(full_pages=shelved_pages, url=page.url)
        else:
            page_detail.content = page.content
    if options.last_updated:
        page_detail.last_updated = page.last_updated
    if options.links:
        page_detail.links = page.links

    return page_detail


def get_content(full_pages: Dict[str, Page], url: str) -> str:
    """
    :param full_pages: whole pages with content
    :type full_pages: Dict[str, Page]
    :param url: the url of the page with the desired content
    :type url: str
    :return: the desired content if it exists
    :rtype: str
    """
    if url in full_pages:
        page = full_pages[url]
        return page.content

    return ''
