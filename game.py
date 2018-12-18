
# class game contains the game logic to:
# - generate the pygame window
# - generate a new instance of the game
# - listen to events, update all sprites and update the display
# - store highscore in a text file and read it later - currently not working

import pygame as pg
import random
from os import path, environ
from settings import *
from sprites import *


class Game():

    def __init__(self):
        # initialize game window, etc
        environ['SDL_VIDEO_CENTERED'] = '1'
        # pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "img")
        try:
            with open(path.join(self.dir, HS_FILE), 'r') as f:
                try:
                    self.highscore = int(f.read())
                except:
                    self.highscore = 0
        except:
            self.highscore = 0

        if HEIGHT % SNAKE_HEIGHT != 0 or WIDTH % SNAKE_WIDTH != 0 or SNAKE_HEIGHT % SNAKE_SPEED != 0 or SNAKE_WIDTH % SNAKE_SPEED != 0:
            self.screen.fill(BLACK)
            self.draw_text("Settings ERROR", 22, RED, WIDTH / 2, HEIGHT/4)
            self.draw_text("The following numbers should be ints: ", 22, RED, WIDTH / 2, HEIGHT *3/ 8 )
            self.draw_text("HEIGHT / SNAKE_HEIGHT, WIDTH / SNAKE_WIDTH,", 20, RED, WIDTH / 2, HEIGHT / 2 )
            self.draw_text("SNAKE_HEIGHT / SNAKE_SPEED, SNAKE_WIDTH / SNAKE_SPEED", 20, RED, WIDTH / 2, HEIGHT /2 +50)
            pg.display.flip()
            self.wait_for_key()

        self.background_orig = pg.image.load(path.join(self.img_dir, "black-background.jpg")).convert()
        self.background = pg.transform.scale(self.background_orig, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()

        self.snake_head = pg.image.load(path.join(self.img_dir, "alien_face.png")).convert()
        self.snake_head = pg.transform.scale(self.snake_head, (SNAKE_WIDTH, SNAKE_HEIGHT))

        self.body_image = pg.image.load(path.join(self.img_dir, "facebook_body.png")).convert()
        self.body_image = pg.transform.scale(self.body_image, (BLOCK_WIDTH , BLOCK_HEIGHT))

        self.portal_image = pg.image.load(path.join(self.img_dir, "portal_purple.png")).convert()
        self.portal_image = pg.transform.scale(self.portal_image, (GATE_WIDTH*2, GATE_HEIGHT*2))

        self.apple_image = pg.image.load(path.join(self.img_dir, "true_apple.png")).convert()
        self.apple_image = pg.transform.scale(self.apple_image, (APPLE_WIDTH, APPLE_HEIGHT))

        self.rock_image = pg.image.load(path.join(self.img_dir, "castleCenter_rounded.png")).convert()
        self.rock_image = pg.transform.scale(self.rock_image, (ROCK_WIDTH, ROCK_HEIGHT))

        # self.spritesheet = Spriteheet(path.join(self.img_dir, SPRITESHEET))

    def new(self):
        # Start a new game
        self.score = 0
        self.won = False
        self.all_sprites = pg.sprite.Group()
        self.body = pg.sprite.Group()
        self.snake_g = pg.sprite.Group()
        self.apples = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.portals = pg.sprite.Group()

        if not AI_on:

            for pos in ROCK_POSITIONS:
                rock = Rock(pos[0], pos[1], self.rock_image, self.all_sprites)
                self.obstacles.add(rock)
                self.all_sprites.add(rock)
            #
            self.portal = Portal(self.portal_image, self.all_sprites)
            self.portals.add(self.portal.gate_1)
            self.portals.add(self.portal.gate_2)
            self.all_sprites.add(self.portal.gate_1)
            self.all_sprites.add(self.portal.gate_2)

        self.apple = Apple(self.apple_image, self.obstacles, self.body, self.snake_g)
        self.all_sprites.add(self.apple)
        self.apples.add(self.apple)

        self.snake = Snake(self.snake_head)
        self.all_sprites.add(self.snake)
        self.snake_g.add(self.snake)
        self.tail = Block(self.snake, self.body_image)
        self.all_sprites.add(self.tail)
        self.snake_g.add(self.tail)

        self.ai = AI(self.snake, self.body, self.obstacles)
        # For debugging apple pos
        # for i in range(500):
        #     self.apple.move()
        #     print(self.apple.rect.topleft)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            if AI_on:
                self.ai.update(self.apple)
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits apple
        hits = pg.sprite.spritecollide(self.snake, self.apples, False, pg.sprite.collide_circle)
        for hit in hits:
            if not self.apple.move():
                self.playing = False
                self.won = True
            if not hit.eating:
                for i in range(hit.value):
                    new_tail = Block(self.tail, self.body_image)
                    self.tail = new_tail
                    self.all_sprites.add(new_tail)
                    self.body.add(new_tail)
                    # self.apple.move()
                    self.score += 10

        # Die!
        hits = pg.sprite.spritecollide(self.snake, self.body, False)
        for hit in hits:
            if hit.waiting == -1:
                self.playing = False

        hits = pg.sprite.spritecollide(self.snake, self.obstacles, False)
        for hit in hits:
            self.playing = False

        if DIE_ON_EDGE:
            if self.snake.rect.right > WIDTH or self.snake.rect.left < 0 or self.snake.rect.bottom > HEIGHT or self.snake.rect.top < 0:
                self.playing = False

        # Teleport:
        hits = pg.sprite.spritecollide(self.snake, self.portals, False, pg.sprite.collide_circle)
        for hit in hits:
            if not hit.exiting:
                hit.other.exiting = True
                self.snake.rect.center = hit.other.rect.center

        hits = pg.sprite.spritecollide(self.tail, self.portals, False, pg.sprite.collide_circle)
        for hit in hits:
            if hit.exiting:
                hit.exiting = False

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing= False
                self.running = False

    def draw(self):
        # Game Loop - Draw
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15 )
        # after drawing - flip
        pg.display.flip()

    def show_start_screen(self):
        # game start/splash screen
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        self.set_rect = pg.Rect(10, 10, 90, 40)
        pg.draw.rect(self.screen, GREY, self.set_rect)
        self.draw_text("Settings", 22, WHITE, 55, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/ continue screen
        if not self.running:
            return

        if self.won:
            #self.screen.fill(BGCOLOR)
            self.screen.blit(self.background, self.background_rect)
            self.draw_text("YOU WON!!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Try a more difficult screen to test your skill", 25, WHITE, WIDTH / 2, HEIGHT * 3/8)
        else:
            self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)

        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        self.set_rect = pg.Rect(10, 10, 90, 40)
        pg.draw.rect(self.screen, GREY, self.set_rect)
        self.draw_text("Settings", 22, WHITE, 55, 15)
        pg.display.flip()
        self.wait_for_key()

    def settings_screen(self):
        global SNAKE_PIXEL_SIZE
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, 30)
        self.draw_text_left("Snake Size", 22, WHITE, 100, HEIGHT / 4)
        self.draw_text_left("Snake Speed", 22, WHITE, 100, HEIGHT / 4 + 50)
        self.draw_text_left("Snake Separation", 22, WHITE, 100, HEIGHT / 4 + 100)
        self.draw_text_left("Apple Value", 22, WHITE, 100, HEIGHT / 4 + 150)
        self.draw_text_left("Die on edge", 22, WHITE, 100, HEIGHT / 4 + 200)
        self.draw_text_left("Rocks", 22, WHITE, 100, HEIGHT / 4 + 250)
        self.draw_text_left("Portals", 22, WHITE, 100, HEIGHT / 4 + 300)

        for i in range(7):
            self.draw_text(".................", 22, WHITE, WIDTH/2, HEIGHT / 4 + 50 * i)

        self.edit_group = pg.sprite.Group()

        self.input_size = InputBox(str(SNAKE_PIXEL_SIZE), "1234567890", 22, WHITE, 400, HEIGHT / 4)
        self.screen.blit(self.input_size.image, self.input_size.rect)

        self.set_rect = pg.Rect(10, 10, 90, 40)
        pg.draw.rect(self.screen, GREY, self.set_rect)
        self.draw_text("Back", 22, WHITE, 55, 15)
        pg.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.type == pg.KEYDOWN:
                        if self.input_size.active:
                            self.input_size.write(pg.key.name(event.key))
                            self.screen.blit(self.input_size.image, self.input_size.rect)
                            if event.key == pg.K_RETURN:
                                self.input_size.active = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.set_rect.collidepoint(event.pos):
                        self.show_start_screen()
                    if self.input_size.rect.collidepoint(event.pos):
                        self.input_size.active = True


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    #if event.key == pg.K_RIGHT:
                    waiting = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.set_rect.collidepoint(event.pos):
                        self.settings_screen()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw_text_left(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)
