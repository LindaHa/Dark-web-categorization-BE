from typing import List
from api.models import Group, GroupDetails, PageDetails, Page


def get_member_urls_for_group(group: Group) -> List[str]:
    """
    :param group: the group whose members' urls are desired
    :type group: Group
    :return: a list of urls of all members of the given group
    :rtype: List[str]
    """
    urls = [url for url in group.members]

    return urls


def get_group_details(group: Group) -> GroupDetails:
    """
    :param group: the group whose members' urls are desired
    :type group: Group
    :return: returns the group details of the given group
    :rtype: GroupDetails
    """
    urls = get_member_urls_for_group(group)
    group_details = GroupDetails(
        members_urls=urls
    )

    return group_details


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
