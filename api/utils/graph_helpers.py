from collections import defaultdict

from api.models import Component


def create_hash_tables(pages):
    index = 0
    table_to_alias = dict()
    table_to_original = dict()
    for page_row in pages:
        page = pages.get(page_row)
        page_id = page.id
        if page_id not in table_to_alias:
            table_to_alias[page_id] = index
            table_to_original[index] = page_id
            index += 1
        # for link in page.links:
        #     link_url = link.get("link")
        #     if link_url not in table_to_alias:
        #         table_to_alias[link_url] = index
        #         table_to_original[index] = link_url
        #         index += 1
    return table_to_alias, table_to_original


def get_page_aliases(pages, table_to_alias):
    pairs = defaultdict(list)
    for page_row in pages:
        page = pages.get(page_row)
        page_index = table_to_alias[page.id]
        if page_index is None:
            break

        links = page.links
        if not links:
            pairs[page_index] = []
        else:
            for link in links:
                link_original = link.link
                link_index = table_to_alias.get(link_original)
                if link_index is None:
                    pairs[page_index] = []
                else:
                    pairs[page_index].append(link_index)
    return pairs


def get_page_originals(components, table_to_original):
    original_components = defaultdict(list)
    for key in components:
        for node_alias in components[key]:
            node_original = table_to_original[node_alias]
            original_components[key].append(node_original)
    return original_components


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


def get_linked_components_from_ids(pages, components):
    linked_components = []
    for key, nodes in components.items():
        component_links = []
        component_pages = []
        for node in nodes:
            full_node = pages.get(node)
            component_pages.append(full_node)
            full_links = full_node.links
            component_links.extend(full_links)

        component = Component(id=key, links=component_links, members=component_pages)
        linked_components.append(component)
    return linked_components


def find_strong_components(vertices):
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


def get_linked_components(pages):
    table_to_alias, table_to_original = create_hash_tables(pages)
    vertices = get_page_aliases(pages, table_to_alias)

    strong_components = find_strong_components(vertices)
    page_originals = get_page_originals(strong_components, table_to_original)
    linked_components = get_linked_components_from_ids(pages, page_originals)

    return linked_components
