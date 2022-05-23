import operator
import collections


class Percept(object):

    def __repr__(self):
        return '<%s>' % getattr(self, '__name__', self.__class__.__name__)

    def is_on_state(self):
        return hasattr(self, 'alive') and self.alive

    def display(self, canvas, x, y, width, height):
        pass


class Agent(Percept):
    def __init__(self, dimension=None):
        self.alive = True
        self.bump = False
        self.img = None
        if dimension is None:
            def dimension(percept):
                return input('Percept=%s; action? ' % percept)
        assert isinstance(dimension, collections.Callable)
        self.state = dimension


def Movement_check(agent):
    move = agent.state

    def states(*percept):
        action = move(*percept)
        print('location: %s percept: %s action: %s' % (
            agent.location, percept, action))
        return action

    agent.state = states
    return agent


class Obstacle(Percept):
    pass


class Stone(Obstacle):
    pass


class Grass(Percept):
    pass


class Cut(Percept):
    pass


REVERT = {
    "Grass": Cut
}


def update(x, **entries):
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


def vector_add(a, b):
    return tuple(map(operator.add, a, b))


orientations = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def distance2(x, y):
    (ax, ay) = x
    (bx, by) = y
    return (ax - bx) ** 2 + (ay - by) ** 2


def tests(test, result, alternative):
    if test:
        if isinstance(result, collections.Callable):
            return result()
        return result
    else:
        if isinstance(alternative, collections.Callable):
            return alternative()
        return alternative


class Environment(object):
    def __init__(self):
        self.objects = []
        self.agents = []

    def all_perc(self):
        return []

    def percept(self, agent):
        return NotImplementedError

    def change_state(self):
        pass

    def is_done(self):
        return not any(agent.is_on_state() for agent in self.agents)

    def step(self):
        if not self.is_done():
            actions = [agent.program(*self.percept(agent))
                       for agent in self.agents]
            for (agent, action) in zip(self.agents, actions):
                self.run_action(agent, action)
            self.change_state()

    def list_object(self, location, tclass=Percept):
        return [thing for thing in self.objects
                if thing.location == location and isinstance(thing, tclass)]

    def percept_at(self, location, tclass=Percept):
        return self.list_object(location, tclass) != []

    def add_object(self, thing, location=None):
        if not isinstance(thing, Percept):
            thing = Agent(thing)
        assert thing not in self.objects, "Don't add the same object twice"
        thing.location = location or self.default_location(thing)
        self.objects.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

    def cut_allthe_grass(self, thing):
        try:
            if thing.__class__.__name__ in REVERT:
                self.add_object(
                    REVERT[thing.__class__.__name__](), thing.location)
            self.objects.remove(thing)
        except ValueError as e:
            print(e)
        if thing in self.agents:
            self.agents.remove(thing)


class Grid2D(Environment):

    def __init__(self, width=10, height=10):
        super(Grid2D, self).__init__()
        update(self, width=width, height=height, observers=[])

    def run_action(self, agent, action):
        agent.bump = False
        if action == 'GoNorth':
            self.move_next_state(agent, vector_add((0, +1), agent.location))
        elif action == 'GoSouth':
            self.move_next_state(agent, vector_add((0, -1), agent.location))
        elif action == 'GoEast':
            self.move_next_state(agent, vector_add((+1, 0), agent.location))
        elif action == 'GoWest':
            self.move_next_state(agent, vector_add((-1, 0), agent.location))

    def move_next_state(self, object, destination):
        object.bump = self.percept_at(destination, Obstacle)
        if not object.bump:
            object.location = destination
            for o in self.observers:
                o.thing_moved(object)

    def add_object(self, object, location=(1, 1)):
        super(Grid2D, self).add_object(object, location)
        object.holding = []
        object.held = None
        for obs in self.observers:
            obs.thing_added(object)

    def cut_allthe_grass(self, thing):
        super(Grid2D, self).cut_allthe_grass(thing)

    def draw_env(self, string):
        objs = {
            "S": Stone,
            "G": Grass,
            "C": Cut
        }
        x, y = 0, 0
        for line in string.splitlines():
            for char in list(line):
                self.add_object(objs[char](), (x, y))
                x += 1
            y += 1
            x = 0

    def sensor(self, observer):
        self.observers.append(observer)


class Entities(Grid2D):
    def __init__(self, width=10, height=10):
        super(Entities, self).__init__(width, height)
        self.start_from = (1, 1)

    def all_perc(self):
        return [Stone, Grass]

    def percept(self, agent):
        status = tests(self.percept_at(agent.location, Grass),
                       'Grass', 'Cut')
        bumps = tests(agent.bump, 'Bump', 'None')

        neighbors = []

        for agent_env in [thing for thing in self.objects
                          if isinstance(thing, Agent)]:
            location_ = agent_env.location
            agent_type = getattr(agent_env, 'name',
                                 agent_env.__class__.__name__)
            if getattr(agent_env, 'id', None) is not None:
                id_ = ("{0}".format(agent_type))

        return status, bumps, neighbors

    def run_action(self, agent, action):
        if action == 'Cut':
            grass_list = self.list_object(agent.location, Grass)
            if grass_list != []:
                grass = grass_list[0]
                agent.performance += 100
                self.cut_allthe_grass(grass)
            else:
                agent.performance -= 20
        elif action != 'NoOp' and action != 'Noop':
            super(Entities, self).run_action(agent, action)
            agent.performance -= 5

    def add_grass(self, location):
        self.add_object(Grass(), location)

    def all_grass(self):

        for y in range(1, self.height):
            for x in range(1, self.width):
                something = False
                for thing in self.objects:
                    if thing.location == (x, y):
                        something = True
                        break
                if not something:
                    self.add_grass((x, y))
