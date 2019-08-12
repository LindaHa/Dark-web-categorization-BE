from collections import defaultdict
from api.models import Group, Link, MetaGroup, Page
from typing import Dict, List, Tuple
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


def strong_connect(
        time: int,
        graph: Dict[int, List[int]],
        node: int,
        is_stack_member_collection: List[bool],
        earliest_reachable_node: List[int],
        discovery_time: List[int],
        visited_stack: List[int],
        components: Dict[int, List[int]],
) -> Tuple[int, Dict[int, List[int]]]:
    # Initialize discovery time and low value
    discovery_time[node] = time
    earliest_reachable_node[node] = time
    time += 1
    is_stack_member_collection[node] = True
    visited_stack.append(node)

    # Go through all vertices adjacent to this one
    for vertex in graph[node]:
        # If v is not visited yet, then recur for it
        if discovery_time[vertex] == -1:
            strong_connect(
                time,
                graph,
                vertex,
                is_stack_member_collection,
                earliest_reachable_node,
                discovery_time,
                visited_stack,
                components,
            )

            # Check if the subtree rooted with v has a connection to
            # the one of the ancestors of u
            # Case 1 (per above discussion on Disc and Low value)
            earliest_reachable_node[node] = min(earliest_reachable_node[node], earliest_reachable_node[vertex])

        elif is_stack_member_collection[vertex]:
            '''Update low value of 'u' only if 'v' is still in stack
            (i.e. it's a back edge, not cross edge).
            Case 2 (per above discussion on Disc and Low value) '''
            earliest_reachable_node[node] = min(earliest_reachable_node[node], discovery_time[vertex])

            # head node found, pop the stack
    w = -1  # To store stack extracted vertices
    if earliest_reachable_node[node] == discovery_time[node]:
        while w != node:
            w = visited_stack.pop()
            components[node].append(w)
            is_stack_member_collection[w] = False

    return (
        time,
        components,
    )


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


def filter_orphaned_nodes(
    reversed_partition: Dict[int, List[str]],
    groups_with_links: Dict[int, List[str]],
) -> List[int]:
    relevant_groups = []

    for group_key, nodes in reversed_partition.items():
        linked_group = groups_with_links[group_key]
        if len(nodes) > 1 and linked_group:
            relevant_groups.append(group_key)

    return relevant_groups


def get_linked_meta_groups_from_ids(
        pages: Dict[str, Page],
        partition: Dict[str, int]
) -> List[MetaGroup]:
    meta_groups = []
    reversed_partition = reverse_partition(partition)
    groups_with_links = get_links_of_groups(pages, reversed_partition)

    relevant_groups = filter_orphaned_nodes(reversed_partition, groups_with_links)

    for group_id in relevant_groups:
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


def find_strong_components(vertices: Dict[int, List[int]]) -> Dict[int, List[int]]:
    # Mark all the vertices as not visited
    # and Initialize parent and visited,
    # and ap(articulation point) arrays
    time = 0
    components = defaultdict(list)

    number_of_vertices = len(vertices)
    discovery_time = [-1] * number_of_vertices
    earliest_reachable_nodes = [-1] * number_of_vertices
    is_stack_member = [False] * number_of_vertices
    visited_stack = []

    # Call the recursive helper function
    # to find articulation points
    # in DFS tree rooted with vertex 'i'
    for vertex in range(number_of_vertices):
        if discovery_time[vertex] == -1:
            time, components = strong_connect(
                time,
                vertices,
                vertex,
                is_stack_member,
                earliest_reachable_nodes,
                discovery_time,
                visited_stack,
                components,
            )

    return components


def get_linked_groups(pages: Dict[str, Page]) -> List[MetaGroup]:
    graph = nx.Graph()

    table_to_alias, table_to_original = create_hash_tables(pages)
    vertex_aliases = get_node_aliases(pages, table_to_alias)
    graph_edges = get_edges(vertex_aliases)

    graph.add_nodes_from(table_to_original.keys())
    graph.add_edges_from(graph_edges)

    partition = cylouvain.best_partition(graph)
    page_originals = get_original_node_key_group_pairs(partition, table_to_original)
    linked_groups = get_linked_meta_groups_from_ids(pages, page_originals)

    return linked_groups


def get_edges(pages_aliases: Dict[int, List[int]]) -> List[Tuple[int, int]]:
    edges = []

    for page_alias in pages_aliases:
        for destination in pages_aliases[page_alias]:
            edges.append((page_alias, destination))

    return edges
