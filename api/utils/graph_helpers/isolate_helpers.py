from typing import Any, Tuple, List, Dict

import networkx as nx

from api.models import Group, Page
from api.utils.graph_helpers.category_helpers import create_categories_for_nodes


def filter_isolates(
        graph: Any
) -> Tuple[Any, List[int]]:
    """
    :param graph: the mined graph
    :type graph: networkx graph
    :return: the given graph without isolated vertices and the isolated vertices
    :rtype: Tuple[networkx graph, List[int]]
    """
    isolates = list(nx.isolates(graph))
    graph_no_isolates = graph.copy()
    graph_no_isolates.remove_nodes_from(isolates)

    return graph_no_isolates, isolates


def insert_isolated_nodes_group(
        linked_groups: List[Group],
        isolated_nodes: List[int],
        pages: Dict[str, Page],
        table_to_original: Dict[int, str]
) -> List[Group]:
    """
    :param pages: original and full pages
    :type pages: Dict[str, Page]
    :param linked_groups:  graph vertices divided into groups with links to other groups
    :type linked_groups: List[Group]
    :param isolated_nodes: aliases of nodes with no incoming or outgoing nodes
    :type isolated_nodes: List[int]
    :param table_to_original: node alias - original node key pairs
    :type table_to_original: Dict[int, str]
    :return: the given list enriched with a special group containing only and all isolates
    :rtype: List[Group]
    """
    group_members = {}

    for node_alias in isolated_nodes:
        original_key = table_to_original.get(node_alias)
        full_node = pages.get(original_key)
        group_members[original_key] = full_node

    categories = create_categories_for_nodes([node for key, node in group_members.items()])

    if len(group_members) > 0:
        group = Group(id=str(len(linked_groups)), members=group_members, categories=categories)
        linked_groups.append(group)

    return linked_groups
