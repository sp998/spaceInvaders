import utils
import pygame


class GameObject:
    def __init__(self, game_builder, image, x, y, velocity):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.velocity = velocity
        self.image = image
        self.game_builder = game_builder

    def set_game_bulder(self, game):
        self.game_builder = game

    def show(self):
        self.game_builder.screen.blit(self.image, (self.x, self.y))

    def touches(self, other):
        return utils.calc_distance(self.x, self.y, other.x, other.y) <= 27

    def update(self):
        self.x += self.dx
        self.y += self.dy


class Enemy(GameObject):
    def update(self):
        if self.x < -32 or self.x > self.game_builder.width:
            self.y += (self.velocity[1] * 100)
            self.velocity[0] *= -1
        self.dx = self.velocity[0]
        super().update()


class Player(GameObject):

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
                self.game_builder.fire_sounds.put(self.game_builder.fire_sound)
                self.game_builder.bullets.append(
                    GameObject(self.game_builder, pygame.image.load("assets/fire.png"), self.x + 32, self.y - 10,
                               [0, -2]))

        if evt.type == pygame.KEYUP:
            if evt.key == pygame.K_LEFT or evt.key == pygame.K_RIGHT:
                self.dx = 0
            if evt.key == pygame.K_UP or evt.key == pygame.K_DOWN:
                self.dy = 0

    def update(self):
        super().update()
        self.x = 0 if self.x < 0 else (
                self.game_builder.width - 64) if self.x > self.game_builder.width - 64 else self.x
        self.y = 0 if self.y < 0 else (
                self.game_builder.height - 64) if self.y > self.game_builder.height - 64 else self.y
