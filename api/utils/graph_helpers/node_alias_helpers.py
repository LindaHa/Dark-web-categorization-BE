from collections import defaultdict
from typing import Dict, Tuple, List

from api.models import Page


def create_hash_tables(pages: Dict[str, Page]) -> Tuple[Dict[str, int], Dict[int, str]]:
    """
    :param pages: the original pages
    :type pages: Dict[str, Page]
    :return: a table with the url of the page and the alias to go with the url, and a table with the alias of the pages and the url represented by the alias
    :rtype: Tuple[Dict[str, int], Dict[int, str]]
    """
    index = 0
    table_to_alias = dict()
    table_to_original = dict()
    for page_row in pages:
        page = pages.get(page_row)
        page_url = page.url
        if page_url not in table_to_alias:
            table_to_alias[page_url] = index
            table_to_original[index] = page_url
            index += 1
        # for link in page.links:
        #     link_url = link.get("link")
        #     if link_url not in table_to_alias:
        #         table_to_alias[link_url] = index
        #         table_to_original[index] = link_url
        #         index += 1
    return table_to_alias, table_to_original


def get_node_aliases(
        pages: Dict[str, Page],
        table_to_alias: Dict[str, int]
) -> Dict[int, List[int]]:
    """
    :param pages: the original pages
    :type pages: Dict[str, Page]
    :param table_to_alias: a table with the page url and the alias to go with the url
    :type table_to_alias: Dict[str, int]
    :return: a table with the alias of the page and a list with urls the page links to
    :rtype: Dict[int, List[int]]
    """
    pairs = defaultdict(list)
    for page_row in pages:
        page = pages.get(page_row)
        page_index = table_to_alias[page.url]
        if page_index is None:
            continue

        links = page.links
        if not links:
            pairs[page_index] = []
        elif links:
            for link in links:
                link_original = link.link
                link_index = table_to_alias.get(link_original)
                if link_index is None and not pairs[page_index]:
                    pairs[page_index] = []
                elif link_index is not None:
                    pairs[page_index].append(link_index)
    return pairs


def get_original_node_key_group_pairs(
        partition: Dict[int, int],
        table_to_original: Dict[int, str]
) -> Dict[str, int]:
    """
    :param partition: a hash table with the page alias and the community the page was assigned to
    :type partition: Dict[int, int]
    :param table_to_original: a table with the alias of a page and the url corresponding to the alias
    :type table_to_original: Dict[int, str]
    :return: a hash table with the page url and the community the page was assigned to
    :rtype: Dict[str, int]
    """
    original_node_key_group_pairs = {}
    for node_alias in partition:
        associated_component_key = partition[node_alias]
        original_node_key = table_to_original[node_alias]
        original_node_key_group_pairs[original_node_key] = associated_component_key

    return original_node_key_group_pairs