

# All game sprites: Snake, Block, Apple, Rock, Hole
# golden apple - adding more rows - levels - fast zone
# 1) ghost power 2) press & portal

import pygame as pg
import random
from settings import *
vec = pg.math.Vector2


class Snake(pg.sprite.Sprite):

    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.Surface((SNAKE_WIDTH, SNAKE_HEIGHT))
        self.image_orig = image
        self.image = image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.circle_radius = SNAKE_PIXEL_SIZE // 2
        self.radius = SNAKE_PIXEL_SIZE * 0.4
        #pg.draw.circle(self.image, WHITE, self.rect.center, self.circle_radius)
        self.rect.topleft = INITIAL_POS

        self.pos = vec(COLUMNS // 2, ROWS // 2)


        self.vel = vec(0,0)
        self.next = vec(0,0)

    def update(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.next = vec(-SNAKE_SPEED, 0)
        if keys[pg.K_RIGHT]:
            self.next = vec(SNAKE_SPEED, 0)
        if keys[pg.K_UP]:
            self.next = vec(0, -SNAKE_SPEED)
        if keys[pg.K_DOWN]:
            self.next = vec(0, SNAKE_SPEED)
        if keys[pg.K_SPACE]:
            self.next = vec(0, 0)

        if self.rect.left % SNAKE_WIDTH == 0 and self.rect.top % SNAKE_HEIGHT == 0 and self.next + self.vel != vec(0, 0):
            self.vel = self.next

        self.rect.left += self.vel.x
        self.rect.top += self.vel.y

        if not DIE_ON_EDGE:
            if self.rect.centerx < 0 + W_ADJUST:
                self.rect.centerx = WIDTH + W_ADJUST
            if self.rect.centerx > WIDTH + W_ADJUST:
                self.rect.centerx = 0 + W_ADJUST
            if self.rect.centery < 0 + H_ADJUST:
                self.rect.centery = HEIGHT + H_ADJUST
            if self.rect.centery > HEIGHT + H_ADJUST:
                self.rect.centery = 0 + H_ADJUST

        self.pos = vec(self.rect.x // (WIDTH // COLUMNS), self.rect.y // (HEIGHT // ROWS))
        self.update_image()

    def update_image(self):
        if self.vel.x > 0:
            self.image = pg.transform.rotate(self.image_orig, 90)
        if self.vel.x < 0:
            self.image = pg.transform.rotate(self.image_orig, -90)
        if self.vel.y > 0:
            self.image = self.image_orig
        if self.vel.y < 0:
            self.image = pg.transform.rotate(self.image_orig, 180)

class Block(pg.sprite.Sprite):

    def __init__(self, previous, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        #self.image.fill(WHITE)
        self.previous = previous
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.radius = SNAKE_PIXEL_SIZE // 2
        #pg.draw.circle(self.image, WHITE, self.rect.center, self.radius)

        self.objectives = []
        self.waiting = 0

        self.vel = self.previous.vel
        self.rect.x = self.previous.rect.x
        self.rect.y = self.previous.rect.y

        self.pos = vec(self.rect.x // (WIDTH // COLUMNS), self.rect.y // (HEIGHT // ROWS))

    def update(self):
        self.vel = self.previous.vel

        if 0 <= self.waiting < SNAKE_PIXEL_SIZE//SNAKE_SPEED + SEP_CHOICE:
            self.waiting += 1
            self.objectives.append(vec(self.previous.rect.x, self.previous.rect.y))
            return
        self.waiting = -1
        if self.vel != vec(0, 0):

            self.objectives.append(vec(self.previous.rect.x, self.previous.rect.y))
            next = self.objectives.pop(0)
            self.rect.x = next.x
            self.rect.y = next.y

            self.pos = vec(self.rect.x // (WIDTH // COLUMNS), self.rect.y // (HEIGHT // ROWS))


class Apple(pg.sprite.Sprite):

    def __init__(self, image, *group_rects):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = image
        self.image = self.image_orig
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.radius = APPLE_HEIGHT * 0.3
        self.circle_radius = SNAKE_PIXEL_SIZE // 2
        #pg.draw.circle(self.image, RED, self.rect.center, self.circle_radius)

        self.group_rects = group_rects
        self.move()
        self.time = None
        self.eating = False
        self.value = APPLE_VALUE
        self.angle = 0

    def move(self):
        occupied = True
        count = 0
        while occupied:
            count += 1
            occupied = False
            x = random.choice(range(0, WIDTH, APPLE_WIDTH))
            y = random.choice(range(0, HEIGHT, APPLE_HEIGHT))

            if (x, y) == INITIAL_POS:
                occupied = True

            for a in self.group_rects:
                self.rect.topleft = (x, y)
                hits = pg.sprite.spritecollide(self, a, False)
                if hits:
                    occupied = True

            if count > ROWS*COLUMNS:
                return False
        self.rect.topleft = (x, y)
        self.pos = vec(self.rect.x // (WIDTH // COLUMNS), self.rect.y // (HEIGHT // ROWS))
        return True

    def update(self):
        self.angle = (self.angle + 2) % 360
        center = self.rect.center
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = center


class Rock(pg.sprite.Sprite):

    def __init__(self, row, col, image, *group_rects):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((ROCK_WIDTH, ROCK_HEIGHT))
        self.image = image
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)

        self.group_rects = group_rects
        self.rect.top = row * ROCK_HEIGHT
        self.rect.left = col * ROCK_WIDTH
        # self.move()

    def move(self):
        occupied = True
        count = 0
        while occupied:
            count += 1
            occupied = False
            x = random.choice(range(0, WIDTH, APPLE_WIDTH))
            y = random.choice(range(0, HEIGHT, APPLE_HEIGHT))

            if (x, y) == INITIAL_POS:
                occupied = True

            for a in self.group_rects:
                self.rect.topleft = (x, y)
                hits = pg.sprite.spritecollide(self, a, False)
                if hits:
                    occupied = True

            if count > ROWS*COLUMNS:
                return False
        self.rect.topleft = (x, y)
        self.pos = vec(self.rect.x // (WIDTH // COLUMNS), self.rect.y // (HEIGHT // ROWS))
        return True

    def update(self):
        pass


class Gate(pg.sprite.Sprite):

    def __init__(self, image, *group_rects, other=None):
        pg.sprite.Sprite.__init__(self, image)
        self.image = pg.Surface((GATE_WIDTH, GATE_HEIGHT))
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.radius = GATE_HEIGHT * 0.1
        self.circle_radius = SNAKE_PIXEL_SIZE // 2
        pg.draw.circle(self.image, BROWN, self.rect.center, self.circle_radius)

        self.group_rects = group_rects
        self.exiting = False
        self.other = other
        self.move()

    def move(self):
        occupied = True
        count = 0
        while occupied:
            count += 1
            occupied = False
            x = random.choice(range(0, WIDTH, APPLE_WIDTH))
            y = random.choice(range(0, HEIGHT, APPLE_HEIGHT))

            if (x, y) == INITIAL_POS:
                occupied = True

            for a in self.group_rects:
                self.rect.topleft = (x, y)
                hits = pg.sprite.spritecollide(self, a, False)
                if hits:
                    occupied = True

            if count > ROWS*COLUMNS:
                return False
        self.rect.topleft = (x, y)
        self.pos = vec(self.rect.x // (WIDTH // COLUMNS), self.rect.y // (HEIGHT // ROWS))
        return True

    def add(self, other):
        self.other = other

    def update(self):
        pass


class Portal(object):

    def __init__(self, image, *group_rects):

        self.gate_1 = Gate(group_rects)
        self.gate_1.image = image
        self.gate_1.image.set_colorkey(WHITE)
        center = self.gate_1.rect.center
        self.gate_1.rect = self.gate_1.image.get_rect()
        self.gate_1.rect.center = center

        self.gate_2 = Gate(group_rects, other=self.gate_1)
        self.gate_2.image = image
        self.gate_2.image.set_colorkey(WHITE)
        center = self.gate_2.rect.center
        self.gate_2.rect = self.gate_2.image.get_rect()
        self.gate_2.rect.center = center
        self.gate_1.add(self.gate_2)

    def update(self):
        pass


class InputBox(pg.sprite.Sprite):

    def __init__(self, instructions, valid, size, color, x, y):
        pg.sprite.Sprite.__init__(self)
        self.font_name = pg.font.match_font(FONT_NAME)
        self.font = pg.font.Font(self.font_name, size)
        self.valid = valid
        self.text = ""
        self.color = color

        self.image = self.font.render(instructions, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.active = False

    def write(self, text):
        if text in self.valid:
            self.text += text
            print(text)
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos


class AI(object):
    def __init__(self, snake, body, obstacles):
        self.snake = snake
        self.current = self.snake.rect.center
        self.body = body

    def update(self, apple):
        self.objective = apple.rect.center
        self.current = self.snake.rect.center
        self.x_distance = (self.objective[0] - self.current[0]) // SNAKE_WIDTH
        self.y_distance = (self.objective[1] - self.current[1]) // SNAKE_HEIGHT

        self.can_go_up = True
        self.can_go_down = True
        self.can_go_right = True
        self.can_go_left = True

        self.next = vec(0, 0)

        for element in self.body:
            if self.snake.pos + vec(1, 0) == element.pos:
                self.can_go_right = False
            if self.snake.pos + vec(-1, 0) == element.pos:
                self.can_go_left = False
            if self.snake.pos + vec(0, 1) == element.pos:
                self.can_go_down = False
            if self.snake.pos + vec(0, -1) == element.pos:
                self.can_go_up = False

        if abs(self.x_distance) >= abs(self.y_distance) or self.snake.vel.y:
            if self.x_distance < 0 and self.can_go_left:
                self.next= vec(-SNAKE_SPEED, 0)
            if self.x_distance > 0 and self.can_go_right:
                self.next= vec(SNAKE_SPEED, 0)

        if abs(self.y_distance) > abs(self.x_distance) or self.snake.vel.x:
            if self.y_distance < 0 and self.can_go_up:
                self.next= vec(0, -SNAKE_SPEED)
            if self.y_distance > 0 and self.can_go_down:
                self.next= vec(0, SNAKE_SPEED)

        if self.next == vec(0,0):
            self.next.x = -self.snake.vel.y
            self.next.y = self.snake.vel.x

        self.snake.next = self.next
