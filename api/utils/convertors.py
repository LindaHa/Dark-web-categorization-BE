from typing import List
from api.models import Group, MetaGroup, NUMBER_OF_FIRST_MEMBERS


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

        first_k_members = []
        count = 0
        for value in group.members:
            if count >= NUMBER_OF_FIRST_MEMBERS:
                break
            else:
                count += 1
                first_k_members.append(group.members[value])

        meta_group = MetaGroup(
            id=group.id,
            links=simple_group_links,
            first_members=first_k_members,
            members_count=len(group.members),
            categories=group.categories,
        )
        meta_groups.append(meta_group)

    return meta_groups
