from import_file import *

Agent_l = search_list.load_agents()
map_l = maps.get_maps()


class GrassingCuttingAgent(App):
    def __init__(self):
        App.__init__(self)
        self.Count_Steps = 0
        self.agent = "Agent A"
        self.agent_pic = "img/machine.jpg"
        self.agentImg = None
        self.stones = Image(source="img/bump_to.jpg")
        self.grass = Image(source="img/grass.jpg")
        self.map = None
        self.run_game = False
        self.environment = None
        self.state_num = 0
        self.initialized = False

    def __initialize_env(self):
        if self.environment is not None:
            del self.environment
            self.environment = None
        if self.map is not None:
            self.environment = map_l[self.map]()
        if self.agent in Agent_l:
            agent_A = Movement_check(Agent_l[self.agent]())
            if agent_A.img is not None and check_img(agent_A.img):
                self.agentImg = Image(
                    source=path.join("agents_dir", path.join("img", agent_A.img)))
            else:
                self.agentImg = Image(source=self.agent_pic)
            self.environment.add_object(agent_A, location=self.environment.start_from)

    def get_scores(self):
        return "ScoreA = {0:d}".format(self.Count_Steps)

    def update_canvas(self, labels, grs, *largs):
        grs.canvas.clear()
        self.counter.text = str(self.state_num)
        nx, ny = max([thing.location for thing in self.environment.objects])
        x = grs.width / float(nx + 1)
        y = grs.height / float(ny + 1)
        labelA, label = labels
        with grs.canvas:
            for thing in [thing for thing in self.environment.objects
                          if isinstance(thing, Grass) or
                             isinstance(thing, Cut)]:
                pos_x, pos_y = thing.location
                if isinstance(thing, Grass):
                    Color(0.5, 0, 0)
                    Rectangle(
                        pos=(
                            pos_x * x + grs.x,
                            pos_y * y + grs.y),
                        size=(x, y))
                    Color(1, 1, 1, 1)
                    Rectangle(texture=self.grass.texture,
                              pos=(
                                  pos_x * x + grs.x,
                                  pos_y * y + grs.y
                              ),
                              size=(x, y))
                elif isinstance(thing, Cut):
                    Color(0.1, 0.5, 0.1)
                    Rectangle(
                        pos=(
                            pos_x * x + grs.x,
                            pos_y * y + grs.y),
                        size=(x, y))
            for thing in [thing for thing in self.environment.objects
                          if isinstance(thing, Stone)]:
                pos_x, pos_y = thing.location
                Color(1, 1, 1, 1)
                Rectangle(texture=self.stones.texture,
                          pos=(pos_x * x + grs.x,
                               pos_y * y + grs.y),
                          size=(x, y))
            for thing in [thing for thing in self.environment.objects if isinstance(thing, Agent_l.get(self.agent, Agent))]:
                pos_x, pos_y = thing.location
                if self.agent in Agent_l and \
                        isinstance(thing, Agent_l[self.agent]):
                    self.scoreA = thing.performance
                    labelA.text = self.get_scores()[0]
                    Color(1, 1, 1, 1)
                    Rectangle(texture=self.agentImg.texture,
                              pos=(pos_x * x + grs.x,
                                   pos_y * y + grs.y),
                              size=(x, y))

    def load_environment(self, labels, wid, *largs):
        self.run_game = False
        self.state_num = 0
        if self.map is None or self.map == "Maps":
            gen_popup("Error!", "No map selected...").open()
            return
        elif self.agent not in Agent_l:
            gen_popup("Error!", "You must choose at least one agent...").open()
            return
        self.__initialize_env()
        self.initialized = True
        self.update_canvas(labels, wid)

    def steps_ex(self, labels, wid, n_step=None):
        if self.environment is not None:
            if n_step is not None:
                if self.state_num == n_step:
                    self.run_game = False
                    self.state_num = 0
                    return False
                else:
                    self.state_num += 1
            if not self.run_game:
                return False
            self.environment.step()
            self.update_canvas(labels, wid)

    def run_btn(self, function, labels, wid, *largs):
        if not self.initialized:
            gen_popup("Error!", "You must load a map...").open()
            self.btn_run.state = "normal"
            return
        elif self.agent == "Agent A":
            popup = gen_popup(
                "Error!", "Agent not selected, reset required...", False).open()
            Clock.schedule_once(popup.dismiss, timeout=2)
            Clock.schedule_once(self.partial_reset, timeout=2)
        self.btn_run.state = "down"
        self.run_game = True
        Clock.schedule_interval(partial(function, labels, wid), 1 / 30.)

    def reload_agents(self, labels, spinners, wid, *largs):
        self.run_game = False
        self.state_num = 0
        self.Count_Steps = 0
        labelA = labels
        labelA.text = self.get_scores()[0]
        global Agent_l
        global map_l
        Agent_l = search_list.load_agents()
        map_l = maps.get_maps()
        spinnerA, spinnerMap = spinners
        spinnerA.values = sorted(
            [agent for agent in list(Agent_l.keys())]) + ["Agent A"]
        spinnerMap.values = sorted(
            [map for map in list(map_l.keys())]) + ["Maps"]
        self.counter.text = str(self.state_num)
        self.__initialize_env()
        self.initialized = True
        self.update_canvas(labels, wid)

    def on_resize(self, width, eight):
        self.update_canvas()

    def select_agent_A(self, spinner, text):
        self.agent = text

    def select_map(self, spinner, text):
        self.map = text

    def build(self):
        wid = Widget()

        self.counter = Label(text="0")
        labelA = Label(text=self.get_scores()[0])
        labelB = Label(text=self.get_scores()[1])
        labels = (labelA, labelB)
        self.labels = labels
        self.wid = wid
        tmp_agents = list(sorted([agent for agent in list(Agent_l.keys())]))
        agentA_spinner = Spinner(text='Agent A', text_size=(95, None), shorten=True,
            values=tmp_agents + ["Agent A"]
        )
        maps_spinner = Spinner(text='Maps', text_size=(95, None), shorten=True,
            values=list(sorted([map for map in list(map_l.keys())])) + ["Maps"]
        )
        agentA_spinner.bind(text=self.select_agent_A)
        maps_spinner.bind(text=self.select_map)
        btn_load = Button(text='Load', on_press=partial(self.load_environment, labels, wid))
        self.btn_run = ToggleButton(text='Run >>', on_press=partial(self.run_btn, self.steps_ex, labels, wid))
        Window.bind(on_resize=self.on_resize)
        action_layout = BoxLayout(size_hint=(1, None), height=50)
        action_layout.add_widget(btn_load)
        action_layout.add_widget(self.counter)
        action_layout.add_widget(self.btn_run)
        agents_layout = BoxLayout(size_hint=(1, None), height=50)
        agents_layout.add_widget(agentA_spinner)
        agents_layout.add_widget(maps_spinner)
        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(action_layout)
        root.add_widget(agents_layout)
        return root


def check_img(img_name):
    return path.isfile(path.join("agents_dir", path.join("img", img_name)))


def gen_popup(type_, text, dismiss=True):
    popup_layout = BoxLayout(orientation='vertical')
    content = Button(text='Dismiss', size_hint=(1, .3))
    popup_layout.add_widget(Label(text=text))
    popup = Popup(title=type_,
                  content=popup_layout)
    if dismiss:
        popup_layout.add_widget(content)
        content.bind(on_press=popup.dismiss)
    return popup


if __name__ == '__main__':
    GrassingCuttingAgent().run()
