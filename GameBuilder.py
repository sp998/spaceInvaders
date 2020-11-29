from queue import Queue
from threading import Thread
import random
from game_objects import *


class GameBuilder:

    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fire_sounds = Queue()
        self.explosions = Queue()
        self.fire_sound = pygame.mixer.Sound('assets/laser.wav')
        self.explosion = pygame.mixer.Sound('assets/explosion.wav')
        self.score_text = pygame.font.Font("freesansbold.ttf", 32)
        self.game_over_text = pygame.font.Font("freesansbold.ttf", 50)
        self.playerimg = pygame.image.load("assets/player.png")
        self.enemyimg = pygame.image.load("assets/small_enemy.png")
        self.icon = pygame.image.load("assets/ufo.png")
        self.ENEMY_COUNT = 20
        self.game_over = False
        pygame.display.set_icon(self.icon)
        pygame.mixer.music.load("assets/background.wav")
        self.running = False
        self.enemies = []
        self.bullets = []
        self.score = 0

    def show_score(self, scr):
        score = self.score_text.render("Score:" + str(scr), True, (255, 255, 255))
        self.screen.blit(score, (10, 10))

    def show_game_over(self):
        game_over = self.game_over_text.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(game_over, (self.width / 3, self.height / 2))

    def set_size(self, size):
        self.width, height = size
        return self

    def set_enemy_count(self, count):
        self.ENEMY_COUNT = count
        return self

    def set_game_title(self, title):
        pygame.display.set_caption(title)
        return self

    def set_game_icon(self, icon):
        pygame.display.set_icon(icon)
        return self

    def set_fire_sound(self, sound):
        self.fire_sound = pygame.mixer.Sound(sound)
        return self

    def set_explosion_sound(self, sound):
        self.explosion = pygame.mixer.Sound(sound)
        return self

    def set_background_music(self, music):
        pygame.mixer.music.load(music)
        return self

    def stop(self):
        self.running = False

    def start(self):
        self.running = True
        pygame.mixer.music.play(-1)
        for _ in range(self.ENEMY_COUNT):
            self.enemies.append(
                Enemy(self, self.enemyimg, random.randint(0, self.width), random.randint(0, self.height / 3),
                      [0.1 * random.randint(10, 40), 0.1 * random.randint(1, 5)]))

        player = Player(self,
                        x=self.width / 2 - 64,
                        y=self.height - 64,
                        image=self.playerimg,
                        velocity=[2, 1.5]
                        )

        def play_music():
            while self.running:
                try:
                    firesound = self.fire_sounds.get_nowait()
                    if firesound:
                        firesound.play()
                except:
                    pass
                try:
                    exsound = self.explosions.get_nowait()

                    if exsound:
                        exsound.play()

                except:
                    pass

        t = Thread(target=play_music)
        t.start()

        while self.running:
            self.screen.fill((0, 0, 0))
            if not self.game_over:
                player.show()
                if len(self.enemies) < self.ENEMY_COUNT - 5:
                    for _ in range(5):
                        self.enemies.append(
                            Enemy(self, self.enemyimg, random.randint(0, self.width),
                                  random.randint(0, self.height / 4),
                                  [0.1 * random.randint(10, 40), 0.1 * random.randint(1, 5)]))
                for enemy in self.enemies:
                    enemy.show()
                    enemy.update()
                    if enemy.touches(player):
                        self.game_over = True
                        pygame.mixer.music.stop()
                    for bullet in self.bullets:
                        if enemy.touches(bullet):
                            self.explosions.put(self.explosion)
                            self.score += 1
                            self.enemies.remove(enemy)
                            self.bullets.remove(bullet)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    player.check_events(event)
                self.show_score(self.score)

                for bullet in self.bullets:
                    bullet.dy = bullet.velocity[1]
                    bullet.show()
                    bullet.update()

                player.update()

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                self.show_game_over()
            pygame.display.update()
