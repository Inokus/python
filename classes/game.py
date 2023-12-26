import sys
import pygame
from classes.file_handler import FileHandler
from classes.audio_manager import AudioManager
from classes.state_manager import StateManager
from classes.in_game import InGame
from classes.menu import (
    MainMenu,
    ModeSelectMenu,
    InGameMenu,
    LeaderboardsMenu,
    OptionsMenu,
    CreditsMenu,
)
from constants.constants import (
    GAME_NAME,
    FPS,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    BRIGHT_COLOR,
)


class Game:
    """Main class responsible for game loop and event checking"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)

        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.display_rect = self.display.get_rect()
        self.display_color = BRIGHT_COLOR
        self.file_handler = FileHandler()
        if not self.file_handler.paths_exists():
            self.file_handler.create_paths()
        self.audio_manager = AudioManager(self.file_handler)
        self.state_manager = StateManager()
        self.in_game = InGame(
            self.display,
            self.display_rect,
            self.file_handler,
            self.audio_manager,
            self.state_manager,
        )
        self.main_menu = MainMenu(self.display, self.display_rect, self.state_manager)
        self.mode_select_menu = ModeSelectMenu(
            self.display, self.display_rect, self.state_manager
        )
        self.in_game_menu = InGameMenu(
            self.display, self.display_rect, self.audio_manager, self.state_manager
        )
        self.leaderboards_menu = LeaderboardsMenu(
            self.display, self.display_rect, self.file_handler, self.state_manager
        )
        self.options_menu = OptionsMenu(
            self.display,
            self.display_rect,
            self.file_handler,
            self.audio_manager,
            self.state_manager,
        )
        self.credits_menu = CreditsMenu(
            self.display,
            self.display_rect,
            self.state_manager,
        )
        self.audio_manager.set_volume()
        self.audio_manager.menu_music.play(-1)
        self.state_manager.current_state = "Main Menu"

    def start(self):
        while True:
            self.check_events()
            match self.state_manager.current_state:
                case "In Game":
                    self.in_game.play()
                case "Main Menu":
                    self.main_menu.draw()
                case "Mode Select":
                    self.mode_select_menu.draw()
                case "In Game Menu":
                    self.in_game_menu.draw()
                case "Leaderboards":
                    self.leaderboards_menu.draw()
                case "Options":
                    self.options_menu.draw()
                case "Credits":
                    self.credits_menu.draw()
                case _:
                    pass

            pygame.display.update()
            self.clock.tick(self.fps)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.state_manager.current_state == "Quit":
                pygame.quit()
                sys.exit()
            match self.state_manager.current_state:
                case "In Game":
                    self.in_game.handle_events(event)
                case "Main Menu":
                    self.main_menu.handle_events(event)
                case "Mode Select":
                    self.mode_select_menu.handle_events(event)
                    if self.state_manager.current_state == "Portal Mode":
                        self.in_game.mode = "Portal"
                        self.in_game.snake.allow_loop_around = True
                        self.state_manager.update_state("In Game")
                    elif self.state_manager.current_state == "Wall Mode":
                        self.in_game.mode = "Wall"
                        self.in_game.snake.allow_loop_around = False
                        self.state_manager.update_state("In Game")
                case "In Game Menu":
                    self.in_game_menu.handle_events(event)
                    if self.state_manager.current_state == "Main Menu":
                        self.in_game.reset_game()
                case "Leaderboards":
                    self.leaderboards_menu.handle_events(event)
                case "Options":
                    self.options_menu.handle_events(event)
                case "Credits":
                    self.credits_menu.handle_events(event)
                case _:
                    pass
