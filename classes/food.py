from random import randint
import pygame
from pygame import Vector2
from constants.constants import (
    CELL_NUM_X,
    CELL_NUM_Y,
    CELL_SIZE,
    DARK_COLOR,
    MEDIUM_COLOR,
    LIGHT_COLOR,
)


class Food(pygame.sprite.Sprite):
    def __init__(self, snake, value):
        super().__init__()
        self.snake = snake
        self.value = value
        self.pos = Vector2(0, 0)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(
            topleft=(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE)
        )
        self.color_subsurface = self.image.subsurface(
            pygame.Rect(1, 1, CELL_SIZE - 2, CELL_SIZE - 2)
        )
        self.square_subsurface = self.image.subsurface(
            pygame.Rect(self.rect.centerx - 2, self.rect.centery - 2, 5, 5)
        )
        self.assign_colors(value)

    # Modify the looks depending on food value
    def assign_colors(self, value):
        if value == 1:
            self.image.fill(DARK_COLOR)
            self.color_subsurface.fill((LIGHT_COLOR))
            self.square_subsurface.fill((MEDIUM_COLOR))
        elif value == 5:
            self.image.fill(DARK_COLOR)
            self.color_subsurface.fill((LIGHT_COLOR))
            self.square_subsurface.fill((DARK_COLOR))
        else:
            self.image.fill(MEDIUM_COLOR)
            self.color_subsurface.fill((DARK_COLOR))
            self.square_subsurface.fill((LIGHT_COLOR))

    def get_position(self):
        x = randint(1, CELL_NUM_X - 2)
        y = randint(3, CELL_NUM_Y - 2)
        return (x, y)

    def change_position(self):
        self.pos = Vector2(self.get_position())

        # Make sure that food item doesn't appear on top of snake
        while True:
            valid_pos = True

            if self.pos == self.snake.head.sprite.pos:
                valid_pos = False
            for segment in self.snake.body:
                if segment.pos == self.pos:
                    valid_pos = False

            if not valid_pos:
                self.pos = Vector2(self.get_position())
            else:
                break

        self.rect = self.image.get_rect(
            topleft=(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE)
        )
