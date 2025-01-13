import random
import time
import os
import heapq as hq



"""A program that utilises Dijkstra's algorithm to find the most
efficient (least net change in self value) from a starting point
on a 2d map to a target point. This map has randomly assigned values
and obstacles that the creature must work around. 
This is an adapted version of previous code where the user could input
themselves. This has been removed for simplicity."""



HISTORY_MARKER = '⬜'
OBSTACLE_MARKER = '⬛'
TARGET_MARKER = '🟩'



class Map:
    def __init__(self, height, width, creature, mapvals = None):
        """Initiates dimensions, values, target location and creature placeholder."""
        self.height, self.width = height, width
        self.size = (height, width)

        self.creature = creature
        if mapvals is None:
            self.mapvals = [[random.randint(1, 9) if random.random() > 0.25 else -1 for c in range(width)] for r in range(height)]
        else:
            self.mapvals = mapvals

        self.mapvals[creature.y][creature.x] = None
        self.mapvals[creature.target_pos[0]][creature.target_pos[1]] = 0


    def update(self):
        """Prints all values, creature location, target location"""
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"{'':-^70s}\nMap: \n")
        for r in range(self.height):
            for c in range(self.width):
                if (r, c) == self.creature.pos:
                    print(f"{self.creature.appearance:>3s}", end="")
                elif (r, c) == self.creature.target_pos:
                    print(f"{TARGET_MARKER:>3s}", end="")
                elif self.mapvals[r][c] == -1:
                    print(f"{OBSTACLE_MARKER:>3s}", end="")
                elif (r, c) in self.creature.history:
                    print(f"{HISTORY_MARKER:>3s}", end="")
                else:
                    print(f"{self.mapvals[r][c]:>4d}", end="")
            print("\n")
        print(f"\n{'':-^70s}")



class Creature:
    def __init__(self, start_x, start_y, target_pos, appearance):
        self.x = start_x
        self.y = start_y
        self.pos = (self.y, self.x)

        self.value = 0

        self.appearance = appearance

        self.target_pos = target_pos

        self.history = []
        self.path = []


    def move(self, n_tile, map_ob):
        self.history.append(self.pos)
        self.pos = n_tile
        self.value += map_ob.mapvals[n_tile[0]][n_tile[1]]


    def neighbourdict(self, map_ob):
        neighbour_dic = {}

        for r in range(len(map_ob.mapvals)):
            for n, c in enumerate(map_ob.mapvals[r]):
                if c == -1:
                    continue

                pos = (r, n)

                neighbour_dic[pos] = {}

                p_neighbours = [
                    (pos[0] - 1, pos[1]), # Up
                    (pos[0], pos[1] + 1), # Right
                    (pos[0] + 1, pos[1]), # Down
                    (pos[0], pos[1] - 1), # Left
                ]

                for p in p_neighbours:
                    try:
                        neighbour = map_ob.mapvals[p[0]][p[1]]
                        if -1 not in [neighbour, p[0], p[1]]:
                            neighbour_dic[pos][p] = neighbour        
                    except:
                        pass
        return neighbour_dic


    def find_shortest_path(self, map_ob):
        neighbour_dic = self.neighbourdict(map_ob)
        prioq = [(0, self.pos)]
        self.costs = {self.pos: 0}
        prev = {self.pos: None}
        visited = set()

        while prioq:
            c_cost, c_tile =  hq.heappop(prioq)
            if c_tile in visited:
                continue
            visited.add(c_tile)

            if c_tile == self.target_pos:
                break

            for neighbour, cost in neighbour_dic.get(c_tile, {}).items():
                if neighbour in visited:
                    continue
                n_cost = c_cost + cost

                if n_cost < self.costs.get(neighbour, float('inf')):
                    self.costs[neighbour] = n_cost
                    prev[neighbour] = c_tile
                    hq.heappush(prioq, (n_cost, neighbour))

        current = self.target_pos
        while current:
            self.path.append(current)
            current = prev.get(current)
        self.path.reverse()

        return self.path if self.costs.get(self.target_pos) != float('inf') else [], self.costs.get(self.target_pos, float('inf'))


def random_main():
        """Main function to run the simulation of the creature finding a path."""

        mapy=random.randint(1, 14)
        mapx=random.randint(1, 20)
        print(f"Map dimensions: {mapy} x {mapx}")

        targ_pos = (random.randint(mapy // 2, mapy - 1), random.randint(mapx // 2, mapx - 1))

        g_creature = Creature(0, 0, targ_pos, '🟥')
        g_map = Map(mapy, mapx, g_creature)

        s_path, cost = g_creature.find_shortest_path(g_map)
        s_path.pop(0)

        g_map.update()
        input("type to continue: ")
        while True:
            
            if g_creature.pos == targ_pos:
                msg = f"The void consumes.\nCurrent value: {g_creature.value}"
            elif not s_path:
                msg = "It appears there is no valid path for the creature to tread."

            if not s_path:
                g_map.update()
                print(msg)

                if input("Proceed? ").strip().lower() == 'e':
                        return False
                return True

            g_map.update()
            print(f"Path: {s_path}")
            print(f"Projected cost: {cost}")
            print(f"Current value: {g_creature.value}")

            if mode == 0:
                time.sleep(t) 
            else:
                if input("Proceed? ").lower() == 'e':
                    return False

            if s_path:
                next_move = s_path.pop(0)
                g_creature.move(next_move, g_map)


def pre_set_main():

    mapused = [
    [100, 1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    [100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100],
    [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 1, 100],
    [100, 100, 100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100],
    [100, 100, 100, 1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 1, 100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 100],
    [100, 100, 100, 1, 100, 1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 1, 100, 100],
    [100, 100, 100, 1, 100, 1, 100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 100],
    [100, 100, 100, 1, 100, 1, 100, 1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 1, 1, 1, 100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]
    
    mapy = len(mapused)
    mapx = len(mapused[0])

    found = False
    for i in range(len(mapused)):
        for j in range(len(mapused[i])):
            if mapused[i][j] == 0:
                targx, targy = i, j
                found = True
                break
        if found:
            break


    g_creature = Creature(0, 0, (targx, targy), '🟥')
    g_map = Map(mapy, mapx, g_creature, mapused)

    s_path, cost = g_creature.find_shortest_path(g_map)
    s_path.pop(0)

    g_map.update()
    input("type to continue: ")
    while True:
            
            if g_creature.pos == (targx, targy):
                msg = f"The void consumes.\nCurrent value: {g_creature.value}"
            elif not s_path:
                msg = "It appears there is no valid path for the creature to tread."

            if not s_path:
                g_map.update()
                print(msg)
                break

            g_map.update()
            print(f"Path: {s_path}")
            print(f"Projected cost: {cost}")
            print(f"Current value: {g_creature.value}")

            if mode == 0:
                time.sleep(t) 
            else:
                if input("Proceed? ").lower() == 'e':
                    return False

            if s_path:
                next_move = s_path.pop(0)
                g_creature.move(next_move, g_map)


# Settings.
mode = 0    # 0 is time
t = 0.1     # Time interval for movement (seconds)

if __name__ == "__main__":
    os.system('cls')
    try:
        if int(input("Type (0 for preset, anything else for random): ")) == 0:
            main_t = pre_set_main
        else:
            main_t = random_main
    except:
        main_t = random_main

    running = True

    while running:
        running = main_t()
    print("\nThe creature rests.")

