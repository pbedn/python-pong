import random

import pyglet
from pyglet.window import FPSDisplay, key
from pyglet.gl import glBegin, glVertex2f, glEnd, GL_QUADS
from pyglet.gl import glLineStipple, glEnable, glLineWidth, GL_LINE_STIPPLE, GL_LINES


class Drawing:
    def __init__(self, width, height, keys, ai=False):
        self.window_width = width
        self.window_height = height
        self.keys = keys
        self.scale_factor = (self.window_width + self.window_height) // 2
        self.computer_player = ai

    @staticmethod
    def draw_rect(x, y, width, height):
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    @staticmethod
    def draw_line(x1, y1, x2, y2, width=2):
        glLineStipple(1, 0xFF)
        glEnable(GL_LINE_STIPPLE)
        glLineWidth(width)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()


class Paddle(Drawing):
    def __init__(self, side, *args):
        super().__init__(*args)
        self.side = side
        self.width = self.window_width // 57
        self.height = self.window_height // 8
        self.speed = self.scale_factor // 80

        if self.side == 'left':
            self.x = self.window_width // 10
            self.y = self.window_height // 2 - self.height // 2
        elif self.side == 'right':
            self.x = self.window_width - self.width - self.window_width // 10
            self.y = self.window_height // 2 - self.height // 2

    def draw(self):
        self.draw_rect(self.x, self.y, self.width, self.height)

    def check_collisions(self, ball):
        # check for collisions of ball with paddle

        if (self.x < ball.x < self.x + self.width and
                self.y < ball.y < self.y + self.height):
            # set fly direction depending on where it hit the paddle
            # (t is 0.5 if hit at top, 0 at center, -0.5 at bottom)
            t = ((ball.y - self.y) / self.height) - 0.5
            if self.side == 'left':
                ball.ball_dir_x = abs(ball.ball_dir_x)  # force it to be positive
            elif self.side == 'right':
                ball.ball_dir_x = -abs(ball.ball_dir_x)  # force it to be negative
            ball.ball_dir_y = t
            ball.ball_speed += 0.5

    def ai_player(self, ball):
        if ball.ball_dir_x == 1:
            if (self.y + self.height / 2) < self.window_height // 2 - self.height / 2:
                self.y += self.speed
            elif (self.y + self.height / 2) > self.window_height // 2 + self.height / 2:
                self.y -= self.speed
        elif ball.ball_dir_x == -1:
            if (self.y + self.height / 2) < ball.y - self.height / 2:
                self.y += self.speed
            elif (self.y + self.height / 2) > ball.y + self.height / 2:
                self.y -= self.speed

    def update(self, ball):
        if self.side == 'left':
            if not self.computer_player:
                if self.keys[key.W]:
                    self.y += self.speed
                if self.keys[key.S]:
                    self.y -= self.speed
            else:
                self.ai_player(ball)

        if self.side == 'right':
            if self.keys[key.UP]:
                self.y += self.speed
            if self.keys[key.DOWN]:
                self.y -= self.speed

        self.check_collisions(ball)


class Ball(Drawing):
    def __init__(self, *args):
        super().__init__(*args)
        self.x = self.window_width // 2
        self.y = self.window_height // 2
        self.ball_dir_x = random.choice([-1, 1])
        self.ball_dir_y = 0.0
        self.ball_size = self.scale_factor // 57
        self.ball_speed = self.scale_factor // 80

    def draw(self):
        self.draw_rect(self.x - self.ball_size / 2,
                       self.y - self.ball_size / 2,
                       self.ball_size,
                       self.ball_size)

    def check_collisions(self):
        # check for left wall collision
        if self.x < 0:
            self.x = self.window_width / 2
            self.y = self.window_height / 2
            self.ball_dir_x = abs(self.ball_dir_x)  # force it to be positive
            self.ball_dir_y = 0

        # check for right wall collision
        if self.x > self.window_width:
            self.x = self.window_width / 2
            self.y = self.window_height / 2
            self.ball_dir_x = -abs(self.ball_dir_x)  # force it to be negative
            self.ball_dir_y = 0

        # check for top wall collision
        if self.y > self.window_height:
            self.ball_dir_y = -abs(self.ball_dir_y)  # force it to be negative

        # check for bottom wall collision
        if self.y < 0:
            self.ball_dir_y = abs(self.ball_dir_y)  # force it to be positive

    def update(self):
        self.x += self.ball_dir_x * self.ball_speed
        self.y += self.ball_dir_y * self.ball_speed
        self.check_collisions()


class Line(Drawing):
    def __init__(self, *args):
        super().__init__(*args)
        self.x1 = self.window_width // 2
        self.y1 = 0.0
        self.x2 = self.window_width // 2
        self.y2 = self.window_height
        self.line_width = 2

    def draw(self):
        self.draw_line(self.x1, self.y1,
                       self.x2, self.y2,
                       self.line_width)


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_location(100, 100)
        self.set_caption('Pong')
        self.set_mouse_visible(False)
        self.frame_rate = 1/60.

        self.fps_display = FPSDisplay(self)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.ai = True

        self.paddle_left = Paddle('left', self.width, self.height, self.keys, self.ai)
        self.paddle_right = Paddle('right', self.width, self.height, self.keys)
        self.ball = Ball(self.width, self.height, self.keys)
        self.line = Line(self.width, self.height, self.keys)

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.paddle_left.draw()
        self.paddle_right.draw()
        self.ball.draw()
        self.line.draw()

    def update(self, dt):
        self.ball.update()
        self.paddle_left.update(self.ball)
        self.paddle_right.update(self.ball)


if __name__ == '__main__':
    game = Game(width=800, height=600, resizable=True)
    pyglet.clock.schedule_interval(game.update, game.frame_rate)
    pyglet.app.run()
