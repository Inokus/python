import pygame


def draw_text(surface, pos, text, font, font_size, color):
    text_font = pygame.font.Font(font, font_size)
    # Don't see much of a difference, so keeping AA off
    text_surface = text_font.render(text, False, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)


def draw_border(surface, pos, width, height, color, border_width):
    # Draw a little big area so that snake and food wouldn't overlap the border
    border = pygame.Rect(pos[0], pos[1], width, height)
    pygame.draw.rect(surface, color, border, border_width)


def tint_display(surface, display_width, display_height, tint_color, tint_alpha=128):
    last_frame = surface.copy()
    tint_surface = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
    tint_surface.fill((*tint_color, tint_alpha))

    # Blit the last frame and the tinted surface
    surface.blit(last_frame, (0, 0))
    surface.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
