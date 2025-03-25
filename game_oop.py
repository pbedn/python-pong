import random
from math import sqrt 

import pyglet
from pyglet import shapes
from pyglet.window import FPSDisplay, key


class Sounds:
    def __init__(self):
        import sys
        if sys.platform == "linux":
            pyglet.options['audio'] = ('openal', 'pulse', 'silent')
        else:
            pyglet.options['audio'] = ('openal', 'directsound', 'silent')

        pyglet.resource.path = ['res/sounds']
        pyglet.resource.reindex()

        self.beep = pyglet.resource.media('ping_pong_8bit_beeep.ogg', streaming=False)
        self.peep = pyglet.resource.media('ping_pong_8bit_peeeeeep.ogg', streaming=False)
        self.plop = pyglet.resource.media('ping_pong_8bit_plop.ogg', streaming=False)


class Drawing:
    def __init__(self, width, height, keys=None, ai=False):
        self.window_width = width
        self.window_height = height
        self.keys = keys
        self.scale_factor = (self.window_width + self.window_height) // 2
        self.computer_player = ai

    @staticmethod
    def draw_rect(x, y, width, height, color=(255, 255, 255)):
        rectangle = shapes.Rectangle(x, y, width, height, color=color)
        rectangle.draw()

    @staticmethod
    def draw_line(x1, y1, x2, y2):
        line = shapes.Line(x1, y1, x2, y2)
        line.draw()


class Paddle(Drawing):
    def __init__(self, side, sounds, *args):
        super().__init__(*args)
        self.side = side
        self.width = self.window_width // 57
        self.height = self.window_height // 8
        self.speed = self.scale_factor // 80
        self.sound = sounds

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
            if self.sound: self.sound.plop.play()

    def ai_player(self, ball, game_difficulty):
        if game_difficulty == 'normal' and random.random() > 0.5:
            pass
        else:
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

    def update(self, ball, game_difficulty=None):
        if self.side == 'left':
            if not self.computer_player:
                if self.keys[key.W]:
                    self.y += self.speed
                if self.keys[key.S]:
                    self.y -= self.speed
            else:
                self.ai_player(ball, game_difficulty)

        if self.side == 'right':
            if self.keys[key.UP]:
                self.y += self.speed
            if self.keys[key.DOWN]:
                self.y -= self.speed

        self.check_collisions(ball)


class Ball(Drawing):
    def __init__(self, sounds=None, *args):
        super().__init__(*args)
        self.reset()
        self.sound = sounds

    def reset(self):
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

    def check_collisions(self, scores):
        # check for left wall collision
        if self.x < 0:
            self.x = self.window_width / 2
            self.y = self.window_height / 2
            self.ball_dir_x = abs(self.ball_dir_x)  # force it to be positive
            self.ball_dir_y = 0
            scores[0]['right'] += 1
            scores[2].label.text = str(scores[0]['right'])
            if self.sound: self.sound.peep.play()
            self.reset()

        # check for right wall collision
        if self.x > self.window_width:
            self.x = self.window_width / 2
            self.y = self.window_height / 2
            self.ball_dir_x = -abs(self.ball_dir_x)  # force it to be negative
            self.ball_dir_y = 0
            scores[0]['left'] += 1
            scores[1].label.text = str(scores[0]['left'])
            if self.sound: self.sound.peep.play()
            self.reset()

        # check for top wall collision
        if self.y > self.window_height:
            self.ball_dir_y = -abs(self.ball_dir_y)  # force it to be negative
            if self.sound: self.sound.beep.play()

        # check for bottom wall collision
        if self.y < 0:
            self.ball_dir_y = abs(self.ball_dir_y)  # force it to be positive
            if self.sound: self.sound.beep.play()

    def vec2_norm(self, x: int, y: float):
        global ball_dir_x, ball_dir_y
        # sets a vectors length to 1 (which means that x + y == 1)
        length = sqrt((x * x) + (y * y))
        if length != 1.0:
            length = 1.0 / length
            x *= length
            y *= length
        ball_dir_y = x
        ball_dir_y = y

    def update(self, scores):
        self.x += self.ball_dir_x * self.ball_speed
        self.y += self.ball_dir_y * self.ball_speed
        self.check_collisions(scores)
        self.vec2_norm(self.x, self.y)


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
                       self.x2, self.y2)


class Score():
    def __init__(self, side, window_width, window_height, text, batch, *args):
        super().__init__(*args)
        self.label = pyglet.text.Label()
        self.label.font_name = 'Arial'
        self.label.anchor_x = 'center'
        self.label.anchor_y = 'center'
        self.label.batch = batch
        self.label.text = text
        self.label.font_size = window_width//11
        if side == 'left':
            self.label.x = window_width // 2 - window_width // 10
            self.label.y = window_height - window_height // 10
        elif side == 'right':
            self.label.x = window_width // 2 + window_width // 10
            self.label.y = window_height - window_height // 10

    def reset(self):
        self.label.text = '0'


