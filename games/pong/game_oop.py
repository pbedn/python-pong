import pyglet
from pyglet.window import FPSDisplay


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_location(100, 100)
        self.set_caption('Pong')
        self.set_mouse_visible(False)
        self.frame_rate = 1/60.

        self.fps_display = FPSDisplay(self)

    def on_draw(self):
        self.clear()
        self.fps_display.draw()

    def update(self, dt):
        pass


if __name__ == '__main__':
    game = Game(width=800, height=600, resizable=True)
    pyglet.clock.schedule_interval(game.update, game.frame_rate)
    pyglet.app.run()
