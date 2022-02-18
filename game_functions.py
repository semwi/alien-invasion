# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:37:15 2021

@author: semwijnschenk
"""

import sys
from pathlib import Path
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import geluid


def check_high_score(stats, sb):
    """Check of er een nieuwe highscore is.
           trefwoord argumenten
               stats: eerste argument, de statistieken
               sb: tweede argument, het scoreboard
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

        # Sla de nieuwe highscore op.
        p = Path('.')
        with open(p / 'high.txt', 'w') as file_object:
            file_object.write(str(stats.high_score))


def reset_spel(stats, ai_settings, sb, aliens, bullets, screen, ship):
    """Reset het spel.
           trefwoord argumenten
               stats: eerste argument, de statistieken
               ai_settings: tweede argument, de instellingen
               sb: derde argument, het scoreboard
               aliens: vierde argument, de aliens
               bullets: vijfde argument, de kogels
               screen: zesde argument, het scherm
               ship: zevende argument, het schip
    """
    # Reset de spelstatistieken.
    stats.ships_left = ai_settings.ship_limit
    stats.reset_stats()
    stats.game_active = True
    stats.score = 0
    stats.level = 1

    # Reset de instellingen.
    ai_settings.alien_points = 50
    ai_settings.ship_speed_factor
    ai_settings.bullet_speed_factor
    ai_settings.alien_speed_factor
    ai_settings.initialize_dynamic_settings()

    # Reset de scorebordafbeeldingen.
    sb.prep_ships()
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.show_score()

    # Verander muziek naar gemeplay muziek.
    geluid.gameplay()

    # Verberg muis.
    pygame.mouse.set_visible(False)

    # Maak de lijst met aliens en kogels leeg.
    aliens.empty()
    bullets.empty()

    # Maak nieuwe vloot en centreer het schip.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship


