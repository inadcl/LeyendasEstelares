class SceneManager:

    def __init__(self, initial_scene, next_scene):
        self.current_scene = initial_scene
        self.next_scene = next_scene

    def initScene(self, activeGameState):
        self.current_scene.initScene(activeGameState)

    def exitScene(self):
        self.current_scene.exitScene()

    def switch_to_scene(self, scene):
        self.current_scene = scene

    def process_input(self, events, pressed_keys, button):
        change_scene = self.current_scene.process_input(events, pressed_keys, button)
        if change_scene:
            self.current_scene = self.next_scene
            #self.next_scene = self.game_over


    def update(self):
        self.current_scene.update()

    def render(self, screen, activeGameState):
        self.current_scene.render(screen, activeGameState)
