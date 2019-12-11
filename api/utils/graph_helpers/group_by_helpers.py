from typing import Dict, List
from enum import Enum
from api.categorization.labels import labels_index
from api.models import Page, Group, Link
from api.utils.graph_helpers.graph_helpers import get_linked_groups_from_ids


class GroupByMode(Enum):
    CATEGORY = 'category'
    LINK = 'link'


def get_partition_by_category(pages: Dict[str, Page]) -> Dict[str, int]:
    """
    :param pages: The original pages from db
    :type pages: Dict[str, Page]
    :return: Page url to category index pairs
    :rtype: Dict[str, int]
    """
    partition = {}
    reversed_labels_index: Dict[str, int] = {label: key for key, label in labels_index.items()}

    for url, page in pages.items():
        p_category = page.categories[0].name
        partition[url] = reversed_labels_index[p_category]

    return partition


def name_by_category(groups: List[Group]) -> List[Group]:
    """
    :param groups: pages divided into groups according to their category
    :type groups: List[Group]
    :return: the original groups but with the groups named according to the category they are representing
    :rtype: List[Group]
    """
    renamed_groups = groups.copy()
    for group in renamed_groups:
        groups_cat = group.categories[0].name
        group.id = groups_cat

    return renamed_groups


def divide_pages_by_category(pages: Dict[str, Page]) -> List[Group]:
    """
    :param pages: The original pages from db
    :type pages: Dict[str, Page]
    :return: A list of groups with links to original page keys
    :rtype:
    """
    partition = get_partition_by_category(pages)
    groups = get_linked_groups_from_ids(pages, partition)
    converted_linked_groups = convert_link_aliases_to_keys(groups, partition)
    renamed_groups = name_by_category(converted_linked_groups)

    return renamed_groups


def convert_link_aliases_to_keys(groups: List[Group]) -> List[Group]:
    for group in groups:
        converted_links = set()
        for link in group.links:
            reversed_link = labels_index[int(link.link)]
            converted_link = Link(link=reversed_link)
            converted_links.add(converted_link)
        group.links = list(converted_links)

    return groups
