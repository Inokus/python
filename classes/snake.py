import pygame
from pygame import Vector2
from constants.constants import (
    CELL_NUM_X,
    CELL_NUM_Y,
    CELL_SIZE,
    DARK_COLOR,
    LIGHT_COLOR,
)


class Snake:
    def __init__(self, length, pos):
        self.head = pygame.sprite.GroupSingle()
        self.body = pygame.sprite.Group()
        self.length = length
        self.pos = pos
        self.tail_pos = None
        self.direction = Vector2(1, 0)
        self.allow_direction_change = True
        self.allow_loop_around = True
        self.create(length)

    def draw(self, surface):
        self.head.draw(surface)
        self.body.draw(surface)

    def move(self):
        prev_pos = self.head.sprite.pos.copy()
        self.head.sprite.pos += self.direction
        # Check boundries only for head since the rest of segments follow
        if self.allow_loop_around:
            if self.head.sprite.pos.x < 1:
                self.head.sprite.pos.x = CELL_NUM_X - 2
            if self.head.sprite.pos.x > CELL_NUM_X - 2:
                self.head.sprite.pos.x = 1
            if self.head.sprite.pos.y < 3:
                self.head.sprite.pos.y = CELL_NUM_Y - 2
            if self.head.sprite.pos.y > CELL_NUM_Y - 2:
                self.head.sprite.pos.y = 3

        self.head.sprite.rect.topleft = (
            self.head.sprite.pos.x * CELL_SIZE,
            self.head.sprite.pos.y * CELL_SIZE,
        )

        for segment in self.body:
            temp_pos = segment.pos.copy()
            segment.pos = prev_pos
            prev_pos = temp_pos
            segment.rect.topleft = (
                segment.pos.x * CELL_SIZE,
                segment.pos.y * CELL_SIZE,
            )

        self.tail_pos = temp_pos
        self.allow_direction_change = True

    def create(self, length):
        for i in range(length):
            x = self.pos[0] - i
            y = self.pos[1]
            segment = Segment((x, y))
            if i == 0:
                segment.subsurface.fill(DARK_COLOR)
                self.head.add(segment)
            else:
                self.body.add(segment)

    def add_segment(self):
        segment = Segment(self.tail_pos)
        self.body.add(segment)

    def reset(self):
        self.head.empty()
        self.body.empty()
        self.tail_pos = None
        self.direction = Vector2(1, 0)
        self.allow_direction_change = True
        self.allow_loop_around = True
        self.create(self.length)


class Segment(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = Vector2(pos[0], pos[1])
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(DARK_COLOR)
        self.subsurface = self.image.subsurface(
            pygame.Rect(1, 1, CELL_SIZE - 2, CELL_SIZE - 2)
        )
        self.subsurface.fill(LIGHT_COLOR)
        self.rect = self.image.get_rect(
            topleft=(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE)
        )
