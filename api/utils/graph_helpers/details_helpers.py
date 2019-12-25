from typing import List, Dict
from api.models import Group, PageDetails, Page, DetailsOptions
from api.utils.graph_helpers.shelving_helpers import get_shelved_pages


def get_group_details(group: Group, options: DetailsOptions) -> List[PageDetails]:
    """
    :param options: information of which details are to be returned
    :type options: DetailsOptions
    :param group: the group whose members' urls are desired
    :type group: Group
    :return: a list of details described in options of all members of the given group
    :rtype: List[PageDetails]
    """
    details = []
    shelved_pages = {}
    if options.content:
        shelved_pages = get_shelved_pages()

    for url, member in group.members.items():
        page_detail = PageDetails(url=url)
        if options.category:
            page_detail.category = member.categories[0].name
        if options.title:
            page_detail.title = member.title
        if options.content:
            page_detail.content = get_content(full_pages=shelved_pages, url=member.url)
        if options.last_updated:
            page_detail.last_updated = member.last_updated
        if options.links:
            page_detail.links = member.links
        details.append(page_detail)

    return details


def get_page_details(page: Page) -> PageDetails:
    """
    :param page: the page which details are desired
    :type page: Page
    :return: returns the details of the given page
    :rtype: PageDetails
    """
    links = [link.link for link in page.links]

    page_details = PageDetails(
        links=links if links else []
    )

    return page_details


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
