class SceneManager:
    def __init__(self, initial_scene):
        self.current_scene = initial_scene

    def initScene(self):
        self.current_scene.initScene()

    def exitScene(self):
        self.current_scene.exitScene()

    def switch_to_scene(self, scene):
        self.current_scene = scene

    def process_input(self, events, pressed_keys, button):
        self.current_scene.process_input(events, pressed_keys, button)

    def update(self):
        self.current_scene.update()

    def render(self, screen):
        self.current_scene.render(screen)
