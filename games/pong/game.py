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


if __name__ == '__main__':
    pyglet.app.run()
