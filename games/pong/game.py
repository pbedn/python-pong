import pyglet


# Setup Window
window = pyglet.window.Window(width=800, height=600)
window.set_caption('Pong')
window.set_mouse_visible(False)


fps_display = pyglet.clock.ClockDisplay()


@window.event
def on_draw():
    window.clear()
    fps_display.draw()


def update(dt):
    pass


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.app.run()
