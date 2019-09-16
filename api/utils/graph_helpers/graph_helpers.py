from collections import defaultdict
from api.models import Group, Page, Link
from typing import Dict, List, Tuple
import cylouvain
import networkx as nx
from api.utils.graph_helpers.isolate_helpers import filter_isolates, insert_isolated_nodes_group
from api.utils.graph_helpers.node_alias_helpers import create_hash_tables, get_node_aliases, \
    get_original_node_key_group_pairs
from api.utils.graph_helpers.partition_helpers import reverse_partition

MAX_PARTITION_COUNT = 50


def get_links_and_nodes_of_groups(
        pages: Dict[str, Page],
        reversed_partition: Dict[int, List[str]]
) -> Tuple[Dict[int, List[str]], Dict[int, List[Page]]]:
    """
    :param pages: the original pages from db
    :type pages: Dict[str, Page]
    :param reversed_partition: each partition key with all of its nodes as original page keys
    :type reversed_partition: Dict[int, List[str]]
    :return: links to other nodes and pages of a group
    :rtype:  Tuple[Dict[int, List[str]], Dict[int, List[Page]]]
    """
    groups_with_links = defaultdict(list)
    nodes_of_groups = defaultdict(list)
    for group_key, node_keys in reversed_partition.items():
        for node_key in node_keys:
            full_node = pages.get(node_key)

            if full_node:
                nodes_of_groups[group_key].append(full_node)
                if full_node.links:
                    for link in full_node.links:
                        if link.link not in groups_with_links[group_key]:
                            groups_with_links[group_key].append(link.link)

    return groups_with_links, nodes_of_groups


def get_linked_groups_from_ids(
        pages: Dict[str, Page],
        partition: Dict[str, int],
        parent_group_id: str = None
) -> List[Group]:
    """
    :param pages: the original pages from db
    :type pages: Dict[str, Page]
    :param partition: each page as the original page key with its respective group key
    :type partition:Dict[str, int]
    :param parent_group_id: the parent group key of which pages the subgroups will be created
    :type parent_group_id: str or None
    :return: a list of groups with links to original page keys
    :rtype: List[Group]
    """
    reversed_partition = reverse_partition(partition)
    groups_with_links, nodes_of_groups = get_links_and_nodes_of_groups(pages, reversed_partition)
    groups = []

    for group_id in nodes_of_groups:
        group_links = []
        links = groups_with_links[group_id]
        parent_key_prefix = parent_group_id + "." if parent_group_id else ""
        if links is not None:
            seen_links = []
            for link in links:
                link_to_group = partition.get(link)
                if link_to_group is not None and link_to_group not in seen_links and link_to_group != group_id:
                    new_link = Link(link=str(parent_key_prefix) + str(link_to_group))
                    group_links.append(new_link)
                    seen_links.append(link_to_group)

        whole_group_id = str(parent_key_prefix) + str(group_id)
        group_members = {node.url: node for node in nodes_of_groups.get(group_id)}
        group = Group(
            id=whole_group_id,
            links=group_links,
            members=group_members
        )
        groups.append(group)

    return groups


def get_groups_without_links_and_isolates(
        pages: Dict[str, Page],
        table_to_alias: Dict[str, int],
        table_to_original: Dict[int, str]
) -> Tuple[Dict[str, int], List[int]]:
    """
    :param table_to_alias: page key - alias pairs
    :type table_to_alias: Dict[str, int],
    :param table_to_original: page alias - page key pairs
    :type table_to_original: Dict[str, int],
    :param pages: the original pages from db
    :type pages: Dict[str, Page]
    :return: the original keys of pages with the respective group keys along with isolates if any
    :rtype: Tuple[Dict[str, int], List[int]]
    """
    graph = nx.Graph()

    vertex_aliases = get_node_aliases(pages, table_to_alias)
    graph_edges = get_edges(vertex_aliases)

    graph.add_nodes_from(table_to_original.keys())
    graph.add_edges_from(graph_edges)

    graph_no_isolates, isolates = filter_isolates(graph)

    partition = cylouvain.best_partition(graph_no_isolates)
    originals_page_group_pairs = get_original_node_key_group_pairs(partition, table_to_original)

    return originals_page_group_pairs, isolates


def get_linked_groups(pages: Dict[str, Page], parent_group_id: str = None) -> List[Group]:
    """
    :param parent_group_id:  id of the group of which pages the subgroups will be created
    :type parent_group_id: str
    :param pages: the original pages from db
    :type pages: Dict[str, Page]
    :return: a list of groups with links to other groups with all isolates as a separate group
    :rtype: List[Group]
    """

    mined_data = dict(pages)
    partition_count_last_run = -1
    partition_count = MAX_PARTITION_COUNT + 1
    group_id_to_pages = {}
    number_of_runs = 0
    isolates = []
    linked_groups = []
    original_table_to_alias, original_table_to_original_keys = create_hash_tables(mined_data)
    while partition_count > MAX_PARTITION_COUNT and partition_count_last_run != partition_count:
        number_of_runs += 1
        partition_count_last_run = partition_count
        table_to_alias, table_to_original = create_hash_tables(mined_data)
        page_originals_partition, isolates = get_groups_without_links_and_isolates(mined_data, table_to_alias, table_to_original)
        linked_groups = get_linked_groups_from_ids(mined_data, page_originals_partition, parent_group_id)

        new_mined_data = {}
        partition_count = 0
        new_group_ids_with_pages = {}
        for group in linked_groups:
            partition_count += 1
            new_mined_data[group.id] = Page(id=group.id, url=group.id, links=group.links)
            new_group_ids_with_pages[group.id] = []
            for subgroup_id in group.members:
                if subgroup_id in group_id_to_pages:
                    new_group_ids_with_pages[group.id] += group_id_to_pages[subgroup_id]
                else:
                    new_group_ids_with_pages[group.id].append(group.members[subgroup_id])

        group_id_to_pages = new_group_ids_with_pages
        mined_data = new_mined_data

    for group in linked_groups:
        group.members = {x.url: x for x in group_id_to_pages[group.id]}

    if parent_group_id is None:
        linked_groups = insert_isolated_nodes_group(
            linked_groups,
            isolates if number_of_runs == 1 else [],
            pages,
            original_table_to_original_keys
        )

    return linked_groups


def get_linked_subgroups_of_group(group_id: str, pages: Dict[str, Page]) -> List[Group]:
    """
    :param group_id: id of the group of which pages the subgroups will be created
    :type group_id: str
    :param pages: the original pages from db of the specified group
    :type pages: Dict[str, Page]
    :return: subgroups of with links to other subgroup
    :rtype: List[Group]
    """
    table_to_alias, table_to_original = create_hash_tables(pages)
    groups_no_links = get_groups_without_links_and_isolates(pages, table_to_alias, table_to_original)[0]
    linked_subgroups = get_linked_groups_from_ids(pages, groups_no_links, group_id)

    return linked_subgroups


def get_edges(pages_aliases: Dict[int, List[int]]) -> List[Tuple[int, int]]:
    """
    :param pages_aliases: page aliases with their links as aliases
    :type pages_aliases: Dict[int, List[int]]
    :return: edges represented as source alias and target alias
    :rtype: List[Tuple[int, int]]
    """
    edges = []

    for page_alias in pages_aliases:
        destinations = pages_aliases[page_alias]
        for destination in destinations:
            if destination is not None:
                edges.append((page_alias, destination))

    return edges
