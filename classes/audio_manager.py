import pygame


class AudioManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.music_volume = 50
        self.sfx_volume = 50
        self.menu_music = pygame.mixer.Sound("audio/music/Ludum Dare 30 - Track 6.wav")
        self.in_game_music = pygame.mixer.Sound(
            "audio/music/Ludum Dare 38 - Track 2.wav"
        )
        self.eat_sfx = pygame.mixer.Sound("audio/sfx/Eat.wav")
        self.death1_sfx = pygame.mixer.Sound("audio/sfx/Death Sound 1.wav")
        self.death2_sfx = pygame.mixer.Sound("audio/sfx/Death Sound 4.wav")

    def set_volume(self):
        settings = self.file_handler.read(self.file_handler.settings_file_name)
        self.music_volume = settings[0]["music_volume"]
        self.sfx_volume = settings[0]["sfx_volume"]
        self.menu_music.set_volume(self.music_volume / 100)
        self.in_game_music.set_volume(self.music_volume / 100)
        self.eat_sfx.set_volume(self.sfx_volume / 100)
        self.death1_sfx.set_volume(self.sfx_volume / 100)
        self.death2_sfx.set_volume(self.sfx_volume / 100)

    def change_volume(self, audio_type, volume):
        if audio_type == "Music":
            self.music_volume = volume
            self.menu_music.set_volume(volume / 100)
            self.in_game_music.set_volume(volume / 100)
        else:
            self.sfx_volume = volume
            self.eat_sfx.set_volume(volume / 100)
            self.death1_sfx.set_volume(volume / 100)
            self.death2_sfx.set_volume(volume / 100)
