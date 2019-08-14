from collections import defaultdict
from api.models import Group, Link, MetaGroup, Page
from typing import Dict, List, Tuple, Any
import cylouvain
import networkx as nx


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
        # if not links:
        if not links and pairs[page_index] is None:
            pairs[page_index] = []
        # else:
        elif links:
            for link in links:
                link_original = link.link
                link_index = table_to_alias.get(link_original)
                # if link_index is None:
                if link_index is None and pairs[page_index] is None:
                    pairs[page_index] = []
                # else:
                elif link_index is not None:
                    pairs[page_index].append(link_index)
                    pairs[link_index].append(page_index)
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


def get_links_of_groups(
        pages: Dict[str, Page],
        reversed_partition: Dict[int, List[str]]
) -> Dict[int, List[str]]:
    groups_with_links = defaultdict(list)
    for group_key, nodes in reversed_partition.items():
        for node in nodes:
            full_node = pages.get(node)
            if full_node and full_node.links:
                for link in full_node.links:
                    if link.link not in groups_with_links[group_key]:
                        groups_with_links[group_key].append(link.link)

    return groups_with_links


def reverse_partition(
    partition: Dict[str, int]
) -> Dict[int, List[str]]:
    groups_with_nodes = defaultdict(list)
    for node_key, group_key in partition.items():
        groups_with_nodes[group_key].append(node_key)

    return groups_with_nodes


def get_linked_meta_groups_from_ids(
        pages: Dict[str, Page],
        partition: Dict[str, int]
) -> List[MetaGroup]:
    reversed_partition = reverse_partition(partition)
    groups_with_links = get_links_of_groups(pages, reversed_partition)
    meta_groups = []

    for group_id in groups_with_links:
        group_links = []
        links = groups_with_links[group_id]
        if links is not None:
            for link in links:
                link_to_group = partition.get(link)
                # TODO: if there is no node for the link create a new group with default values
                if link_to_group is not None and link_to_group not in group_links:
                    group_links.append(link_to_group)

        meta_group = MetaGroup(id=group_id, links=group_links, members_count=len(reversed_partition[group_id]))
        meta_groups.append(meta_group)

    return meta_groups


def get_linked_groups(pages: Dict[str, Page]) -> List[MetaGroup]:
    graph = nx.Graph()

    table_to_alias, table_to_original = create_hash_tables(pages)
    vertex_aliases = get_node_aliases(pages, table_to_alias)
    graph_edges = get_edges(vertex_aliases)

    graph.add_nodes_from(table_to_original.keys())
    graph.add_edges_from(graph_edges)

    graph, isolates = filter_isolates(graph)

    partition = cylouvain.best_partition(graph)
    page_originals = get_original_node_key_group_pairs(partition, table_to_original)
    linked_groups = get_linked_meta_groups_from_ids(pages, page_originals)

    groups_and_isolates = insert_isolated_nodes_group(linked_groups, isolates)

    return groups_and_isolates


def get_edges(pages_aliases: Dict[int, List[int]]) -> List[Tuple[int, int]]:
    edges = []

    for page_alias in pages_aliases:
        for destination in pages_aliases[page_alias]:
            edges.append((page_alias, destination))

    return edges


def filter_isolates(
        graph: Any
) -> Tuple[Any, List[int]]:
    isolates = list(nx.isolates(graph))
    graph.remove_nodes_from(isolates)

    return graph, isolates


def insert_isolated_nodes_group(
        linked_meta_groups: List[MetaGroup],
        isolated_nodes: List[int]
) -> List[MetaGroup]:
    meta_group = MetaGroup(id=len(linked_meta_groups), members_count=len(isolated_nodes))
    linked_meta_groups.append(meta_group)

    return linked_meta_groups
