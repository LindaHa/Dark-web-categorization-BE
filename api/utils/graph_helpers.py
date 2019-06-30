from collections import defaultdict


# This class represents an directed graph
# using adjacency list representation
class Graph:
    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.components = defaultdict(list)

        self.Time = 0

    # function to add an edge to the graph
    def add_edge(self, u, v):
        self.graph[u].append(v)

    def add_to_component(self, u, w):
        self.components[u].append(w)

    def find_strongly_connected_components_recursively(self, u, low, disc, stack_member, st):
        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stack_member[u] = True
        st.append(u)

        # Go through all vertices adjacent to this one
        for v in self.graph[u]:

            # If v is not visited yet, then recur for it
            if disc[v] == -1:

                self.find_strongly_connected_components_recursively(v, low, disc, stack_member, st)

                # Check if the subtree rooted with v has a connection to
                # the one of the ancestors of u
                # Case 1 (per above discussion on Disc and Low value)
                low[u] = min(low[u], low[v])

            elif stack_member[v]:

                '''Update low value of 'u' only if 'v' is still in stack 
                (i.e. it's a back edge, not cross edge). 
                Case 2 (per above discussion on Disc and Low value) '''
                low[u] = min(low[u], disc[v])

                # head node found, pop the stack

        w = -1  # To store stack extracted vertices
        if low[u] == disc[u]:
            while w != u:
                w = st.pop()
                self.add_to_component(u, w)
                stack_member[w] = False

            # The function to do DFS traversal.
        # It uses recursive find_strongly_connected_components()

    def find_strongly_connected_components(self):
        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        disc = [-1] * self.V
        low = [-1] * self.V
        stack_member = [False] * self.V
        st = []

        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for i in range(self.V):
            if disc[i] == -1:
                self.find_strongly_connected_components_recursively(i, low, disc, stack_member, st)
