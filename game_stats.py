# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 19:10:04 2021

@author: semwijnschenk
"""


class GameStats():
    """Houd statistieken voor Alien Invasion bij."""

    def __init__(self, ai_settings):
        """Statistieken initialiseren.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
        """
        # Check de statistieken.
        self.check_stats(ai_settings)

        # Start alien invasion inactief.
        self.game_active = False

    def check_stats(self, ai_settings):
        """Checkt de statistieken.
            trefwoord argumenten
                ai_settings: eerste argument, de instellingen
        """
        # Start het bijhouden van de statistieken.
        self.ai_settings = ai_settings
        self.reset_stats()
        self.score = 0
        self.check_highscore()

    def check_highscore(self):
        """Haalt highscore uit high.txt."""
        with open('high.txt') as file_object:
            high = file_object.read()

        self.high_score = int(high)

    def reset_stats(self):
        """Initialiseer statistieken die veranderen tijdens het spel."""
        self.ships_left = self. ai_settings.ship_limit
        self.level = 1
