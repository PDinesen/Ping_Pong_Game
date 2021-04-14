import pygame
from pygame.locals import *
import random
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_X = 700
BACKGROUND_Y = 400
SIZE = 20
SPEED_BALL = 2
SPEED_PLAYER = 2


class Ball:
    def __init__(self, surface):
        self.parent_screen = surface
        self.x = int(BACKGROUND_X / 2 - 50)
        self.y = int(BACKGROUND_Y / 2)
        self.radius = 8
        self.direction_x = SPEED_BALL * (-1)**random.randint(0, 1)
        self.direction_y = SPEED_BALL * (-1)**random.randint(0, 1)

    def draw(self):
        pygame.draw.circle(self. parent_screen, WHITE, (self.x, self.y), self.radius)

    def walk(self):
        self.x += self.direction_x
        self.y += self.direction_y
        self.draw()


class Player:
    def __init__(self, surface):
        self.score = 0
        self.parent_screen = surface
        self.y = int(BACKGROUND_Y / 2)
        self.direction = 'up'

    def draw(self, x):
        # self.parent_screen.fill(BLACK)
        pygame.draw.rect(self.parent_screen, WHITE, [x, self.y, 8, SIZE * 3])

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self, x):
        if self.direction == 'up':
            if self.y == 10:
                self.direction = 'down'
            else:
                self.y -= SPEED_PLAYER
        elif self.direction == 'down':
            if self.y + SIZE * 3 == BACKGROUND_Y - 10:
                self.direction = 'up'
            else:
                self.y += SPEED_PLAYER
        self.draw(x)


class Background:
    def __init__(self):
        self.surface = pygame.display.set_mode((BACKGROUND_X, BACKGROUND_Y))

    def draw(self):
        self.surface.fill(BLACK)
        pygame.draw.rect(self.surface, WHITE, [5, 5, BACKGROUND_X - 10, BACKGROUND_Y - 10], width=5)
        for i in range(int(BACKGROUND_Y / (SIZE + 10))):
            pygame.draw.rect(self.surface, WHITE, [int(BACKGROUND_X / 2) - 2, 10 + i * (SIZE + 10), 4, SIZE])


class Game:
    def __init__(self):
        pygame.init()
        self.background = Background()
        self.surface = self.background.surface
        self.player1 = Player(self.surface)
        self.player2 = Player(self.surface)
        self.player1.draw(20)
        self.player2.draw(BACKGROUND_X - 28)
        self.ball = Ball(self.surface)
        self.ball.draw()
        pygame.display.flip()

    def display_scores(self):
        font = pygame.font.SysFont('arial', 50)
        score1 = font.render(f"{self.player1.score}", True, WHITE)
        score2 = font.render(f"{self.player2.score}", True, WHITE)
        self.surface.blit(score1, (50, 50))
        self.surface.blit(score2, (BACKGROUND_X - 75, 50))

    def show_game_over(self):
        self.draw_all()
        pygame.draw.rect(self.surface, BLACK, [200, 100, 400, 150])
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Continue Press SPACE", True, WHITE)
        self.surface.blit(line1, (200, 100))
        line2 = font.render("or restart game with ENTER", True, WHITE)
        self.surface.blit(line2, (200, 150))
        line3 = font.render("or exit game with ESCAPE", True, WHITE)
        self.surface.blit(line3, (200, 200))
        pygame.display.flip()

    def is_collision(self, xy, c):
        if abs(xy - c) <= self.ball.radius:
            return True
        return False

    def move_all(self):
        self.ball.walk()
        self.player1.walk(20)
        self.player2.walk(BACKGROUND_X - 28)

    def draw_all(self):
        self.background.draw()
        self.player1.draw(20)
        self.player2.draw(BACKGROUND_X - 28)
        self.ball.draw()
        self.display_scores()
        pygame.display.flip()

    def play(self):
        self.background.draw()
        self.move_all()

        if self.is_collision(10, self.ball.y) or self.is_collision(BACKGROUND_Y - 10, self.ball.y):
            self.ball.direction_y *= -1
        if self.is_collision(10, self.ball.x):
            self.player2.score += 1
            raise Exception("Point for 2")
        if self.is_collision(BACKGROUND_X - 10, self.ball.x):
            self.player1.score += 1
            raise Exception("Point for 1")
        if self.is_collision(28, self.ball.x):
            if self.player1.y <= self.ball.y <= self.player1.y + SIZE * 3:
                self.ball.direction_x *= -1
        if self.is_collision(BACKGROUND_X - 28, self.ball.x):
            if self.player2.y <= self.ball.y <= self.player2.y + SIZE * 3:
                self.ball.direction_x *= -1

        self.display_scores()
        pygame.display.update()
        time.sleep(.01)

    def reset(self):
        self.player1 = Player(self.surface)
        self.player2 = Player(self.surface)
        self.ball = Ball(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if pause:
                        if event.key == K_RETURN:
                            self.reset()
                            pause = False
                        if event.key == K_SPACE:
                            self.ball = Ball(self.surface)
                            pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.player2.move_up()
                        if event.key == K_DOWN:
                            self.player2.move_down()
                        if event.key == K_a:
                            self.player1.move_up()
                        if event.key == K_z:
                            self.player1.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True


if __name__ == '__main__':
    game = Game()
    game.run()
