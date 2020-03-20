from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
def reverse(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

def new_entry(room, visited_rooms):
    visited_rooms[room.id] = {}
    
    for direction in room.get_exits():
        visited_rooms[room.id][direction] = "?"


def bfs(player, visited_rooms, target="?"):
    # Create a queue
    q = Queue()
    # enqueue path to current room
    q.enqueue([player.current_room.id])
    # initialize empty set of visited rooms
    visited = set()
    # while theres stuff in the queue
    while q.size() > 0:
        # dequeue first path
        path = q.dequeue()
        # get last room on path
        last = path[-1]
        # check if it's been visited
        # if not...
        if last not in visited:
            # mark as visited
            visited.add(last)
            # check if any of its directions have a "?"
            if "?" in visited_rooms[last].values:
                # if so, return the path
                return path
            # otherwise
            # get all exits from last room:
            for direction in visited_rooms[last]:
                next_room = visited_rooms[last][direction]
                # copy path
                path_copy = path.copy()
                # append room in exit direction
                path_copy.append()
                # queue it up 
                q.enqueue(path_copy)
    return None


def explore_world(player, room_graph):
    # Create a stack
    s = Stack()
    # init empty visited dict
    visited_rooms = {}
    # init empty path to fill
    traversal_path = []
    # Add current room to dict
    new_entry(player.current_room, visited_rooms)
    # add room to stack
    s.push(player.current_room)
    # while the stack not empty
    while len(visited_rooms) < len(room_graph):
        # pop off room
        room = s.pop()
        # add room to visited dict
        if room.id not in visited_rooms:
            new_entry(room, visited_rooms)
        # pick a direction that has a ?
        exits = 0
        unexplored_moves = [dir for dir in visited_rooms[player.current_room.id] if [visited_rooms[player.current_room.id][dir] == "?"]]
        move = random.choice(unexplored_moves)
        # find the room in that direction and add as value in dict
        pretend_room = room.get_room_in_direction(move)
        visited_rooms[room.id][move] = pretend_room
        if pretend_room not in visited_rooms:
            new_entry(pretend_room, visited_rooms)
        # add reverse direction to room we are going to
        reverse_dir = reverse(move)
        visited_rooms[pretend_room.id][reverse_dir] = player.current_room.id
        # add direction to path
        player.travel(move)
        traversal_path.append(move)
        # add room to stack
        s.push(pretend_room)
        exits += 1
        # if you run out of ?s
        if exits == 0:
            # implement bfs to find way back to recent ?
            retrace = bfs(player, visited_rooms)
            # append that path to this path
            if retrace is None:
                return traversal_path
            traversal_path.append(retrace)
    return traversal_path


# def bfs(player, visited, target="?"):
#     # Start with a queue
#     # push path of exits to queue
#     # empty visited


# def explore_world(player):
#     # Initialize a stack
#     s = Stack()
#     # initialize visited dict
#     visited = {}
#     # path traveled
#     path = []
#     # Add first room to dict
#     new_entry(player, visited)
#     # for each exit in the first room
#     for direction in player.current_room.get_exits():
#         # push (room id, direction) to stack
#         s.push((player.current_room.id, direction))
#     # while the stack is not empty
#     while s.size() > 0:
#         # Pop off tuple
#         print(s.stack)
#         next_exit = s.pop()
#         last = next_exit[0]
#         direction = next_exit[1]
#         # Travel in that direction
#         print("Path traveled from start: ", path)
#         print("Current Room #", player.current_room.id)
#         print("next exploration tuple", next_exit)
#         player.travel(direction)
#         path.append(direction)
#         print("Current room after travel:", player.current_room.id)
#         print(visited)
#         # Check if the room is in the dict
#         # if not...
#         if player.current_room.id not in visited:
#             #  Add entry for room
#             new_entry(player, visited)
#         # Change value for both rooms and dirs
#         # Set value of last room at direction traveled to current room
#         visited[last][direction] = player.current_room.id
#         # Set the value of current room at reverse direction to last room
#         reverse = reverse_direction(direction)
#         visited[player.current_room.id][reverse] = last
#         # Check exits of this room
#         counter = 0
#         for nexit in player.current_room.get_exits():
#             # Check if the value in the dict is "?"
#             # iF so, add to stack
#             if visited[player.current_room.id][nexit] == "?":
#                 s.push((player.current_room.id, nexit))
#                 counter += 1
#         if counter == 0:
#             # insert breadth first searrch to find last "?"
#             print("Start retrace at before bfs call: ", player.current_room.id)
#             retrace = bfs(player, visited)
#             print("Retrace steps from bfs", retrace)
#             for move in retrace:
#                 player.travel(move)
#                 path.append(move)
#             print("Room after retracing", player.current_room.id)
#             print("Path with retrace", path)
#     return path


traversal_path = explore_world(player, room_graph)

print(explore_world(player, room_graph))
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    #print(player.current_room)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
