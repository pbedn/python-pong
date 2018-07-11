import random
from math import sqrt

import pyglet
from pyglet.window import key
from pyglet.gl import *


# Setup Window
window = pyglet.window.Window(width=800, height=600)
window.set_caption('Pong')
window.set_mouse_visible(False)

WINDOW_WIDTH_HALF = window.width // 2
WINDOW_HEIGHT_HALF = window.height // 2


fps_display = pyglet.clock.ClockDisplay()

main_batch = pyglet.graphics.Batch()

keys = key.KeyStateHandler()
window.push_handlers(keys)

score_left = pyglet.text.Label("0", font_name='Arial', font_size=window.width//11,
                          x=window.width//2-window.width//10, y=window.height-window.height//10,
                          anchor_x='center', anchor_y='center', batch=main_batch)


score_right = pyglet.text.Label("0", font_name='Arial', font_size=window.width//11,
                          x=window.width//2+window.width//10, y=window.height-window.height//10,
                          anchor_x='center', anchor_y='center', batch=main_batch)


def init(new_game):
    global paddle_left_x, paddle_left_y, paddle_right_x, paddle_right_y
    global ball_pos_x, ball_pos_y, ball_dir_x, ball_dir_y
    global paddle_width, paddle_height, paddle_speed
    global ball_size, ball_speed
    global score_player_left, score_player_right

    if new_game:
        score_player_left = 0
        score_player_right = 0
        score_left.text = str(score_player_left)
        score_right.text = str(score_player_right)

    # paddles in general
    paddle_width = window.width // 57
    paddle_height = window.height // 8
    paddle_speed = 9

    # left paddle position
    paddle_left_x = window.width // 10
    paddle_left_y = WINDOW_HEIGHT_HALF - paddle_height // 2

    # right paddle position
    paddle_right_x = window.width - paddle_width - window.width // 10
    paddle_right_y = WINDOW_HEIGHT_HALF - paddle_height // 2

    ball_pos_x = WINDOW_WIDTH_HALF
    ball_pos_y = WINDOW_HEIGHT_HALF
    ball_dir_x = random.choice([-1, 1])
    ball_dir_y = 0.0
    ball_size = 12
    ball_speed = 8


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


def ai_player(ball_direction_x, ball_position_y, paddle_y):
    # center the paddle when ball is moving away
    if ball_direction_x == 1:
        if (paddle_y + paddle_height / 2) < WINDOW_HEIGHT_HALF - paddle_height / 2:
            paddle_y += paddle_speed
        elif (paddle_y + paddle_height / 2) > WINDOW_HEIGHT_HALF + paddle_height / 2:
            paddle_y -= paddle_speed
    elif ball_direction_x == -1:
        if (paddle_y + paddle_height / 2) < ball_position_y - paddle_height / 2:
            paddle_y += paddle_speed
        elif (paddle_y + paddle_height / 2) > ball_position_y + paddle_height / 2:
            paddle_y -= paddle_speed
    return paddle_y


@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    main_batch.draw()

    # Draw Paddles
    draw_rect(paddle_left_x, paddle_left_y, paddle_width, paddle_height)
    draw_rect(paddle_right_x, paddle_right_y, paddle_width, paddle_height)

    # Draw Ball
    draw_rect(ball_pos_x - ball_size / 2, ball_pos_y - ball_size / 2, ball_size, ball_size)

    # Draw Line
    draw_line(WINDOW_WIDTH_HALF, 0.0, WINDOW_WIDTH_HALF, window.height)


def vec2_norm(x: int, y: float):
    global ball_dir_x, ball_dir_y
    # sets a vectors length to 1 (which means that x + y == 1)
    length = sqrt((x * x) + (y * y))
    if length != 1.0:
        length = 1.0 / length
        x *= length
        y *= length
    ball_dir_y = x
    ball_dir_y = y


def update(dt):
    global score_player_left, score_player_right
    global ball_pos_x, ball_pos_y, ball_dir_x, ball_dir_y
    global paddle_left_x, paddle_left_y, paddle_right_x, paddle_right_y
    global paddle_speed, ball_speed, ball_size
    global paddle_width, paddle_height

    if not computer_player:
        if keys[key.W]:
            paddle_left_y += paddle_speed
        if keys[key.S]:
            paddle_left_y -= paddle_speed
    else:
        paddle_left_y = ai_player(ball_dir_x, ball_pos_y, paddle_left_y)

    if keys[key.UP]:
        paddle_right_y += paddle_speed
    if keys[key.DOWN]:
        paddle_right_y -= paddle_speed

    # fly the ball
    ball_pos_x += ball_dir_x * ball_speed
    ball_pos_y += ball_dir_y * ball_speed

    # check for collisions of ball with left paddle
    if (paddle_left_x < ball_pos_x < paddle_left_x + paddle_width and
       paddle_left_y < ball_pos_y < paddle_left_y + paddle_height):
        # set fly direction depending on where it hit the paddle
        # (t is 0.5 if hit at top, 0 at center, -0.5 at bottom)
        t = ((ball_pos_y - paddle_left_y) / paddle_height) - 0.5
        ball_dir_x = abs(ball_dir_x)  # force it to be positive
        ball_dir_y = t

        ball_speed += 0.5

    # check for collisions of ball with right paddle
    # TODO: sometimes ball fly through paddle (higher speed)
    if (paddle_right_x < ball_pos_x < paddle_right_x + paddle_width and
       paddle_right_y < ball_pos_y < paddle_right_y + paddle_height):
        # set fly direction depending on where it hit the paddle
        # (t is 0.5 if hit at top, 0 at center, -0.5 at bottom)
        t = ((ball_pos_y - paddle_right_y) / paddle_height) - 0.5
        ball_dir_x = -abs(ball_dir_x)  # force it to be negative
        ball_dir_y = t

        ball_speed += 0.5

    # check for left wall collision
    if ball_pos_x < 0:
        score_player_right += 1
        score_right.text = str(score_player_right)
        ball_pos_x = window.width / 2
        ball_pos_y = window.height / 2
        ball_dir_x = abs(ball_dir_x)  # force it to be positive
        ball_dir_y = 0
        init(new_game=False)

    # check for right wall collision
    if ball_pos_x > window.width:
        score_player_left += 1
        score_left.text = str(score_player_left)
        ball_pos_x = window.width / 2
        ball_pos_y = window.height / 2
        ball_dir_x = -abs(ball_dir_x)  # force it to be negative
        ball_dir_y = 0
        init(new_game=False)

    # check for top wall collision
    if ball_pos_y > window.height:
        ball_dir_y = -abs(ball_dir_y)  # force it to be negative

    # check for bottom wall collision
    if ball_pos_y < 0:
        ball_dir_y = abs(ball_dir_y)  # force it to be positive

    # normalize ball_dir_y
    # TODO: Research that in more detail
    vec2_norm(ball_dir_x, ball_dir_y)


if __name__ == '__main__':
    computer_player = True
    init(new_game=True)
    pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.app.run()
