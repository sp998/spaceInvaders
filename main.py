import pygame
import random
from pygame import mixer
from queue import Queue

ENEMY_COUNT = 20
import utils
from threading import Thread

score = 0
game_over = False


def main():
    pygame.init()
    mixer.music.load("assets/background.wav")

    pygame.display.set_caption("Space Invaders")
    fire_sound = mixer.Sound('assets/laser.wav')
    explosion = mixer.Sound('assets/explosion.wav')
    explosions = Queue()
    fire_sounds = Queue()
    score_text = pygame.font.Font("freesansbold.ttf", 32)
    game_over_text = pygame.font.Font("freesansbold.ttf", 50)
    playerimg = pygame.image.load("assets/player.png")
    enemyimg = pygame.image.load("assets/small_enemy.png")
    width, height = 800, 600
    icon = pygame.image.load("assets/ufo.png")
    pygame.display.set_icon(icon)
    running = True
    screen = pygame.display.set_mode((width, height))
    mixer.music.play(-1)

    def show_score(scr):
        score = score_text.render("Score:" + str(scr), True, (255, 255, 255))
        screen.blit(score, (10, 10))

    def show_game_over():
        game_over = game_over_text.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over, (width / 3, height / 2))

    class GameObject:
        def __init__(self, image, x, y, velocity):
            self.x = x
            self.y = y
            self.dx = 0
            self.dy = 0
            self.velocity = velocity
            self.image = image

        def show(self):
            screen.blit(self.image, (self.x, self.y))

        def touches(self, other):
            return utils.calc_distance(self.x, self.y, other.x, other.y) <= 27

        def update(self):
            self.x += self.dx
            self.y += self.dy

    class Enemy(GameObject):
        def update(self):
            if self.x < -32 or self.x > width:
                self.y += (self.velocity[1] * 100)
                self.velocity[0] *= -1
            self.dx = self.velocity[0]

            super().update()

    enemies = []
    bullets = []
    for _ in range(ENEMY_COUNT):
        enemies.append(Enemy(enemyimg, random.randint(0, width), random.randint(0, height / 3),
                             [0.1 * random.randint(10, 40), 0.1 * random.randint(1, 5)]))

    class Player(GameObject):
        def __init__(self, image, x, y, velocity):
            super().__init__(image, x, y, velocity)
            self.bullets = []

        def check_events(self, evt):
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_LEFT:
                    self.dx = -self.velocity[0]
                if evt.key == pygame.K_RIGHT:
                    self.dx = self.velocity[0]
                if evt.key == pygame.K_UP:
                    self.dy = -self.velocity[1]
                if evt.key == pygame.K_DOWN:
                    self.dy += self.velocity[1]
                if evt.key == pygame.K_SPACE:
                    fire_sounds.put(fire_sound)
                    bullets.append(
                        GameObject(pygame.image.load("assets/fire.png"), self.x + 32, self.y - 10, [0, -2]))

            if evt.type == pygame.KEYUP:
                if evt.key == pygame.K_LEFT or evt.key == pygame.K_RIGHT:
                    self.dx = 0
                if evt.key == pygame.K_UP or evt.key == pygame.K_DOWN:
                    self.dy = 0

        def update(self):
            super().update()
            self.x = 0 if self.x < 0 else (width - 64) if self.x > width - 64 else self.x
            self.y = 0 if self.y < 0 else (height - 64) if self.y > height - 64 else self.y

    player = Player(x=width / 2 - 64,
                    y=height - 64,
                    image=playerimg,
                    velocity=[2, 1.5]
                    )

    def play_music():
        while running:
            try:
                firesound = fire_sounds.get_nowait()
                if firesound:
                    firesound.play()
            except :
                pass
            try:
                exsound = explosions.get_nowait()

                if exsound:
                    exsound.play()

            except:
                pass

    t = Thread(target=play_music)
    t.start()

    while running:
        screen.fill((0, 0, 0))
        global game_over
        global score
        if not game_over:
            player.show()
            if len(enemies) < ENEMY_COUNT - 5:
                for _ in range(5):
                    enemies.append(Enemy(enemyimg, random.randint(0, width), random.randint(0, height / 3),
                                         [0.1 * random.randint(10, 40), 0.1 * random.randint(1, 5)]))
            for enemy in enemies:
                enemy.show()
                enemy.update()
                if enemy.touches(player):
                    game_over = True
                    mixer.music.stop()
                for bullet in bullets:
                    if enemy.touches(bullet):
                        explosions.put(explosion)
                        score += 1
                        enemies.remove(enemy)
                        bullets.remove(bullet)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                player.check_events(event)
            show_score(score)

            for bullet in bullets:
                bullet.dy = bullet.velocity[1]
                bullet.show()
                bullet.update()

            player.update()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            show_game_over()
        pygame.display.update()


if __name__ == "__main__":
    main()
