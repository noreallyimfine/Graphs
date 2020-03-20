from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

#random.seed(175456)
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

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

def bfs(player, visited_rooms):
    room = player.current_room
    q = Queue()
    q.enqueue([room.id])
    visited = set()
    
    while q.size() > 0:
        path = q.dequeue()
        last = path[-1]
        if last not in visited:
            visited.add(last)
            for direction in visited_rooms[last]:
                if visited_rooms[last][direction] == "?":
                    return path
                elif visited_rooms[last][direction] not in visited:
                    path_copy = path.copy()
                    path_copy.append(visited_rooms[last][direction])
                    q.enqueue(path_copy)
    return path

# def bfs(player, visited_rooms, target="?"):
#     # Create a queue
#     q = Queue()
#     # enqueue path to current room
#     q.enqueue([player.current_room])
#     # initialize empty set of visited rooms
#     traversal_path = []
#     visited = set()
#     # while theres stuff in the queue
#     while q.size() > 0:
#         # dequeue first path
#         path = q.dequeue()
#         # get last room on path
#         last = path[-1]
#         print("last value", last.id)
#         print("current room", player.current_room.id)
#         # check if it's been visited
#         # if not...
#         if last.id not in visited:
#             # mark as visited
#             visited.add(last.id)
            
#             # check if any of its directions have a "?"
#             if "?" in visited_rooms[last.id].values():
#                 # loop through path by index
#                 for i in range(len(path)):
#                     # loop through moves on current index
#                     for direction in visited_rooms[path[i].id]:
#                         # if moving in that direction gives us room at index+1
#                         if last.get_room_in_direction(direction) == path[i+1]:
#                             # append that direction to traversal path
#                             traversal_path.append(direction)
#                     # if so, return the path
#                     return traversal_path
#             # otherwise
#             # get all exits from last room:
#             for direction in visited_rooms[last.id]:

#                 ##############################
#                 next_room = last.get_room_in_direction(direction)
#                 #next_room = visited_rooms[last.id][direction]
#                 ##############################
                
                
#                 # copy path
#                 path_copy = path.copy()
#                 # append room in exit direction
#                 path_copy.append(next_room)
#                 # queue it up 
#                 q.enqueue(path_copy)
#     return None


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
    while s.size() > 0:
        # pop off room
        room = s.pop()
        # add room to visited dict
        if room.id not in visited_rooms:
            new_entry(room, visited_rooms)

        # pick a direction that has a ?

        unexplored_moves = []
        for direction in visited_rooms[player.current_room.id]:
            if visited_rooms[player.current_room.id][direction] == "?":
                unexplored_moves.append(direction)

        ##########

        print("Unexplored moves", unexplored_moves)
        if len(unexplored_moves) > 0:
            move = random.choice(unexplored_moves)
            # find the room in that direction and add as value in dict
            pretend_room = room.get_room_in_direction(move)
            visited_rooms[room.id][move] = pretend_room.id
            if pretend_room not in visited_rooms:
                new_entry(pretend_room, visited_rooms)
            # add reverse direction to room we are going to
            reverse_dir = reverse(move)
            visited_rooms[pretend_room.id][reverse_dir] = player.current_room.id
            print("Pretend room reverse value: ", visited_rooms[pretend_room.id][reverse_dir])
            print("Pretend room values: ", visited_rooms[pretend_room.id]) 
            # add direction to path
            print("Traversal path", traversal_path)
            print("Current room: ", player.current_room.id)
            print("Next move: ", move)
            print("Moving to room:", pretend_room.id)
            player.travel(move)
            traversal_path.append(move)
            # add room to stack
            s.push(pretend_room)
        
        # if you run out of ?s
        else:
            # implement bfs to find way back to recent ?
            retrace = bfs(player, visited_rooms)
            # append that path to this path
            if retrace is None:
                return traversal_path
            
            # ###################################
            # for walk_back in retrace:
            #     player.travel(walk_back)
            #     traversal_path.append(move)
            traversal_path.append(retrace)
            ###################################
    return traversal_path


traversal_path = explore_world(player, room_graph)

# print(explore_world(player, room_graph))
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
