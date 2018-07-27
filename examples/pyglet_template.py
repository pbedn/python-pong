import pyglet
from pyglet.window import FPSDisplay


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.frame_rate = 1/60.0
        self.fps_display = FPSDisplay(self)

    def on_draw(self):
        self.clear()

        self.fps_display.draw()

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = GameWindow(width=800, height=600, caption="Title", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
