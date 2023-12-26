import pygame
from classes.ui_elements import Button, Slider
from utils.utils import draw_text
from constants.constants import (
    DARK_COLOR,
    MEDIUM_COLOR,
    BRIGHT_COLOR,
    FONT,
    MEDIUM_FONT,
)

# Parent class that serves as blueprint for the rest of menus
class Menu:
    def __init__(self, surface, rect, state_manager):
        self.surface = surface
        self.rect = rect
        self.state_manager = state_manager
        self.center_x_pos = rect.center[0]
        self.center_y_pos = rect.center[1]
        self.btn_height = self.rect.height // 10
        self.btn_width = self.rect.width // 3
        self.font = FONT
        self.font_size = MEDIUM_FONT
        self.text_base_color = MEDIUM_COLOR
        self.text_hover_color = DARK_COLOR
        self.background_color = BRIGHT_COLOR
        self.options = []
        self.buttons = []
        self.selected = 0

    def draw(self):
        self.surface.fill(self.background_color)
        for i, button in enumerate(self.buttons):
            if self.selected == i:
                button.selected = True
            else:
                button.selected = False
            button.draw()

    # Allow menu navigation by keeping track of currently selected item
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                self.selected = (self.selected - 1) % len(self.options)
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.selected = (self.selected + 1) % len(self.options)

    def create_buttons(self, spacing=None):
        if spacing is None:
            spacing = self.btn_height // 2
        total_buttons_height = (self.btn_height + spacing) * len(self.options) - spacing
        start_y = (self.rect.height - total_buttons_height) // 2
        for i, option in enumerate(self.options):
            btn = Button(
                self.surface,
                (self.center_x_pos, start_y + (self.btn_height + spacing) * i),
                self.btn_width,
                self.btn_height,
                option,
                self.font,
                self.font_size,
                self.text_base_color,
                self.text_hover_color,
                self.background_color,
            )
            self.buttons.append(btn)


class MainMenu(Menu):
    def __init__(self, surface, rect, state_manager):
        super().__init__(surface, rect, state_manager)
        self.options = ["Play", "Leaderboards", "Options", "Credits", "Quit"]
        self.create_buttons()

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                state_input = self.handle_input()
                self.state_manager.update_state(state_input)

    def handle_input(self):
        state = self.options[self.selected]
        if state == "Play":
            state = "Mode Select"
        return state


class ModeSelectMenu(Menu):
    def __init__(self, surface, rect, state_manager):
        super().__init__(surface, rect, state_manager)
        self.options = ["Portal Mode", "Wall Mode", "Back"]
        self.create_buttons()

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                state_input = self.handle_input()
                if state_input == "Back":
                    self.state_manager.current_state = self.state_manager.previous_state
                else:
                    self.state_manager.update_state(state_input)
            if event.key == pygame.K_ESCAPE:
                self.state_manager.current_state = self.state_manager.previous_state

    def handle_input(self):
        state = self.options[self.selected]
        self.selected = 0
        return state


class InGameMenu(Menu):
    def __init__(self, surface, rect, audio_manager, state_manager):
        super().__init__(surface, rect, state_manager)
        self.audio_manager = audio_manager
        self.options = ["Resume", "Leaderboards", "Options", "Main Menu"]
        self.create_buttons()

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                state_input = self.handle_input()
                self.state_manager.update_state(state_input)
            if event.key == pygame.K_ESCAPE:
                self.state_manager.update_state("In Game")

    def handle_input(self):
        state = self.options[self.selected]
        if state == "Resume":
            state = "In Game"
        if state == "Main Menu":
            self.audio_manager.in_game_music.stop()
            self.audio_manager.menu_music.play(-1)
        self.selected = 0
        return state


