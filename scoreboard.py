# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 14:31:40 2021

@author: semwijnschenk
"""

import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    """Een klas om scoregegevens te rapporteren."""

    def __init__(self, ai_settings, screen, stats):
        """Initialiseer de attributen voor het bijhouden van scores.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
                screen: tweede argument, het scherm
                stats: derde argument, de statistieken
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Lettertype-instellingen voor scoren informatie.
        self.prep_font()

        # Bereid de initiele score afbeeldingen voor.
        self.prep_images()

    def prep_images(self):
        """Bereid de initiele score afbeeldingen voor."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_font(self):
        """Lettertype-instellingen voor scoren informatie."""
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

    def prep_score(self):
        """Verander de score in een gerenderde afbeelding."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Geef de score rechtsboven in het scherm weer.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Teken de score op het scherm."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Teken de schepen.
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Verander de highscore in een gerenderde afbeelding."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Centreer de hoogste score bovenaan het scherm.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Verander het niveau in een gerenderde afbeelding."""
        self.level_image = self.font.render(
            str(self.stats.level), True, self.text_color,
            self.ai_settings.bg_color)

        # Positie van het huidige level op het scherm.
        self.position_level()

    def position_level(self):
        """Plaats het niveau onder de score."""
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Laat zien hoeveel schepen er nog over zijn."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
