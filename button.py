# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 20:18:22 2021

@author: semwijnschenk
"""

import pygame.font


class Button():
    """Een klasse voor de speelknop."""

    def __init__(self, ai_settings, screen, msg):
        """Initialiseer de knop atributen.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
                screen: tweede argument, het scherm
            input argumenten
                msg: derde argument, een string
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Maak de knop.
        self.maak_knop()

        # Het knopbericht hoeft maar één keer te worden voorbereid.
        self.prep_msg(msg)

    def maak_knop(self):
        """Stel de afmetingen en eigenschappen van de knop in."""
        self.width, self.height = 200, 50
        # De rgb is wit.
        self.button_color = (255, 255, 255)
        # De rgb is oranje.
        self.text_color = (247, 152, 98)
        self.font = pygame.font.SysFont(None, 48)

        # Bouw het rechthoekige object van de knop en centreer het.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    def prep_msg(self, msg):
        """"Verander het bericht in een gerenderde afbeelding
        en centreer de tekst op de knop.
            input argumenten
                msg: eerste argument, een string
        """
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Teken een lege knop en teken vervolgens een bericht.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