class MenuItem():
    def __init__(self, window_width, window_height, text, modifier, *args):
        super().__init__(*args)
        self.label = pyglet.text.Label()
        self.label.font_name = 'Arial'
        self.label.anchor_x = 'center'
        self.label.anchor_y = 'center'
        self.label.text = text
        self.label.font_size = (window_width + window_height) // 26
        self.label.x = window_width // 2
        self.label.y = window_height - modifier * window_height // 10

    def reset(self):
        self.label.text = '0'

    def draw(self):
        self.label.draw()


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_location(100, 100)
        self.set_caption('Pong')
        self.set_mouse_visible(False)
        self.frame_rate = 1/60.
        self.fps_display = FPSDisplay(self)
        self.keys = key.KeyStateHandler()

        self.main_batch = pyglet.graphics.Batch()

        self.ai = True

        self.play_sounds = True
        if self.play_sounds:
            self.sounds = Sounds()

        self.paddle_left = Paddle('left', self.sounds, self.width, self.height, self.keys, self.ai)
        self.paddle_right = Paddle('right', self.sounds, self.width, self.height, self.keys)
        self.ball = Ball(self.sounds, self.width, self.height, self.keys)
        self.line = Line(self.width, self.height, self.keys)

        self.score_left = Score('left', self.width, self.height, '0', batch=self.main_batch)
        self.score_right = Score('right', self.width, self.height, '0', batch=self.main_batch)
        score = {'left': 0, 'right': 0}
        self.scores = [score, self.score_left, self.score_right]

        self.game_menu = True
        self.start_game = MenuItem(self.width, self.height, "Start Game", modifier=2)
        self.start_game.bold = True
        self.difficulty = MenuItem(self.width, self.height, "Difficulty: ", modifier=4)
        self.game_difficulty = 'normal'
        self.difficulty.label.text += self.game_difficulty
        self.exit_game = MenuItem(self.width, self.height, "Exit Game", modifier=6)
        self.menu_items = [self.start_game, self.difficulty, self.exit_game]
        self.current_index = 0
        self.current_selection = self.menu_items[0].label

    def draw_menu(self):
        self.start_game.draw()
        self.difficulty.draw()
        self.exit_game.draw()

    def draw_game_objects(self):
        self.fps_display.draw()
        self.paddle_left.draw()
        self.paddle_right.draw()
        self.ball.draw()
        self.line.draw()
        # self.score_left.draw()
        # self.score_right.draw()

    def on_draw(self):
        self.clear()
        if self.game_menu:
            self.draw_menu()
        else:
            self.draw_game_objects()
            self.main_batch.draw()

    def choose_menu_item(self, symbol, modifier):
        if symbol == key.DOWN:
            self.current_selection.bold = False
            self.current_selection.font_size -= 10
            self.current_index += 1
            if self.current_index > 2:
                self.current_index = 0
            self.current_selection = self.menu_items[self.current_index].label
            self.current_selection.bold = True
            self.current_selection.font_size += 10
        elif symbol == key.UP:
            self.current_selection.bold = False
            self.current_selection.font_size -= 10
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = 2
            self.current_selection = self.menu_items[self.current_index].label
            self.current_selection.bold = True
            self.current_selection.font_size += 10
        elif self.current_index == 1 and symbol == key.RIGHT:
            self.game_difficulty = 'harder'
            self.current_selection.text = 'Difficulty: ' + self.game_difficulty
        elif self.current_index == 1 and symbol == key.LEFT:
            self.game_difficulty = 'normal'
            self.current_selection.text = 'Difficulty: ' + self.game_difficulty
        elif symbol == key.ENTER:
            if self.current_index == 0:
                self.game_menu = False
            elif self.current_index == 1:
                pass
            elif self.current_index == 2:
                pyglet.app.exit()

    def on_key_press(self, symbol, modifier):
        if self.game_menu:
            self.choose_menu_item(symbol, modifier)
        else:
            if self.keys[key.ESCAPE]:
                pyglet.app.exit()
            self.push_handlers(self.keys)

    def update(self, dt):
        if self.game_menu:
            pass
        else:
            self.ball.update(self.scores)
            self.paddle_left.update(self.ball, self.game_difficulty)
            self.paddle_right.update(self.ball)


if __name__ == '__main__':
    game = Game(width=800, height=600, resizable=True)
    pyglet.clock.schedule_interval(game.update, game.frame_rate)
    pyglet.app.run()