def check_play_button(ai_settings, sb, screen, stats, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Start een nieuw spel wanneer de speler op play klikt.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               sb: tweede argument, het scoreboard
               screen: derde argument, het scherm
               stats: vierde argument, de statistieken
               play_button: vijfde argument, de speel-knop
               ship: zesde argument, het schip
               aliens: zevende argument, de aliens
               bullets: achtste argument, de kogels
          input argumenten
               mouse_x: negende argument, een getal
               mouse_y: tiende argument, een getal
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        reset_spel(stats, ai_settings, sb, aliens, bullets, screen, ship)


def ship_hit(ai_settings, screen, ship, stats, sb, aliens, bullets):
    """Reageer op schip dat wordt geraakt door alien.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               ship: derde argument, het schip
               stats: vierde argument, de statistieken
               sb: vijfde argument, het scoreboard
               aliens: zesde argument, de aliens
               bullets: zevende argument, de kogels
    """
    if stats.ships_left > 0:
        # Verlaag de schepen met 1.
        stats.ships_left -= 1

        # Leeg de lijsten aliens en bullets.
        aliens.empty()
        bullets.empty()

        # Update het scoreboard.
        sb.prep_ships()

        # Maak een nieuwe vloot en centreer het schip.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Wacht 0,5 seconden.
        sleep(0.5)

        # Speel het geluid effect.
        geluid.life()

    else:
        # gameover muziek
        geluid.game_over()

        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_fleet_edges(ai_settings, aliens):
    """Reageer op gepaste wijze als aliens een rand hebben bereikt.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               aliens: tweede argument, de aliens
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Laat de hele vloot vallen en verander de richting van de vloot.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               aliens: tweede argument, de aliens
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_number_aliens_x(ai_settings, alien_width):
    """Bepaal het aantal aliens dat in een rij past.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
           input argumenten:
               alien_width: tweede argument, een getal
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creëer een alien en plaats deze in de rij.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               aliens: derde argument, de aliens
          input argumenten
               alien_number: vierde argument, een getal
               row_number: vijfde argument, een getal
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 70 + alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creëer een volledige vloot van aliens.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               ship: derde argument, het schip
               aliens: vierde argument, de aliens
    """
    # Creëer een alien en vind het aantal aliens op een rij.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Creëer de vloot van buitenaardse wezens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Vuur een kogel af, als de limiet nog niet is bereikt.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               ship: derde argument, het schip
               bullets: vierde argument, de kogels
    """
    # Speel het shoot soundeffect.
    geluid.shoot()
    # Maak een nieuwe kogel en voeg deze toe aan de groep met kogels.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """reageert op ingedrukte toetsen
           trefwoord argumenten
               event: eerste argument, evenement als in; als er iets gebeurt
               ai_settings: tweede argument, de instellingen
               screen: derde argument, het scherm
               ship: vierde argument, het schip
               bullets: vijfde argument, de kogels
    """
    if event.key == pygame.K_RIGHT:
        # Schip gaat naar rechts.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()


def check_keyup_events(event, ship):
    """Reageert op toets releases.
           trefwoord argumenten
               event: eerste argument, evenement als in; als er iets gebeurt
               ship: tweede argument, het schip
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """Reageert op toets -en muisgebeurtenissen.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               stats: derde argument, de statistieken
               sb: vierde argument, het scoreboard
               play_button: vijfde argument, de speel-knop
               ship: zesde argument, het schip
               aliens: zevende argument, de aliens
               bullets: achtste argument, de kogels
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, sb, screen, stats, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """Werk afbeeldingen op het scherm bij en flip naar het nieuwe scherm.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               stats: derde argument, de statistieken
               sb: vierde argument, het scoreboard
               ship: vijfde argument, het schip
               aliens: zesde argument, de aliens
               bullets: zevende argument, de kogels
               play_button: achtste argument, de speel-knop
    """
    # Teken het scherm opnieuw, elk gaat door de lus.

    screen.fill(ai_settings.bg_color)

    # Teken alle kogels opnieuw, achter schip en aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Teken de score informatie.
    sb.show_score()

    # Teken de play-knop als het spel inactief is.
    if not stats.game_active:
        play_button.draw_button()

    # Maak het meest recent getekende scherm zichtbaar.
    pygame.display.flip()


def update_bullets(ai_settings, screen, sb, ship, stats, aliens, bullets):
    """Update positie van kogels, en verwijder oude kogels.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               sb: derde argument, het scoreboard
               ship: vierde argument, het schip
               stats: vijfde argument, de statistieken
               aliens: zesde argument, de aliens
               bullets: zevende argument, de kogels
    """
    # Update de positie van bullet.
    bullets.update()

    # Verwijder kogels die al verdwenen zijn.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Reageert op botsingen tussen aliens en kogels.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               stats: derde argument, de statistieken
               sb: vierde argument, het scoreboard
               ship: vijfde argument, het schip
               aliens: zesde argument, de aliens
               bullets: zevende argument, de kogels
    """

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # Verwijder kogels en buitenaardse wezens die zijn gebotst.
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # Maak een nieuw level.
    start_new_level(ai_settings, screen, sb, stats, ship, aliens, bullets)


def start_new_level(ai_settings, screen, sb, stats, ship, aliens, bullets):
    """"Mak nieuwe floot, maak het spel sneller en sloop oude kogels .
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               stats: derde argument, de statistieken
               sb: vierde argument, het scoreboard
               ship: vijfde argument, het schip
               aliens: zesde argument, de aliens
               bullets: zevende argument, de kogels
    """
    if len(aliens) == 0:
        # Start nieuw level als de vloot kapot is.
        bullets.empty()
        ai_settings.increase_speed()

        # Ga naar het volgende level!
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Berekend hoeveel rijen er moeten komen.
          trefwoord argumenten
               ai_settings: eerste argument, de instellingen
          input argumenten
               ship_height: tweede argument, een getal
               alien_height: derde argument, een getal

         return aantal rijen
    """
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (3*alien_height))
    return number_rows


def check_aliens_bottom(ai_settings, screen, ship, stats, sb, aliens,
                        bullets):
    """Controleer of aliens de onderkant van het scherm hebben bereikt.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               ship: derde argument, het schip
               stats: vierde argument, de statistieken
               sb: vijfde argument, het scoreboard
               aliens: zesde argument, de aliens
               bullets: zevende argument, de kogels
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Behandel dit op dezelfde manier alsof het schip werd geraakt.
            ship_hit(ai_settings, screen, ship, stats, sb, aliens, bullets)
            break


def update_aliens(ai_settings, screen, ship, stats, sb, aliens, bullets):
    """Controleer of de vloot op een rand is,
      werk vervolgens de posities van alle aliens in de vloot bij.
           trefwoord argumenten
               ai_settings: eerste argument, de instellingen
               screen: tweede argument, het scherm
               ship: derde argument, het schip
               stats: vierde argument, de statistieken
               sb: vijfde argument, het scoreboard
               aliens: zesde argument, de aliens
               bullets: zevende argument, de kogels
      """
    check_fleet_edges(ai_settings, aliens)
    # Update positie van de aliens.
    aliens.update()

    # Zoek naar botsingen tussen aliens en het schip.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, stats, sb, aliens, bullets)

    # Kijk uit voor aliens die de grond raken.
    check_aliens_bottom(ai_settings, screen, ship, stats, sb, aliens, bullets)
