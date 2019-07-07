from collections import defaultdict


def create_hash_tables(pages):
    index = 0
    table_to_index = dict()
    table_to_url = dict()
    for page in pages:
        url = page.url
        if url not in table_to_index:
            table_to_index[url] = index
            table_to_url[index] = url
            index += 1
        for link in page.links:
            link_url = link.get("link")
            if link_url not in table_to_index:
                table_to_index[link_url] = index
                table_to_url[index] = link_url
                index += 1
    return table_to_index, table_to_url


def get_raw_relations(pages):
    pairs = defaultdict(list)
    table_to_index, table_to_url = create_hash_tables(pages)
    for page in pages:
        url = page.url
        page_index = table_to_index[url]
        links = page.links
        if not links:
            pairs[page_index] = []
        else:
            for link in links:
                link_index = table_to_index[link.get('link')]
                pairs[page_index].append(link_index)
    return pairs


#
# def find_strong_components(pages):
#     index = 0
#     visited_stack = defaultdict(list)
#     vertices = get_raw_relations(pages)
#     strongly_connected_components = defaultdict(list)
#     number_of_vertices = len(vertices)
#     for i in range(number_of_vertices):
#         enriched_vertex = dict()
#         enriched_vertex["value"] = i
#         visited_stack, index, strongly_connected_components = strong_connect(
#             enriched_vertex,
#             visited_stack,
#             index,
#             vertices,
#             strongly_connected_components
#         )
#     return strongly_connected_components
#
#
# def strong_connect(vertex, visited_stack, index, vertices, strongly_connected_components):
#     # Set the depth index for v to the smallest unused index
#     vertex["index"] = index
#     vertex["low_link"] = index
#     index += 1
#     visited_stack.push(vertex)
#     vertex["is_on_stack"] = True
#
#     # Consider successors of v
#     for successor_vertex in vertices[vertex]:
#         if successor_vertex['index'] is None:
#             # successor_vertex has not yet been visited; recurse on it
#             strong_connect(successor_vertex, visited_stack, index, vertices, strongly_connected_components)
#             vertex["low_link"] = min(vertex["low_link"], successor_vertex["low_link"])
#         elif successor_vertex["is_on_stack"]:
#             # successor_vertex is in stack S and hence in the current SCC
#             # If successor_vertex is not on stack, then (v, w) is a cross-edge in the DFS tree and must be ignored
#             # Note: The next line may look odd - but is correct.
#             # It says successor_vertex[index] not successor_vertex["low_link"];
#             # that is deliberate and from the original paper
#             vertex["low_link"] = min(vertex["low_link"], successor_vertex["index"])
#
#     # If v is a root node, pop the stack and generate an SCC
#     if vertex["low_link"]:
#         while True:
#             successor_vertex = visited_stack.pop()
#             successor_vertex.on_stack = False
#             strongly_connected_components[vertex] = successor_vertex
#             if successor_vertex == vertex:
#                 break
#         return visited_stack, index, strongly_connected_components


def strong_connect(
        time,
        graph,
        node,
        is_stack_member_collection,
        earliest_reachable_node,
        discovery_time,
        visited_stack,
        components,
):
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


def find_strong_components(pages):
    # Mark all the vertices as not visited
    # and Initialize parent and visited,
    # and ap(articulation point) arrays
    time = 0
    vertices = get_raw_relations(pages)
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