class LeaderboardsMenu(Menu):
    def __init__(self, surface, rect, file_handler, state_manager):
        super().__init__(surface, rect, state_manager)
        self.file_handler = file_handler
        self.btn_width = self.rect.width // 4
        self.portal_mode_leaderboard = None
        self.wall_mode_leaderboard = None
        self.loaded = False
        self.previously_selected = 0
        self.options = ["Portal Mode", "Wall Mode", "Back"]
        self.create_buttons()

    def draw(self):
        self.surface.fill(self.background_color)
        for i, button in enumerate(self.buttons):
            if self.selected == i:
                button.selected = True
            else:
                button.selected = False
            button.draw()

        # When leaderboards are opened load up data only once
        if not self.loaded:
            self.get_leaderboards()

        if self.selected == 0:
            self.draw_leaderboards("Portal")
        elif self.selected == 1:
            self.draw_leaderboards("Wall")
        else:
            if self.previously_selected == 0:
                self.draw_leaderboards("Portal")
            else:
                self.draw_leaderboards("Wall")

    # Overwrite parent method to allow horizontal navigation
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.previously_selected = self.selected
                self.selected = (self.selected + 1) % len(self.options)
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.previously_selected = self.selected
                self.selected = (self.selected - 1) % len(self.options)
            if event.key == pygame.K_RETURN:
                state_input = self.handle_input()
                if state_input == "Back":
                    self.loaded = False
                    self.state_manager.current_state = self.state_manager.previous_state
            if event.key == pygame.K_ESCAPE:
                self.loaded = False
                self.state_manager.current_state = self.state_manager.previous_state

    def create_buttons(self, spacing=None):
        if spacing is None:
            spacing = self.btn_width // 3
        total_buttons_width = (self.btn_width + spacing) * len(self.options) - spacing
        start_x = (self.rect.width - total_buttons_width) // 2
        for i, option in enumerate(self.options):
            btn = Button(
                self.surface,
                (
                    start_x + (self.btn_width + spacing) * i,
                    self.rect.bottom - (MEDIUM_FONT + (self.btn_height // 2)),
                ),
                self.btn_width,
                self.btn_height,
                option,
                self.font,
                self.font_size,
                self.text_base_color,
                self.text_hover_color,
                self.background_color,
                "midleft",
            )
            self.buttons.append(btn)

    def handle_input(self):
        state = self.options[self.selected]
        self.selected = 0
        return state

    def draw_leaderboards(self, mode):
        if mode == "Portal":
            leaderboard = self.portal_mode_leaderboard
        else:
            leaderboard = self.wall_mode_leaderboard

        for i, entry in enumerate(leaderboard):
            divisor = len(entry) + 1
            draw_text(
                self.surface,
                (
                    (self.rect.width // divisor),
                    self.btn_height + ((self.btn_height // 1.4) * i),
                ),
                f"{i + 1}.",
                self.font,
                self.font_size,
                self.text_base_color,
            )
            for j, key in enumerate(["name", "score"]):
                draw_text(
                    self.surface,
                    (
                        (self.rect.width / divisor)
                        + (self.rect.width / divisor) * (j + 1),
                        self.btn_height + ((self.btn_height // 1.4) * i),
                    ),
                    f"{entry[key]}",
                    self.font,
                    self.font_size,
                    self.text_base_color,
                )

    def get_leaderboards(self):
        self.portal_mode_leaderboard = self.file_handler.get_data("Portal")
        self.wall_mode_leaderboard = self.file_handler.get_data("Wall")
        self.loaded = True


class OptionsMenu(Menu):
    def __init__(self, surface, rect, file_handler, audio_manager, state_manager):
        super().__init__(surface, rect, state_manager)
        self.file_handler = file_handler
        self.audio_manager = audio_manager
        self.options = ["Music volume", "SFX volume", "Back"]
        self.sliders = []
        self.selected_slider = None
        self.create_buttons(self.btn_height * 1.5)
        self.create_sliders()

    def draw(self):
        super().draw()
        for i, slider in enumerate(self.sliders):
            if self.selected == i:
                slider.selected = True
            else:
                slider.selected = False
            slider.draw()

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                if self.sliders[0].selected:
                    if self.audio_manager.music_volume < 100:
                        self.change_volume("increase", "Music", self.sliders[0])
                elif self.sliders[1].selected:
                    if self.audio_manager.sfx_volume < 100:
                        self.change_volume("increase", "SFX", self.sliders[1])
            if event.key in (pygame.K_a, pygame.K_LEFT):
                if self.sliders[0].selected:
                    if self.audio_manager.music_volume > 0:
                        self.change_volume("decrease", "Music", self.sliders[0])
                elif self.sliders[1].selected:
                    if self.audio_manager.sfx_volume > 0:
                        self.change_volume("decrease", "SFX", self.sliders[1])
            if event.key == pygame.K_RETURN:
                state_input = self.handle_input()
                if state_input == "Back":
                    self.state_manager.current_state = self.state_manager.previous_state
                else:
                    self.state_manager.update_state(state_input)
            if event.key == pygame.K_ESCAPE:
                self.state_manager.current_state = self.state_manager.previous_state

    def handle_input(self):
        state = self.options[self.selected]
        self.selected = 0
        return state

    def change_volume(self, adjustment, audio_type, slider):
        if adjustment == "increase":
            if audio_type == "Music":
                new_volume = self.audio_manager.music_volume + 5
            else:
                new_volume = self.audio_manager.sfx_volume + 5
        else:
            if audio_type == "Music":
                new_volume = self.audio_manager.music_volume - 5
            else:
                new_volume = self.audio_manager.sfx_volume - 5

        self.audio_manager.change_volume(audio_type, new_volume)
        self.file_handler.update_settings(audio_type, new_volume)
        self.adjust_slider(audio_type, slider)

    def create_sliders(self):
        music_slider = Slider(
            self.surface,
            (self.rect.centerx, self.buttons[0].rect.bottom + self.btn_height // 2),
            self.rect.width // 3,
            MEDIUM_FONT // 2,
            MEDIUM_COLOR,
            DARK_COLOR,
            MEDIUM_COLOR,
        )
        sfx_slider = Slider(
            self.surface,
            (self.rect.centerx, self.buttons[1].rect.bottom + self.btn_height // 2),
            self.rect.width // 3,
            MEDIUM_FONT // 2,
            MEDIUM_COLOR,
            DARK_COLOR,
            MEDIUM_COLOR,
        )
        self.adjust_slider("Music", music_slider)
        self.adjust_slider("SFX", sfx_slider)
        self.sliders.append(music_slider)
        self.sliders.append(sfx_slider)

    def adjust_slider(self, audio_type, slider):
        settings = self.file_handler.read(self.file_handler.settings_file_name)
        if audio_type == "Music":
            volume = settings[0]["music_volume"]
        else:
            volume = settings[0]["sfx_volume"]
        slider.thumb_rect.centerx = (
            slider.track_rect.left + (slider.width / 100) * volume
        )


class CreditsMenu(Menu):
    def __init__(self, surface, rect, state_manager):
        super().__init__(surface, rect, state_manager)
        self.options = ["Back"]
        self.song_names = []
        self.create_buttons()

    def draw(self):
        super().draw()
        self.draw_credits()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                state_input = self.handle_input()
                if state_input == "Back":
                    self.state_manager.current_state = self.state_manager.previous_state
            if event.key == pygame.K_ESCAPE:
                self.state_manager.current_state = self.state_manager.previous_state

    def create_buttons(self, spacing=None):
        if spacing is None:
            spacing = self.btn_height // 2
        start_y = self.rect.bottom - (MEDIUM_FONT + self.btn_height)
        for option in self.options:
            btn = Button(
                self.surface,
                (self.center_x_pos, start_y),
                self.btn_width,
                self.btn_height,
                option,
                self.font,
                self.font_size,
                self.text_base_color,
                self.text_hover_color,
                self.background_color,
            )
            self.buttons.append(btn)

    def handle_input(self):
        state = self.options[self.selected]
        self.selected = 0
        return state

    def draw_credits(self):
        available_height = self.rect.bottom - (MEDIUM_FONT + self.btn_height * 1.5)
        start_y = available_height // 4

        draw_text(
            self.surface,
            (self.rect.centerx, start_y - MEDIUM_FONT),
            "Programmed by Inokus",
            FONT,
            MEDIUM_FONT,
            DARK_COLOR,
        )
        draw_text(
            self.surface,
            (self.rect.centerx, start_y * 2 - MEDIUM_FONT * 2),
            "Music by Abstraction :",
            FONT,
            MEDIUM_FONT,
            DARK_COLOR,
        )
        draw_text(
            self.surface,
            (self.rect.centerx, start_y * 2),
            "(abstractionmusic.com)",
            FONT,
            MEDIUM_FONT,
            DARK_COLOR,
        )
        draw_text(
            self.surface,
            (self.rect.centerx, start_y * 2 + MEDIUM_FONT * 2),
            "Ludum Dare 30 - Track 6",
            FONT,
            MEDIUM_FONT,
            MEDIUM_COLOR,
        )
        draw_text(
            self.surface,
            (self.rect.centerx, start_y * 2 + MEDIUM_FONT * 4),
            "Ludum Dare 38 - Track 2",
            FONT,
            MEDIUM_FONT,
            MEDIUM_COLOR,
        )
        draw_text(
            self.surface,
            (self.rect.centerx, start_y * 3 + MEDIUM_FONT * 3),
            "SFX by OmegaPixelArt",
            FONT,
            MEDIUM_FONT,
            DARK_COLOR,
        )
