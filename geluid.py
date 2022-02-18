# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 20:21:50 2021

@author: semwijnschenk
"""

from pygame import mixer


def gameplay():
    """Ren functie die gameplay muziek afspeeld."""
    # Laad de muziek de mixer in.
    mixer.music.load("audio/gameplay.mp3")

    # Zet het volume lager.
    mixer.music.set_volume(0.4)

    # Speel het geluid op een channel voor oneindig lang.
    mixer.Channel(0).play(mixer.Sound("audio/gameplay.mp3"), -1)


def thema():
    """Een functie die thema muziek afspeeld."""
    mixer.music.load("audio/theme.mp3")
    mixer.music.set_volume(0.4)
    mixer.Channel(0).play(mixer.Sound('audio/theme.mp3'), -1)


def game_over():
    """Een functie die een game_over sound effect afspeeld."""
    mixer.music.load("audio/game_over.mp3")
    mixer.music.set_volume(0.7)
    mixer.Channel(1).play(mixer.Sound("audio/game_over.mp3"))


def life():
    """Een functie die een sound effect afspeeld als er 1 life minder is."""
    mixer.music.load("audio/life.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    mixer.Channel(2).play(mixer.Sound("audio/life.mp3"))


def shoot():
    """Een functie die een schiet sound effect afspeeld."""
    mixer.music.load("audio/shoot.mp3")
    mixer.music.set_volume(0.3)
    mixer.music.play()
    mixer.Channel(3).play(mixer.Sound("audio/shoot.mp3"))
