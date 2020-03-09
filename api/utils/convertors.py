from typing import List, Dict
from api.models import Group, MetaGroup, NUMBER_OF_FIRST_MEMBERS, Page
from api.utils.graph_helpers.url_helpers import get_domain_from_url


def convert_groups_to_meta_groups(groups: List[Group]) -> List[MetaGroup]:
    """
    :param groups: groups to be converted
    :type groups: List[Group]
    :return: meta groups made from groups
    :rtype: List[MetaGroup]
    """
    meta_groups = []

    for group in groups:
        simple_group_links = []
        if group.links:
            simple_group_links = group.links

        first_k_members = get_first_members(group.members)
        domains_count = get_number_of_domains(group.members)

        meta_group = MetaGroup(
            id=group.id,
            links=simple_group_links,
            first_members=first_k_members,
            members_count=len(group.members),
            domains_count=domains_count,
            categories=group.categories,
        )
        meta_groups.append(meta_group)

    return meta_groups


def get_first_members(members: Dict[str, Page]) -> List[Page]:
    """
    :param members: all members of a community
    :type members: Dict[str, Page]
    :return: a list of NUMBER_OF_FIRST_MEMBERS members
    :rtype: List[Page]
    """
    count = 0
    first_k_members = []
    for member_id in members:
        if count >= NUMBER_OF_FIRST_MEMBERS:
            break
        else:
            count += 1
            first_k_members.append(members[member_id])

    return first_k_members


def get_number_of_domains(members: Dict[str, Page]) -> int:
    """
    :param members: all members of a community
    :type members: Dict[str, Page]
    :return: the number of domains in the community
    :rtype: int
    """
    domains = {}
    for key in members:
        domain = get_domain_from_url(key)
        if domain not in domains:
            domains[domain] = domain

    return len(domains)

