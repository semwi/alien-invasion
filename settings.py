# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 09:46:19 2021

@author: semwijnschenk
"""


class Settings():
    """Een klasse om alle instellingen voor Alien Invasion op te slaan."""

    def __init__(self):
        """Initialiseer de statische instellingen van het spel."""
        self.overige_settings()
        # Instellingen voor het scherm.
        self.scherm_settings()
        # Start instellingen die veranderen gedurende het spel.
        self.initialize_dynamic_settings()
        # Instellingen voor de kogel.
        self.bullet_settings()

    def scherm_settings(self):
        """Instellingen voor het scherm."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 165, 255)

    def bullet_settings(self):
        """Instellingen voor de kogel."""
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

    def initialize_dynamic_settings(self):
        """Initialiseer instellingen die tijdens het spel veranderen."""
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # Fleet_direction van 1 staat voor rechts, -1 staat voor links.
        self.fleet_direction = 1

        # Hoeveel levens heeft de speler?
        self.ship_limit = 3

    def increase_speed(self):
        """Verhoog snelheidsinstellingen en alien puntwaarden."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def overige_settings(self):
        """"Overige instellingen voor Alien Invasion."""
        # De instellingen voor de alien.
        self.fleet_drop_speed = 10

        # Hoeveel punten er bij komen per geschoten alien aan het begin.
        self.alien_points = 50

        # Hoe snel het spel versnelt.
        self.speedup_scale = 1.5

        # Hoe snel de score systeem versnelt.
        self.score_scale = 15
