from collections import defaultdict
from api.models import MetaGroup, Page
from typing import Dict, List, Tuple
import cylouvain
import networkx as nx

from api.utils.graph_helpers.isolate_helpers import filter_isolates, insert_isolated_nodes_group
from api.utils.graph_helpers.node_alias_helpers import create_hash_tables, get_node_aliases, \
    get_original_node_key_group_pairs
from api.utils.graph_helpers.partition_helpers import reverse_partition


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
                if link_to_group is not None and link_to_group not in group_links and link_to_group != group_id:
                    group_links.append(link_to_group)

        meta_group = MetaGroup(id=group_id, links=group_links, members_count=len(reversed_partition[group_id]))
        meta_groups.append(meta_group)

    return meta_groups


def get_linked_meta_groups(pages: Dict[str, Page]) -> List[MetaGroup]:
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
