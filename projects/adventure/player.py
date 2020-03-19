from util import Stack


class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room

    def travel(self, direction, show_rooms=False):
        next_room = self.current_room.get_room_in_direction(direction)
        if next_room is not None:
            self.current_room = next_room
            if (show_rooms):
                next_room.print_room_description(self)
        else:
            print("You cannot move in that direction.")

    def explore_world(self, traversal_path=[]):
        ## Depth first traversal
        s = Stack()
        # Push starting room to stack
        s.push(self.current_room)
        print('Current Room:', self.current_room.id)
        # intialize empty visited list
        visited = set()
        # while stack has stuff in it
        while s.size() > 0:
            # pop last element
            last_room = s.pop()
            print("Last room", last_room.id)
            # check if visited
            # if not
            if last_room.id not in visited:
                # add to visited
                visited.add(last_room.id)
                print("visited - ", visited)
                # check every exit
                for ex in last_room.get_exits():
                    print("exit", ex)
                    # explore room
                    self.travel(ex)
                    # check if that room has already been explored:
                    # if not, add exit to the path
                    print('Current Room after travelling:', self.current_room.id)
                    if self.current_room.id not in visited:
                        # add exit to path
                        traversal_path.append(ex)
                        # push current room to stack
                    s.push(self.current_room)  
        return traversal_path
