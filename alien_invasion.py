# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 08:52:55 2021

@author: semwijnschenk
"""

import pygame
import geluid
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    """De functie die het spel uitvoert."""
    # Initialiseer pygame, instellingen en schermobject.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion - Sem Wijnschenk, NP2F")

    # Maak de speelknop.
    play_button = Button(ai_settings, screen, "Play")

    # Maak een schip, een groep kogels en een groep aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Creëer de vloot van buitenaardse wezens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Maak een term om statistieken bij te houden en maak een scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Speel de thema muziek af.
    geluid.thema()

    # Start de hoofdlus voor het spel.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update(ai_settings)
            gf.update_bullets(ai_settings, screen, sb, ship, stats, aliens,
                              bullets)
            gf.update_aliens(ai_settings, screen, ship, stats, sb, aliens,
                             bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button)


run_game()
