import pygame
from utils.utils import draw_text


class Button:
    def __init__(
        self,
        surface,
        pos,
        width,
        height,
        text,
        font,
        font_size,
        text_base_color,
        text_hover_color,
        background_color,
        align="midtop",
    ):
        self.parent_surface = surface
        self.surface = pygame.Surface((width, height))
        if align == "midtop":
            self.rect = self.surface.get_rect(midtop=pos)
        else:
            self.rect = self.surface.get_rect(midleft=pos)
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font = font
        self.text_base_color = text_base_color
        self.text_hover_color = text_hover_color
        self.background_color = background_color
        self.selected = False

    def draw(self):
        self.surface.fill((self.background_color))
        if self.selected:
            draw_text(
                self.surface,
                (self.width // 2, self.height // 2),
                self.text,
                self.font,
                self.font_size,
                self.text_hover_color,
            )
        else:
            draw_text(
                self.surface,
                (self.width // 2, self.height // 2),
                self.text,
                self.font,
                self.font_size,
                self.text_base_color,
            )
        self.parent_surface.blit(self.surface, self.rect)


class Slider:
    def __init__(
        self,
        surface,
        pos,
        width,
        height,
        thumb_base_color,
        thumb_hover_color,
        track_color,
    ):
        self.parent_surface = surface
        self.track_surface = pygame.Surface((width, height))
        self.thumb_surface = pygame.Surface((height * 2, height * 2))
        self.track_rect = self.track_surface.get_rect(center=pos)
        self.thumb_rect = self.thumb_surface.get_rect(center=pos)
        self.width = width
        self.height = height
        self.thumb_base_color = thumb_base_color
        self.thumb_hover_color = thumb_hover_color
        self.track_color = track_color
        self.selected = False

    def draw(self):
        self.track_surface.fill((self.track_color))
        if self.selected:
            self.thumb_surface.fill(self.thumb_hover_color)
        else:
            self.thumb_surface.fill(self.thumb_base_color)

        self.parent_surface.blit(self.track_surface, self.track_rect)
        self.parent_surface.blit(self.thumb_surface, self.thumb_rect)
