# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:55:41 2021

@author: semwijnschenk
"""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Een klasse die een enkele alien in de vloot vertegenwoordigt."""

    def __init__(self, ai_settings, screen):
        """Initialiseer de alien, en bepaal zijn startpositie.

        trefwoord argumenten
            ai_settings: eerste argument, de instellingen
            screen: tweede argument, het scherm
        """
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Maak de alien.
        self.maak_alien()

    def maak_alien(self):
        """Een functie voor het maken van de alien."""
        # Laad de afbeeldinging van de alien en stel het rect-attribuut in.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start elke nieuwe alien linksboven in het scherm.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Bewaar de exacte positie van de alien.
        self.x = float(self.rect.x)

    def blitme(self):
        """Teken de alien op zijn huidige locatie."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True als alien aan de rand van het scherm is."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Verplaats de alien naar rechts of links."""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
