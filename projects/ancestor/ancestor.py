class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


def earliest_ancestor(ancestors, starting_node, counter=0):
    # DFS and store a max_len
    """
    Return a ID of earliest ancestor using depth-first search
    """
    # Create a stack
    stack = Stack()
    # Push the starting vertex
    stack.push([starting_node])
    # Create a set to store visited
    visited = set()
    # While the stack is not empty
    while stack.size() > 0:
        # Pop the first path
        path = stack.pop()
        # get parent from last pair
        print(path)
        parent = path[-1]
        # Check if it's been visited
        # If it hasn't been visited
        if parent not in visited:
            # Mark it as visited
            print(parent)
            visited.add(parent)
            # Push all it's neighbors onto the stack
            for grandparent in ancestors:
                if grandparent[1] == parent:
                    path_copy = path.copy()
                    path_copy.append(grandparent[0])
                    stack.push(path_copy)
    if len(path) < 2:
        return -1
    else:
        return path[-1]


if __name__ == "__main__":
    ancestors = [(1, 3), (2, 3), (3, 6),
                 (5, 6), (5, 7), (4, 5),
                 (4, 8), (8, 9), (11, 8), (10, 1)]
    starting_node = 6
    earliest_ancestor(ancestors, starting_node)