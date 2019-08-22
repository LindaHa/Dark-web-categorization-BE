from typing import Any, Tuple, List

import networkx as nx

from api.models import MetaGroup


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