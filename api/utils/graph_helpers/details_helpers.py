from typing import List
from api.models import Group, PageDetails, Page, DetailsOptions


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
    for url, member in group.members.items():
        page_detail = PageDetails(url=url)
        if options.category:
            page_detail.category = member.categories[0].name
        if options.title:
            page_detail.title = member.title
        if options.content:
            page_detail.content = member.content
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
