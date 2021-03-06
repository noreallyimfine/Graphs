"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:
    """
    Represent a graph as a dictionary of vertices mapping labels to edges.
    """
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print("ERROR: vertex does not exist.")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            print("ERROR: vertex does not exists.")

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Create a queue
        queue = Queue()
        # Enqueue the starting vertex
        queue.enqueue(starting_vertex)
        # Create a set to store visited
        visited = set()
        # While the queue is not empty
        while queue.size() > 0:
            # Dequeue the first vertex
            v = queue.dequeue()
            # Check if it's been visited
            # If it hasn't been visited
            if v not in visited:
                # Mark it as visited
                print(v)
                visited.add(v)
                # Enqueue all it's neighbors
                for neighbor in self.get_neighbors(v):
                    queue.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Create a stack
        stack = Stack()
        # Push the starting vertex
        stack.push(starting_vertex)
        # Create a set to store visited
        visited = set()
        # While the stack is not empty
        while stack.size() > 0:
            # Pop the first vertex
            v = stack.pop()
            # Check if it's been visited
            # If it hasn't been visited
            if v not in visited:
                # Mark it as visited
                print(v)
                visited.add(v)
                # Push all it's neighbors onto the stack
                for neighbor in self.get_neighbors(v):
                    stack.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # Check if node has been visited
        # If not...
        if starting_vertex not in visited:
            # Mark it as visited
            print(starting_vertex)
            visited.add(starting_vertex)
            # recurse on neighbors
            for neighbor in self.get_neighbors(starting_vertex):
                self.dft_recursive(neighbor, visited=visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create a queue
        q = Queue()
        # Enqueue a path to the starting vertex
        q.enqueue([starting_vertex])
        # Create a set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first path
            path = q.dequeue()
            # grab the vertex from the end of the path
            v = path[-1]
            # check if it's been visited
            # If it hasn't
            if v not in visited:
                # Mark it as visited
                visited.add(v)
                # CHECK IF IT'S THE TARGET
                if v == destination_vertex:
                    # If yes, return the path
                    return path
                # Enqueue a path to all it's neighbors
                for neighbor in self.get_neighbors(v):
                    # make a copy of the path
                    path_copy = path.copy()
                    # Add neighbor to copy
                    path_copy.append(neighbor)
                    # enqueue the copy
                    q.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create a stack
        s = Stack()
        # Push path to start to stack
        s.push([starting_vertex])
        # Visited set
        visited = set()
        # While stack has stuff in it
        while s.size() > 0:
            # Pop path off the stack
            path = s.pop()
            # Get last vertex on path
            v = path[-1]
            # Check if in visited
            # If not...
            if v not in visited:
                # Mark as visited
                visited.add(v)
                # Check if it's the destination
                if v == destination_vertex:
                    return path
                # Push a path to all neighbors to the stack
                for neighbor in self.get_neighbors(v):
                    path_copy = path.copy()
                    path_copy.append(neighbor)
                    s.push(path_copy)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=set()):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # Base case - starting_vertex is destination_vertex
        if starting_vertex == destination_vertex:
            return [destination_vertex]
        # Check if starting vertex in visited
        # If not...
        if starting_vertex not in visited:
            # Mark it as visited
            visited.add(starting_vertex)
            # Recurse on the neighbors
            for neighbor in self.get_neighbors(starting_vertex):
                path = self.dfs_recursive(neighbor, destination_vertex, visited)
                if path:
                    return [starting_vertex] + path


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
