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
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
def reverse_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

def new_entry(player, visited_dict):
    print(f"Entry added for room {player.current_room.id}")
    visited_dict[player.current_room.id] = {}
    
    for dir in player.current_room.get_exits():
        visited_dict[player.current_room.id][dir] = "?"


def bfs(player, visited, target="?"):
    # Initialize a queue
    q = Queue()
    # For every exit from room
    for exit in player.current_room.get_exits():
        # enqueue path to exit
        q.enqueue([exit])
    # use dict lookup to search neighbors for "?"
    # while theres stuff in the queue
    original = player.current_room.id
    while q.size() > 0:
        #print("Queue: ", q.queue)
        current = original
        path = q.dequeue()
        #print("Current:", current)
        #print("Path", path)
        for direction in path[-1]:
            player.travel(direction)
        current = player.current_room.id
        #print("Current after travel:", current)
        direction = path[-1]
        #print("next move:", direction)
        #print("Visited dict at the current room going in last direction of path:", visited[current][direction])
        if visited[current][direction] == target:
            return path
        for nexit in visited[current]:
            #print("Nexit: ", nexit)
            path_copy = path.copy()
            path_copy.append(nexit)
            q.enqueue(path_copy)
               



def explore_world(player):
    # Initialize a stack
    s = Stack()
    # initialize visited dict
    visited = {}
    # path traveled
    path = []
    # Add first room to dict
    new_entry(player, visited)
    # for each exit in the first room
    for direction in player.current_room.get_exits():
        # push (room id, direction) to stack
        s.push((player.current_room.id, direction))
    # while the stack is not empty
    while s.size() > 0:
        # Pop off tuple
        next_exit = s.pop()
        last = next_exit[0]
        direction = next_exit[1]
        # Travel in that direction
        print("Path traveled: ", path)
        print("Current Room #", player.current_room.id)
        print("next exploration tuple", next_exit)
        player.travel(direction)
        path.append(direction)
        print("Current room after travel:", player.current_room.id)
        print(visited)
        # Check if the room is in the dict
        # if not...
        if player.current_room.id not in visited:
            #  Add entry for room
            new_entry(player, visited)
        # Change value for both rooms and dirs
        # Set value of last room at direction traveled to current room
        visited[last][direction] = player.current_room.id
        # Set the value of current room at reverse direction to last room
        reverse = reverse_direction(direction)
        visited[player.current_room.id][reverse] = last
        # Check exits of this room
        counter = 0
        for nexit in player.current_room.get_exits():
            # Check if the value in the dict is "?"
            # iF so, add to stack
            if visited[player.current_room.id][nexit] == "?":
                s.push((player.current_room.id, nexit))
                counter += 1
        if counter == 0:
            # insert breadth first searrch to find last "?"
            print("Start retrace at before bfs call: ", player.current_room.id)
            retrace = bfs(player, visited)
            print("Start retrace at after bfs call: ", player.current_room.id)
            print("Retrace steps from bfs", retrace)
            for move in retrace:
                print("Room as we retrace", player.current_room.id)
                path.append(move)
    return path


    # if not visited:
    #     visited = {}
    #     #new_entry(player, visited)
    # if not rooms_visited:
    #     rooms_visited = set()
    # print("Current Room", player.current_room.id)
    # print("Visited: ", visited)
    # print("Rooms Visited: ", rooms_visited)
    # for dir in player.current_room.get_exits():
    #     current = player.current_room.id
    #     if player.current_room.id not in visited:
    #         new_entry(player, visited)
    #         rooms_visited.add(player.current_room.id)
    #     if visited[player.current_room.id][dir] == "?":    
    #         player.travel(dir)
    #         print("Direction Travelled:", dir)
    #         visited[current][dir] = player.current_room.id
    #         reverse = reverse_direction(dir)
    #         visited[player.current_room.id][reverse] = current
    #         explore_world(player, visited=visited, rooms_visited=rooms_visited)
    # return rooms_visited
# Add current room to top of a stack
# Store room and exits in dict with "?" 
# while stack not empty
# Check out all the exits 
# Check if the room is in dict already
# If not, add room
# Either way, change both "?" directions




traversal_path = explore_world(player)

print(explore_world(player))
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    print(player.current_room)
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
