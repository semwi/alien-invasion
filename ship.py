# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:20:47 2021

@author: semwijnschenk
"""

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Een klasse voor het schip."""

    def __init__(self, ai_settings, screen):
        """Initialiseer het schip en bepaal de startpositie.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
                screen: tweede argument, het scherm
        """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Laad de afbeelding van het schip.
        self.img_ship(screen)
        # Bekijkt de positie van het schip.
        self.positie_schip()
        # Beweging wordt gevlagt.
        self.movement_flag()

    def img_ship(self, screen):
        """Laad de afbeelding van het schip en verkrijg zijn rect.
            trefwoord argumenten
                screen: eerste argument, het scherm
        """
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    def positie_schip(self):
        """Bekijkt de positie van het schip."""
        # Start elk nieuw schip in het midden onderaan het scherm.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Sla een decimale waarde op voor het midden van het schip.
        self.center = float(self.rect.centerx)

    def movement_flag(self):
        """Vlagt als er beweging is."""
        self.moving_right = False
        self.moving_left = False

    def update(self, ai_settings):
        """Werk de positie van het schip bij op basis van bewegingsvlaggen.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
        """
        # Werk de middenwaarde van het schip bij, niet de rechthoek.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect-object vanuit self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Teken het schip op zijn huidige locatie."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centreer het schip op het scherm."""
        self.center = self.screen_rect.centerx
