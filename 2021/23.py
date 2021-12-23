DATA = ['BB', 'CC', 'AD', 'DA']
TESTDATA = ['BA', 'CD', 'BC', 'DA']
# to be inserted in the middle of each existing room
PART2 = ['DD', 'CB', 'BA', 'AC']

ROOMS = ['A', 'B', 'C', 'D']
# (room hallway index, cost of movement)
INDEX = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def part1():
    rooms = dict(zip(ROOMS, map(list, DATA)))
    hallway = [None] * 11
    print(move(hallway, rooms))


def part2():
    rooms = [list(a[0] + b + a[1]) for a, b in zip(DATA, PART2)]
    rooms = dict(zip(ROOMS, rooms))
    # rooms are at index 2, 4, 6 and 8
    hallway = [None] * 11
    # print(rooms)
    print(move(hallway, rooms))


def move(hallway, rooms, energy=0):
    # the rules imply that every amphipod can move at most twice: once into the hallway and once into its final spot
    # pick a movable amphipod that's not in it's final position and move it to any valid location
    return min(move_room(hallway, rooms, energy), move_hallway(hallway, rooms, energy))


def move_room(hallway, rooms, energy):
    min_energy = float('inf')
    moved = False
    for roomid, room in rooms.items():
        # an amphipod can always exit a room because they can't stop in front of one
        pod, new_room, cost = move_out(room, roomid)
        if pod:
            moved = True
            pos = INDEX[roomid]
            goal_pos = INDEX[pod]
            new_rooms = rooms.copy()
            new_rooms[roomid] = new_room
            e = energy + cost * COST[pod]
            # first try to move directly into the goal room
            # note that move_out will only pull an amphipod from its target room if it has to move out of the way for something
            if pod != roomid and can_move(hallway, pos, goal_pos):
                # there is no reason not to move directly into the goal room if it's possible, so don't consider other scenarios anymore
                new_goal_room, goal_cost = move_in(rooms[pod], pod)
                if new_goal_room:
                    goal_energy = e + COST[pod] * (abs(pos - goal_pos) + goal_cost)
                    new_rooms[pod] = new_goal_room
                    return move(hallway, new_rooms, goal_energy)
            # move to valid position in hallway
            for new_pos, new_cost in valid_moves(hallway, pos):
                new_energy = e + COST[pod] * new_cost
                new_hallway = hallway.copy()
                new_hallway[new_pos] = pod
                min_energy = min(min_energy, move(new_hallway, new_rooms, new_energy))
    # at this point no moves are possible
    # if no pods were moved, all are in their target locations or the hallway
    if moved or any(hallway):
        return min_energy
    return energy


def move_hallway(hallway, rooms, energy):
    min_energy = float('inf')
    for pos, pod in enumerate(hallway):
        if pod is None:
            continue
        if can_move(hallway, pos, INDEX[pod]):
            new_goal_room, goal_cost = move_in(rooms[pod], pod)
            if new_goal_room:
                goal_energy = energy + COST[pod] * (abs(pos - INDEX[pod]) + goal_cost)
                new_hallway = hallway.copy()
                new_hallway[pos] = None
                new_rooms = rooms.copy()
                new_rooms[pod] = new_goal_room
                min_energy = min(min_energy, move(new_hallway, new_rooms, goal_energy))
    return min_energy


def move_out(room, goal):
    for i, v in enumerate(room):
        if v is not None:
            break
    if v is None or all(v == goal for v in room[i:]):
        return None, None, None
    r = list(room)
    r[i] = None
    # i + 1 is the cost to move into the hallway
    return v, r, i + 1


# only call for candidates that equal goal (not checked)
def move_in(room, goal):
    for i, v in reversed(list(enumerate(room))):
        if v is None or v != goal:
            break
    if v is not None:
        return None, None
    r = list(room)
    r[i] = goal
    return r, i + 1


def valid_moves(hallway, starting_pos):
    for i in [0, 1, 3, 5, 7, 9, 10]:
        if can_move(hallway, starting_pos, i):
            yield i, abs(starting_pos - i)


def can_move(hallway, frm, to):
    if to < frm:
        return not any(map(bool, hallway[to:frm]))
    return not any(map(bool, hallway[frm+1:to+1]))


if __name__ == '__main__':
    # part1()
    part2()
