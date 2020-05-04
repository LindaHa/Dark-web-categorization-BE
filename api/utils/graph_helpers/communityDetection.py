import time
from typing import List, Tuple, Dict
import leidenalg
import igraph as ig
import cylouvain
import networkx as nx

from api.utils.caching_helpers import redis_get_complex_object, redis_cache_complex_object
from api.utils.graph_helpers.isolate_helpers import filter_isolates

def leiden_partition(vertices: List[int], edges: List[Tuple[int, int]]) -> Tuple[Dict[int, int], List[int]]:
    """
    :param vertices: The vertices to be divided into communities by the Leiden algorithm
    :type vertices: List[int]
    :param edges: The links according to which the vertices are divided into communities
    :type edges: List[Tuple[int, int]]
    :return: the partition of the vertices, isolated nodes
    :rtype: Tuple[Dict[int, int], List[int]]
    """
    graph = ig.Graph()

    graph.add_vertices(len(vertices))
    graph.vs['id'] = vertices
    graph.add_edges(edges)

    isolates = [(v.index, v['id']) for v in graph.vs.select(_degree=0)]
    graph.delete_vertices([v[0] for v in isolates])
    isolates = [v[1] for v in isolates]

    if len(graph.vs) == 0:
        return {}, isolates

    exec_time = redis_get_complex_object('exec_time')
    start_time = time.time()
    partition = leidenalg.find_partition(graph, leidenalg.ModularityVertexPartition)
    stop_time = time.time()
    the_time = stop_time - start_time
    print('time: ', the_time)
    redis_cache_complex_object('exec_time', exec_time + the_time)
    partition_map = {}

    for index, p in enumerate(partition.membership):
        partition_map[graph.vs[index]['id']] = p

    return partition_map, isolates


def louvain_partition(vertices: List[int], edges: List[Tuple[int, int]]) -> Tuple[Dict[int, int], List[int]]:
    """
    :param vertices: The vertices to be divided into communities by the Louvain algorithm
    :type vertices: List[int]
    :param edges: The links according to which the vertices are divided into communities
    :type edges: List[Tuple[int, int]]
    :return: the partition of the vertices, isolated nodes
    :rtype: Tuple[Dict[int, int], List[int]]
    """
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    graph_no_isolates, isolates = filter_isolates(graph)

    if not graph_no_isolates.node:
        return {}, isolates

    exec_time = redis_get_complex_object('exec_time')
    start_time = time.time()
    partition = cylouvain.best_partition(graph_no_isolates)
    stop_time = time.time()
    the_time = stop_time - start_time
    redis_cache_complex_object('exec_time', exec_time + the_time)

    return partition, isolates
