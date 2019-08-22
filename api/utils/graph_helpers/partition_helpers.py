from collections import defaultdict
from typing import Dict, List


def reverse_partition(
    partition: Dict[str, int]
) -> Dict[int, List[str]]:
    groups_with_nodes = defaultdict(list)
    for node_key, group_key in partition.items():
        groups_with_nodes[group_key].append(node_key)

    return groups_with_nodes