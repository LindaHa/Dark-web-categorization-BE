from typing import List, Any
from api.models import Group
from api.utils.caching_helpers import get_cached_group_subgroups, cache_groups_subgroups, get_cached_all_groups, \
    get_cached_all_groups_by_category
from api.utils.graph_helpers.graph_helpers import get_linked_groups
from api.utils.graph_helpers.group_by_helpers import GroupByMode, divide_pages_by_category


def get_zero_lvl_groups(el_repository: Any, group_by_mode: str) -> List[Group]:
    """
    :param el_repository: the repository for fetching all pages
    :type el_repository: Any
    :param group_by_mode: the mode according to which the pages are divided into groups
    :type group_by_mode: str
    :return: groups with pages which were divided according to he group by mode
    :rtype: List[Group]
    """
    subgroups = []
    if group_by_mode == GroupByMode.LINKS:
        zero_lvl_groups = get_cached_all_groups()
        if zero_lvl_groups:
            subgroups = zero_lvl_groups
        else:
            pages = el_repository.fetch_all()
            subgroups = get_linked_groups(pages)

    elif group_by_mode == GroupByMode.CATEGORY:
        zero_lvl_groups = get_cached_all_groups_by_category()
        if zero_lvl_groups:
            subgroups = zero_lvl_groups
        else:
            pages = el_repository.fetch_all()
            subgroups = divide_pages_by_category(pages)

    return subgroups


def get_subgroups_of_group(parent_group_id: str, el_repository: Any, group_by_mode: str) -> List[Group]:
    """
    :param el_repository: the repository for fetching all pages
    :type el_repository: Any
    :param parent_group_id: group id
    :type parent_group_id: str
    :param group_by_mode: the mode according to which the pages are divided into groups
    :type group_by_mode: str
    :return: a list of sub-groups of the group with the given id
    :rtype: List[Group]
    """
    ids = parent_group_id.split(".")
    unused_ids = []
    subgroups = []

    while ids and not subgroups:
        subgroup_id = '.'.join(ids)
        subgroups = get_cached_group_subgroups(subgroup_id)
        if not subgroups:
            last_id = ids.pop()
            unused_ids.append(last_id)

    if not subgroups:
        subgroups = get_zero_lvl_groups(el_repository, group_by_mode)

    while unused_ids:
        unused_id = str(unused_ids.pop())
        ids.append(unused_id)
        next_id = ".".join(ids)

        next_group = [group for group in subgroups if group.id == next_id][0]
        # TODO check if next_group is not null
        pages = next_group.members
        subgroups = get_linked_groups(pages, next_id)

        cache_groups_subgroups(next_id, subgroups)

    return subgroups
