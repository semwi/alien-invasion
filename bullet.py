# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 13:19:37 2021

@author: semwijnschenk
"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Een klasse om kogels afgevuurd vanaf het schip te beheren.
        input argumenten
            sprite: eerste argument, een afbeelding
    """

    def __init__(self, ai_settings, screen, ship):
        """Maak bullet object, op de huidige positie van het schip.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
                screen: tweede argument, het scherm
                ship: derde argument, het schip
        """
        super(Bullet, self).__init__()
        self.screen = screen

        # Stel de knop positie in.
        self.bullet_positie(ai_settings, ship)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def bullet_positie(self, ai_settings, ship):
        """Maak een bullet rect op (0, 0) en stel de juiste positie in.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
                ship: tweede argument, het schip
        """
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Sla een decimale waarde op voor de positie van bullet object.
        self.y = float(self.rect.y)

    def update(self):
        """Verplaats de kogel over het scherm."""
        # Werk de decimale positie van bullet object bij.
        self.y -= self.speed_factor
        # Werk de rechterpositie bij.
        self.rect.y = self.y

    def draw_bullet(self):
        """Teken de kogel naar het scherm."""
        pygame.draw.rect(self.screen, self.color, self.rect)
