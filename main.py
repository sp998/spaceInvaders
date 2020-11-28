import pygame
import random
from pygame import mixer
import threading
ENEMY_COUNT = 30
import utils

score = 0
game_over = False


def main():
    pygame.init()
    mixer.music.load("assets/background.wav")
    pygame.display.set_caption("Space Invaders")
    fire_sound=mixer.Sound('assets/laser.wav')
    explosion=mixer.Sound('assets/explosion.wav')

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
    for _ in range(ENEMY_COUNT):
        enemies.append(Enemy(enemyimg, random.randint(0, width), random.randint(0, height / 3),
                             [0.1 * random.randint(1, 4), 0.1 * random.randint(1, 5)]))

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
                    self.bullets.append(
                        GameObject(pygame.image.load("assets/fire.png"), self.x + 32, self.y - 10, [0, -0.4]))
            if evt.type == pygame.KEYUP:
                if evt.key == pygame.K_LEFT or evt.key == pygame.K_RIGHT:
                    self.dx = 0
                if evt.key == pygame.K_UP or evt.key == pygame.K_DOWN:
                    self.dy = 0

        def show(self):
            super().show()
            for bullet in self.bullets:
                bullet.show()

        def update(self):
            for bullet in self.bullets:
                bullet.dy = bullet.velocity[1]
                if bullet.y < 0:
                    self.bullets.remove(bullet)
                for enemy in enemies:
                    if enemy.touches(bullet):
                        enemies.remove(enemy)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        explosion.play()
                        global score
                        score += 1
                bullet.update()

            for enemy in enemies:
                if self.touches(enemy):
                    global game_over
                    game_over = True
                    mixer.music.stop()

            super().update()
            self.x = 0 if self.x < 0 else (width - 64) if self.x > width - 64 else self.x
            self.y = 0 if self.y < 0 else (height - 64) if self.y > height - 64 else self.y

    player = Player(x=width / 2 - 64,
                    y=height - 64,
                    image=playerimg,
                    velocity=[0.5, 0.4]
                    )

    while running:
        screen.fill((0, 0, 0))
        if not game_over:
            player.show()
            if len(enemies) < ENEMY_COUNT - 5:
                for _ in range(5):
                    enemies.append(Enemy(enemyimg, random.randint(0, width), random.randint(0, height / 3),
                                         [0.1 * random.randint(1, 6), 0.1 * random.randint(1, 10)]))
            for enemy in enemies:
                enemy.show()
                enemy.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                player.check_events(event)
            global score
            show_score(score)
            player.update()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            show_game_over()
        pygame.display.update()


if __name__ == "__main__":
    main()
