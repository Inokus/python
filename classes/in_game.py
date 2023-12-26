import sys
import pygame
from pygame import Vector2
from classes.snake import Snake
from classes.food import Food
from utils.utils import draw_text, draw_border, tint_display
from constants.constants import (
    CELL_NUM_X,
    CELL_NUM_Y,
    CELL_SIZE,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    DISPLAY_UPDATE,
    DARK_COLOR,
    BRIGHT_COLOR,
    FONT,
    SMALL_FONT,
    MEDIUM_FONT,
)


class InGame:
    """Gameplay and user registration to leaderboards logic"""

    def __init__(self, surface, rect, file_handler, audio_manager, state_manager):
        self.surface = surface
        self.rect = rect
        self.file_handler = file_handler
        self.audio_manager = audio_manager
        self.state_manager = state_manager
        self.score = 0
        self.food_eaten = 0
        self.snake_speed = 300
        self.snake_speed_increments = 10
        self.max_snake_speed = 50
        self.input_buffer = []
        self.game_active = True
        self.music_active = False
        self.timer_active = False
        self.mode = None
        self.snake = Snake(3, (CELL_NUM_X // 4, CELL_NUM_Y // 2))
        self.food_items = []
        self.add_food([1, 5, 10])
        self.food_items[0].change_position()
        self.food_group = pygame.sprite.Group()
        self.food_group.add(self.food_items[0])

    def play(self):
        if self.game_active:
            if not self.music_active:
                self.music_active = True
                self.audio_manager.menu_music.stop()
                self.audio_manager.in_game_music.play(-1)

            if not self.timer_active:
                self.enable_timer()

            if self.food_collision():
                self.audio_manager.eat_sfx.play()

            if self.body_collision():
                self.audio_manager.in_game_music.stop()
                self.audio_manager.death1_sfx.play()
                self.game_over()
                return

            if self.mode == "Wall":
                if self.wall_collision():
                    self.audio_manager.in_game_music.stop()
                    self.audio_manager.death2_sfx.play()
                    self.game_over()
                    return

            self.surface.fill(BRIGHT_COLOR)
            draw_border(
                self.surface,
                (CELL_SIZE - 2, CELL_SIZE * 3 - 2),
                CELL_SIZE * (CELL_NUM_X - 2) + 4,
                CELL_SIZE * (CELL_NUM_Y - 4) + 4,
                (DARK_COLOR),
                2,
            )
            draw_text(
                self.surface,
                (self.rect.centerx, (CELL_SIZE * 3) // 2),
                f"Score: {self.score}",
                FONT,
                MEDIUM_FONT,
                (DARK_COLOR),
            )
            self.snake.draw(self.surface)
            self.food_group.draw(self.surface)
        else:
            username = self.get_username(self.surface, self.rect.center)
            self.file_handler.add_entry(self.mode, username, self.score)
            self.reset_game()
            self.state_manager.update_state("Main Menu")
            self.audio_manager.menu_music.play(-1)

    def handle_events(self, event):
        if event.type == DISPLAY_UPDATE:
            if self.input_buffer:
                self.snake.direction = self.input_buffer.pop(0)
            self.snake.move()

        # Allow snake direction change only if it's not opposite of last input
        if event.type == pygame.KEYDOWN:
            command_count = len(self.input_buffer)
            if event.key in (pygame.K_w, pygame.K_UP):
                if (command_count == 0 and self.snake.direction.y != 1) or (
                    command_count == 1 and self.input_buffer[0].y != 1
                ):
                    self.input_buffer.append(Vector2(0, -1))
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                if (command_count == 0 and self.snake.direction.x != -1) or (
                    command_count == 1 and self.input_buffer[0].x != -1
                ):
                    self.input_buffer.append(Vector2(1, 0))
            if event.key in (pygame.K_s, pygame.K_DOWN):
                if (command_count == 0 and self.snake.direction.y != -1) or (
                    command_count == 1 and self.input_buffer[0].y != -1
                ):
                    self.input_buffer.append(Vector2(0, 1))
            if event.key in (pygame.K_a, pygame.K_LEFT):
                if (command_count == 0 and self.snake.direction.x != 1) or (
                    command_count == 1 and self.input_buffer[0].x != 1
                ):
                    self.input_buffer.append(Vector2(-1, 0))
            if event.key == pygame.K_ESCAPE:
                self.disable_timer()
                self.state_manager.update_state("In Game Menu")

    def get_username(self, surface, pos):
        message_text = "Enter your username"
        input_text = ""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    length = len(input_text)
                    if event.key == pygame.K_RETURN:
                        if length < 3:
                            message_text = "A minimum of 3 characters are required"
                        elif not input_text.isalnum():
                            message_text = "Only alphanumeric characters are allowed"
                        else:
                            return input_text
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if length < 16:
                            input_text += event.unicode

            text_surface = pygame.Surface(
                (self.rect.width // 1.5, self.rect.height // 4)
            )
            text_surface.fill(BRIGHT_COLOR)
            text_rect = text_surface.get_rect(center=pos)
            draw_border(
                text_surface, (0, 0), text_rect.width, text_rect.height, DARK_COLOR, 2
            )
            draw_text(
                text_surface,
                (text_rect.width // 2, SMALL_FONT),
                message_text,
                FONT,
                SMALL_FONT,
                DARK_COLOR,
            )
            draw_text(
                text_surface,
                (text_rect.width // 2, text_rect.height // 2),
                input_text + "_" if len(input_text) < 16 else input_text,
                FONT,
                MEDIUM_FONT,
                DARK_COLOR,
            )
            draw_text(
                text_surface,
                (text_rect.width // 2, text_rect.height - SMALL_FONT),
                "Press ENTER to continue",
                FONT,
                SMALL_FONT,
                DARK_COLOR,
            )
            surface.blit(text_surface, text_rect)
            pygame.display.update()

    def add_food(self, values):
        for value in values:
            self.food_items.append(Food(self.snake, value))

    def change_food(self):
        # Change currently displayed food based on number of food items eaten so far
        if self.food_eaten % 10 == 0:
            self.food_items[2].change_position()
            self.food_group.add(self.food_items[2])
        elif self.food_eaten % 5 == 0:
            self.food_items[1].change_position()
            self.food_group.add(self.food_items[1])
        else:
            self.food_items[0].change_position()
            self.food_group.add(self.food_items[0])

    def food_collision(self):
        if pygame.sprite.spritecollide(self.snake.head.sprite, self.food_group, False):
            self.snake.add_segment()
            # Make sure that snake speed doesn't exceed maximum at any time and update it when needed
            if self.snake_speed > self.max_snake_speed:
                self.snake_speed -= self.snake_speed_increments
                self.update_timer()
            collided_food = pygame.sprite.spritecollide(
                self.snake.head.sprite, self.food_group, False
            )[0]
            self.score += collided_food.value
            self.food_eaten += 1
            self.food_group.remove(collided_food)
            self.change_food()
            return True
        return False

    def body_collision(self):
        if pygame.sprite.spritecollide(self.snake.head.sprite, self.snake.body, False):
            return True
        return False

    def wall_collision(self):
        if (
            self.snake.head.sprite.pos.x < 1
            or self.snake.head.sprite.pos.x > CELL_NUM_X - 2
            or self.snake.head.sprite.pos.y < 3
            or self.snake.head.sprite.pos.y > CELL_NUM_Y - 2
        ):
            return True
        return False

    def reset_game(self):
        self.score = 0
        self.food_eaten = 0
        self.snake_speed = 300
        self.input_buffer = []
        self.game_active = True
        self.music_active = False
        self.snake.reset()
        self.food_items[0].change_position()
        self.food_group.empty()
        self.food_group.add(self.food_items[0])

    def game_over(self):
        self.game_active = False
        self.disable_timer()
        tint_display(
            self.surface,
            DISPLAY_WIDTH,
            DISPLAY_HEIGHT,
            (128, 128, 128),
        )

    def enable_timer(self):
        pygame.time.set_timer(DISPLAY_UPDATE, self.snake_speed)
        self.timer_active = True

    def disable_timer(self):
        pygame.time.set_timer(DISPLAY_UPDATE, 0)
        self.timer_active = False

    def update_timer(self):
        pygame.time.set_timer(DISPLAY_UPDATE, self.snake_speed)
