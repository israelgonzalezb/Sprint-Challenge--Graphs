from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
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

# For the current room, pick a random direction to move if that direction is "?"
# For that room, for any direction that returns an error, mark that exit as 0
# For that room, for the first direction that returns success, mark that exit as 1
# Add that direction traveled to the traversal path
# For the current room, mark the opposite direction as 1 because you just came in that way


explorer_map = {}
unexplored_rooms = 1


def explorer(previous_room=0):
    global unexplored_rooms
    print(f"The Map has {unexplored_rooms} unexplored rooms")
    exits = player.current_room.get_exits()
    print("exits", exits)
    room = player.current_room.id
    print("map", explorer_map, "previous room",
          previous_room, "current room", room)
    exit_count = len(exits)
    random_indexes = []
    possible_directions = []

    opposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}

    if room not in explorer_map:
        explorer_map[room] = {}
        unexplored_rooms -= 1

    for exit_direction in exits:
        if exit_direction not in explorer_map[room]:
            # -> {0: {'n': ?, 's': '?', 'w': '?', 'e': '?'}}
            explorer_map[room][exit_direction] = "?"
            unexplored_rooms += 1

    # we have all the unexplored exits, now let's randomly pick one of the unexplored ones
    # make a list of all unexplored exits
    for exit_direction in exits:
        if explorer_map[room][exit_direction] is "?":
            possible_directions.append(exit_direction)

    # if there are any unexplored exits, pick a random one to travel to
    if len(possible_directions) > 0:
        print(
            f"This room has {len(possible_directions)} unexplored exits: {possible_directions}")
        random_direction = random.randrange(0, len(possible_directions))
        print(f"Moving {possible_directions[random_direction]}")
        player.travel(possible_directions[random_direction])
        previous_room = room
        new_room = player.current_room.id
        explorer_map[previous_room][possible_directions[random_direction]] = new_room
        if new_room not in explorer_map:
            explorer_map[new_room] = {}
            unexplored_rooms -= 1
        opposite_direction = opposite_directions[possible_directions[random_direction]]
        if explorer_map[new_room].get(opposite_direction, "?") is "?":
            explorer_map[new_room][opposite_direction] = previous_room
        explorer(previous_room)
    # if there is only one direction left, then let's go backwards cuz we're at a dead end
    if len(exits) is 1:
        print("Dead end, doubling back")
        player.travel(exits[0])
        explorer(room)
    # finally, if there are more than 1 exits and all rooms are explored, let's pick a random direction to travel
    # just make sure not to go backwards from where we just came from
    if len(possible_directions) is 0 and unexplored_rooms > 0:
        print(f"This room has no unexplored exits")
        allowed_directions = []
        # Make a list of all the possible exits, excluding the one we came from
        for exit_direction in exits:
            if explorer_map[room][exit_direction] is not previous_room:
                allowed_directions.append(exit_direction)
        # for the allowed directions, pick a random one and go there
        random_direction = random.randrange(0, len(allowed_directions))
        player.travel(allowed_directions[random_direction])
        explorer(room)

    # while len(random_indexes) < exit_count:
    #     random_index = random.randrange(0, exit_count)
    #     if random_index not in random_indexes:
    #         random_indexes.append(random_index)
    #     print(random_indexes)

    # for idx in random_indexes:
    #     if explorer_map[room][exits[idx]] is "?":
    #         player.travel(exits[idx])
    #         previous_room = room
    #         new_room = player.current_room.id
    #         explorer_map[previous_room][exits[idx]] = new_room
    #         print("new room", new_room)
    #         opposite_direction = opposite_directions[exits[idx]]
    #         print("opposite direction", opposite_direction)
    #         if new_room not in explorer_map:
    #             explorer_map[new_room] = {}
    #         explorer_map[new_room][opposite_direction] = previous_room
    #         explorer()

    #direction = directions[random.randint(0,4)]
while unexplored_rooms > 0:
    explorer()
print(explorer_map)

traversal_path = ["n", "n", "n"]

# {0: {'n': 1, 's': 5, 'w': 7, 'e': 3}, 3: {'w': 0, 'e': 3}, 5: {'n': 0, 's': 0}, 1: {'n': 1, 's': 0}, 7: {'w': 8, 'e': 0}, 8: {'e': 7}}
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
