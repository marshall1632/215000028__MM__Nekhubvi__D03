from . agent import *
import random


class DFSsearchClass(Agent):
    def __init__(self, x=2, y=2):
        Agent.__init__(self)
        random.seed()
        self.actions = {0: "GoEast", 1: "GoNorth", 2: "GoWest", 3: "GoSouth", 4: "NoOp"}
        self.current_position = (1, 1)
        self.environmentmap = {self.current_position: ([1, 1, 1, 1], 4)}
        self.childnode = 0
        self.current_node = 'NoOp'

        def insert_location(location, bumps, parent=-1):
            if bumps == 'Bump':
                self.environmentmap[location] = ([0, 0, 0, 0], -1)
                self.environmentmap[location] = ([0, 0, 0, 0], -1)
                checks = tuple(map(sum, list(zip(list(location), [1, 0]))))
                if checks in self.environmentmap:
                    self.environmentmap[checks][0][2] = 0
                checks = tuple(map(sum, list(zip(list(location), [0, 1]))))
                if checks in self.environmentmap:
                    self.environmentmap[checks][0][3] = 0
                checks = tuple(map(sum, list(zip(list(location), [-1, 0]))))
                if checks in self.environmentmap:
                    self.environmentmap[checks][0][0] = 0
                checks = tuple(map(sum, list(zip(list(location), [0, -1]))))
                if checks in self.environmentmap:
                    self.environmentmap[checks][0][1] = 0
            else:
                self.environmentmap[location] = ([1, 1, 1, 1], parent)

        def cost_path():
            if self.childnode == 0:
                return self.current_position[0] + 1, self.current_position[1]
            elif self.childnode == 1:
                return self.current_position[0], self.current_position[1] + 1
            elif self.childnode == 2:
                return self.current_position[0] - 1, self.current_position[1]
            elif self.childnode == 3:
                return self.current_position[0], self.current_position[1] - 1

        def Calculate_path_cost(CheckStatus, bumps, *largs):
            if bumps == 'Bump':
                if self.current_node == "NoOp":
                    return self.current_node
                insert_location(cost_path(), bumps)
                self.environmentmap[self.current_position][0][self.childnode] = 0
                for i in range(0, 4):
                    if (self.environmentmap[self.current_position][0][(self.childnode + i) % 4]) == 1:
                        self.childnode = (self.childnode + i) % 4
                        self.current_node = self.actions[self.childnode]
                        self.environmentmap[self.current_position][0][self.childnode] = 0
                        return self.current_node
                self.childnode = self.environmentmap[self.current_position][1]
                self.current_node = self.actions[self.environmentmap[self.current_position][1]]
                return self.current_node
            else:
                if self.current_node == "GoEast" or self.current_node == "GoNorth" or self.current_node == "GoWest" or self.current_node == "GoSouth":
                    self.current_position = cost_path()
                if self.current_position not in self.environmentmap:
                    insert_location(self.current_position, bumps,
                                    (self.childnode + 2) % 4)
                    check = tuple(map(sum, list(zip(list(self.current_position), [1, 0]))))
                    if check in self.environmentmap:
                        self.environmentmap[self.current_position][0][0] = 0
                        self.environmentmap[check][0][2] = 0
                    check = tuple(map(sum, list(zip(list(self.current_position), [0, 1]))))
                    if check in self.environmentmap:
                        self.environmentmap[self.current_position][0][1] = 0
                        self.environmentmap[check][0][3] = 0
                    check = tuple(map(sum, list(zip(list(self.current_position), [-1, 0]))))
                    if check in self.environmentmap:
                        self.environmentmap[self.current_position][0][2] = 0
                        self.environmentmap[check][0][0] = 0
                    check = tuple(map(sum, list(zip(list(self.current_position), [0, -1]))))
                    if check in self.environmentmap:
                        self.environmentmap[self.current_position][0][3] = 0
                        self.environmentmap[check][0][1] = 0
                if CheckStatus == 'Grass':
                    self.current_node = 'Cut'
                    return self.current_node
                if CheckStatus == 'Cut':
                    j = 0
                    while j < 6:
                        for i in range(0, 4):
                            if j < 5:
                                self.childnode += random.randint(0, 1)
                            if self.environmentmap[self.current_position][0][(self.childnode + i) % 4] == 1:
                                self.childnode = (self.childnode + i) % 4
                                self.current_node = self.actions[self.childnode]
                                self.environmentmap[self.current_position][0][self.childnode] = 0
                                return self.current_node
                        j += 1
                    self.current_node = self.actions[self.environmentmap[self.current_position][1]]
                    self.childnode = self.environmentmap[self.current_position][1]
                    return self.current_node

        self.program = Calculate_path_cost
