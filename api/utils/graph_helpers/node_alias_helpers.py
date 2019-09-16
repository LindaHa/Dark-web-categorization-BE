from collections import defaultdict
from typing import Dict, Tuple, List

from api.models import Page


def create_hash_tables(pages: Dict[str, Page]) -> Tuple[Dict[str, int], Dict[int, str]]:
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
    original_node_key_group_pairs = {}
    for node_alias in partition:
        associated_component_key = partition[node_alias]
        original_node_key = table_to_original[node_alias]
        original_node_key_group_pairs[original_node_key] = associated_component_key

    return original_node_key_group_pairs