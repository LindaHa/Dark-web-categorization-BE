from typing import List
from api.models import Group, MetaGroup


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
        for link in group.links:
            simple_group_links.append(link.link)
        meta_group = MetaGroup(id=group.id, links=simple_group_links, members_count=len(group.members))
        meta_groups.append(meta_group)

    return meta_groups
