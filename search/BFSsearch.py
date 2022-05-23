from .agent import *


class BFSsearchClass(Agent):

    def __init__(self, x=2, y=2):
        Agent.__init__(self)
        self.map = {(0, 0): [True, True, True, True, 0, True]}
        self.position = (0, 0)
        self.movement = (0, 0)
        self.Initial_state = 'GoNorth'
        self.move_node = True

        self.tempo = 0

        def program(status, bump, *largs):

            def positioning():
                coordinate = vector_add((0, 1), self.movement)
                coordsouth = vector_add((0, -1), self.movement)
                coordwest = vector_add((-1, 0), self.movement)
                coordeast = vector_add((1, 0), self.movement)

                if coordinate in self.map:
                    self.map[coordinate][1] = False
                else:
                    self.map[coordinate] = [True, False, True, True, 9, False]

                if coordsouth in self.map:
                    self.map[coordsouth][0] = False
                else:
                    self.map[coordsouth] = [False, True, True, True, 9, False]

                if coordwest in self.map:
                    self.map[coordwest][3] = False
                else:
                    self.map[coordwest] = [True, True, True, False, 9, False]

                if coordeast in self.map:
                    self.map[coordeast][2] = False
                else:
                    self.map[coordeast] = [True, True, False, True, 9, False]

            def position_Cut():
                coordinate = vector_add((0, 1), self.position)
                coordsouth = vector_add((0, -1), self.position)
                coordwest = vector_add((-1, 0), self.position)
                coordeast = vector_add((1, 0), self.position)

                if coordinate in self.map:
                    self.map[coordinate][1] = False
                else:
                    self.map[coordinate] = [True, False, True, True, 9, False]

                if coordsouth in self.map:
                    self.map[coordsouth][0] = False
                else:
                    self.map[coordsouth] = [False, True, True, True, 9, False]

                if coordwest in self.map:
                    self.map[coordwest][3] = False
                else:
                    self.map[coordwest] = [True, True, True, False, 9, False]

                if coordeast in self.map:
                    self.map[coordeast][2] = False
                else:
                    self.map[coordeast] = [True, True, False, True, 9, False]

            def goal(direction):
                if direction == 1:
                    self.position = vector_add((0, 1), self.position)
                    return 'GoNorth'
                elif direction == 2:
                    self.position = vector_add((0, -1), self.position)
                    return 'GoSouth'
                elif direction == 3:
                    self.position = vector_add((-1, 0), self.position)
                    return 'GoWest'
                elif direction == 4:
                    self.position = vector_add((1, 0), self.position)
                    return 'GoEast'

            def move_to_goal():
                if self.Initial_state == 'GoNorth':
                    self.map[self.movement][4] = 2
                elif self.Initial_state == 'GoSouth':
                    self.map[self.movement][4] = 1
                elif self.Initial_state == 'GoWest':
                    self.map[self.movement][4] = 4
                elif self.Initial_state == 'GoEast':
                    self.map[self.movement][4] = 3

            def pos_state():
                if self.Initial_state == 'GoNorth':
                    self.movement = vector_add((0, 1), self.position)
                elif self.Initial_state == 'GoSouth':
                    self.movement = vector_add((0, -1), self.position)
                elif self.Initial_state == 'GoWest':
                    self.movement = vector_add((-1, 0), self.position)
                elif self.Initial_state == 'GoEast':
                    self.movement = vector_add((1, 0), self.position)

            def move_back():
                if self.Initial_state == 'GoNorth':
                    self.map[self.movement][1] = False
                if self.Initial_state == 'GoSouth':
                    self.map[self.movement][0] = False
                if self.Initial_state == 'GoWest':
                    self.map[self.movement][3] = False
                if self.Initial_state == 'GoEast':
                    self.map[self.movement][2] = False

            def move_north():
                if self.map[self.position][0] == True:
                    self.Initial_state = 'GoNorth'
                    self.map[self.position][0] = False
                elif self.map[self.position][1] == True:
                    self.Initial_state = 'GoSouth'
                    self.map[self.position][1] = False
                elif self.map[self.position][2] == True:
                    self.Initial_state = 'GoWest'
                    self.map[self.position][2] = False
                elif self.map[self.position][3] == True:
                    self.Initial_state = 'GoEast'
                    self.map[self.position][3] = False
                elif self.map[self.position][4] != 0:
                    self.move_node = True
                    self.Initial_state = goal(self.map[self.position][4])
                else:
                    self.Initial_state = 'Noop'

            def draw_state():
                if self.Initial_state == 'GoNorth':
                    self.Initial_state = 'GoSouth'
                elif self.Initial_state == 'GoSouth':
                    self.Initial_state = 'GoNorh'
                elif self.Initial_state == 'GoWest':
                    self.Initial_state = 'GoEast'
                elif self.Initial_state == 'GoEast':
                    self.Initial_state = 'GoWest'

            if self.Initial_state == 'Noop':
                return 'Noop'

            pos_state()
            if status == 'Grass':
                return 'Cut'

            if bump == 'Bump':
                positioning()
                move_north()
                return self.Initial_state

            if not self.move_node:
                verifica = self.movement in self.map

                if verifica and self.map[self.movement][5] == False:
                    self.map[self.movement][5] = True
                    move_to_goal()
                    move_back()
                    self.position = self.movement
                    position_Cut()
                    move_north()
                    return self.Initial_state

                elif verifica:
                    self.tempo = 2
                    self.move_node = True
                    move_back()
                    draw_state()
                    return self.Initial_state
                else:
                    self.tempo = 3
                    self.map[self.movement] = [True, True, True, True, 0, True]
                    move_to_goal()
                    move_back()
                    self.position = self.movement
                    position_Cut()
                    move_north()
                    return self.Initial_state
            else:
                self.tempo = 4
                self.move_node = False
                move_north()
                position_Cut()
                return self.Initial_state

        self.program = program
