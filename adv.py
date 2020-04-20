from room import Room
from player import Player
from world import World

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

# For the current room, pick a random direction to move if that direction is "?"
# For that room, for any direction that returns an error, mark that exit as 0
# For that room, for the first direction that returns success, mark that exit as 1
# Add that direction traveled to the traversal path
# For the current room, mark the opposite direction as 1 because you just came in that way

# if a room has only one exit, it's a dead end
# if the room leading to that exit has only two exits, it's a dead end
# and so on until we reach a room with three exits or more...
# these passages should never be explored again once they've been explored once...


explorer_map = {}
global unexplored_exits
unexplored_exits = 0
global traversal_path
traversal_path = []
opposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
iter_previous_room = 0
dead_ends = []


def explorer(previous_room=0):
    global unexplored_exits
    global traversal_path
    global iter_previous_room
    global dead_ends
    exits = player.current_room.get_exits()
    room = player.current_room.id
    # print(f"Room {room}s exits: {exits}")
    # print("map", explorer_map, "previous room",
    # previous_room, "current room", room)
    unexplored_directions = []

    if room not in explorer_map:
        explorer_map[room] = {}
        for exit_direction in exits:
            # print(f"Checking {exit_direction} of {explorer_map[room]}")
            explorer_map[room][exit_direction] = "?"
            unexplored_exits += 1  # 1: 4
            # print(
            # f"Added {exit_direction} to room {room}, total unexplored exits is {unexplored_exits}")
        # print(f"Room {room} has been added to the map: {explorer_map[room]}")

    # make a list of all unexplored exits for this room
    for exit_direction in exits:
        if explorer_map[room].get(exit_direction, None) is "?":
            unexplored_directions.append(exit_direction)
            # print(
            # f"Added {exit_direction} to possible directions of room {room}: {unexplored_directions}")
        elif explorer_map[room].get(exit_direction, None) is None:
            explorer_map[room][exit_direction] = "?"
            unexplored_exits += 1
            unexplored_directions.append(exit_direction)
            # print(
            # f"Added {exit_direction} to possible directions of room {room}: {unexplored_directions}")
    # print(f"Room {room}s exits: {explorer_map[room]}")
    # print(f"The Map has {unexplored_exits} unexplored exits")
    # print(f"Will prioritize {room}s unexplored exits: {unexplored_directions}")

    # we have all the current room's unexplored exits, now let's randomly pick one of the unexplored ones
    # if there are any unexplored exits on the map
    if unexplored_exits > 0:
        # if the current room has any unexplored exits
        if len(unexplored_directions) > 0:
            # print(
            # f"This room has {len(unexplored_directions)} unexplored exits: {unexplored_directions}")
            random_direction = random.randrange(0, len(unexplored_directions))
            # print(f"Moving {unexplored_directions[random_direction]}")
            player.travel(unexplored_directions[random_direction])
            traversal_path.append(unexplored_directions[random_direction])
            previous_room = room
            iter_previous_room = room
            new_room = player.current_room.id
            # update our map and count of unexplored rooms
            explorer_map[previous_room][unexplored_directions[random_direction]] = new_room
            unexplored_exits -= 1  # 1: 3
            # print(f"Total unexplored exits is {unexplored_exits}")
            if new_room not in explorer_map:
                # print(f"Room {new_room} has been added to the map")
                explorer_map[new_room] = {}
                for exit_direction in player.current_room.get_exits():
                    if explorer_map[new_room].get(exit_direction, None) is None:
                        # print(
                        # f"Checking {exit_direction} of {explorer_map[new_room]}")
                        explorer_map[new_room][exit_direction] = "?"
                        unexplored_exits += 1  # 1: 4
                        # print(
                        # f"Added {exit_direction} to room {new_room}, total unexplored exits is {unexplored_exits}")
            opposite_direction = opposite_directions[unexplored_directions[random_direction]]
            if explorer_map[new_room].get(opposite_direction, None) is "?":
                explorer_map[new_room][opposite_direction] = previous_room
                unexplored_exits -= 1
                # print(f"Added {opposite_direction} to room {new_room}")
                # print(f"Total unexplored exits is {unexplored_exits}")
            else:
                explorer_map[new_room][opposite_direction] = previous_room
                # print(f"Updated {opposite_direction} of room {new_room}")
                # print(f"Total unexplored exits is {unexplored_exits}")

            # explorer(previous_room)
        # if there is only one direction left, then let's go backwards cuz we're at a dead end
        if len(exits) is 1:
            # print("Dead end, doubling back")
            if room not in dead_ends:
                dead_ends.append(room)
            # if the previous room had only two exits, it lead only to the dead end so blacklist it

            def dead_end_checker(room_to_check):
                if len(explorer_map[room_to_check]) is 2:
                    for connection in explorer_map[room_to_check]:
                        if len(explorer_map[explorer_map[room_to_check][connection]]) is 2 and explorer_map[room_to_check][connection] not in dead_ends:
                            dead_ends.append(
                                explorer_map[room_to_check][connection])
                            dead_end_checker(
                                explorer_map[room_to_check][connection])
            dead_end_checker(previous_room)
            # if len(explorer_map[previous_room]) is 2:
            #     for connections in explorer_map[previous_room]:

            #     if previous_room not in dead_ends:
            #         dead_ends.append(previous_room)
            #     for passage in explorer_map[previous_room]:
            #         connected_room = explorer_map[previous_room][passage]
            #         if len(explorer_map[connected_room]) is 2 and explorer_map[connected_room] not in dead_ends:
            #             dead_ends.append(connected_room)
            player.travel(exits[0])
            if explorer_map[room].get(exits[0], "?") is "?":
                explorer_map[new_room][exits[0]] = previous_room
            if unexplored_exits > 0:
                traversal_path.append(exits[0])
                iter_previous_room = room
                # explorer(room)
        # finally, if there are more than 1 exits and all rooms are explored, let's pick a random direction to travel
        # just make sure not to go backwards from where we just came from
        elif len(unexplored_directions) is 0:
            # print(f"Room {room} has no unexplored exits")
            # print(
            # f"Room {room} has these exits: {exits}, we came from {previous_room}")
            allowed_directions = []
            # Make a list of all the possible exits, excluding the one we came from
            for exit_direction in exits:
                if explorer_map[room][exit_direction] is not previous_room and (explorer_map[room][exit_direction] not in dead_ends or len(exits) is 2):
                    allowed_directions.append(exit_direction)
            # for the allowed directions, pick a random one and go there
            if len(allowed_directions) > 0:
                random_direction = random.randrange(0, len(allowed_directions))
                player.travel(allowed_directions[random_direction])
                traversal_path.append(allowed_directions[random_direction])

            if unexplored_exits > 0:
                iter_previous_room = room
                # explorer(room)


explorer(iter_previous_room)
while unexplored_exits > 0:
    explorer(iter_previous_room)

print(explorer_map)
print(dead_ends)
# print(traversal_path)

# {0: {'n': 1, 's': 5, 'w': 7, 'e': 3}, 1: {'s': 0, 'n': 2}, 2: {'s': 1}, 7: {'e': 0, 'w': 8},
# 8: {'e': 7, 's': 9}, 9: {'n': 8, 's': 10}, 10: {'n': 9, 'e': 11}, 11: {'w': 10, 'e': 6},
# 6: {'w': 11, 'n': 5}, 5: {'s': 6, 'n': 0}, 3: {'w': 0, 'e': 4}, 4: {'w': 3}}
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
