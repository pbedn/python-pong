import pyglet
from pyglet.gl import *

# Global Variables
PADDLESIZE = 50
PADDLEOFFSET = 20
LINETHICKNESS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Setup Window
window = pyglet.window.Window(width=800, height=600)
window.set_caption('Pong')
window.set_mouse_visible(False)

WINDOW_WIDTH_HALF = window.width // 2
WINDOW_HEIGHT_HALF = window.height // 2


fps_display = pyglet.clock.ClockDisplay()


def init():
    global paddle_left_x, paddle_left_y, paddle_right_x, paddle_right_y
    global ball_pos_x, ball_pos_y
    global paddle_width, paddle_height
    global ball_size

    # paddles in general
    paddle_width = window.width // 57
    paddle_height = window.height // 8

    # left paddle position
    paddle_left_x = window.width // 10
    paddle_left_y = WINDOW_HEIGHT_HALF - paddle_height // 2

    # right paddle position
    paddle_right_x = window.width - paddle_width - window.width // 10
    paddle_right_y = WINDOW_HEIGHT_HALF - paddle_height // 2

    ball_pos_x = WINDOW_WIDTH_HALF
    ball_pos_y = WINDOW_HEIGHT_HALF
    ball_size = 12


def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


def draw_line(x1, y1, x2, y2, width=2):
    glLineStipple(1, 0xFF)
    glEnable(GL_LINE_STIPPLE)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


@window.event
def on_draw():
    window.clear()
    fps_display.draw()

    # Draw Paddles
    draw_rect(paddle_left_x, paddle_left_y, paddle_width, paddle_height)
    draw_rect(paddle_right_x, paddle_right_y, paddle_width, paddle_height)

    # Draw Ball
    draw_rect(ball_pos_x - ball_size / 2, ball_pos_y - ball_size / 2, ball_size, ball_size)

    # Draw Line
    draw_line(WINDOW_WIDTH_HALF, 0.0, WINDOW_WIDTH_HALF, window.height)


def update(dt):
    pass


if __name__ == '__main__':
    init()
    pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.app.run()
