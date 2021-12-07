#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 27-10-2020
           """

import random

import pygame

pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))
# icon = pygame.image.load("ic.jpg")
# pygame.display.set_icon(icon)

wheat = (245, 222, 179)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (200, 0, 0)
light_red = (255, 0, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
green = (34, 177, 76)
light_green = (0, 255, 0)

clock = pygame.time.Clock()
tank_width = 40
tank_height = 20
turret_width = 5
wheel_width = 5
ground_height = 35

small_font = pygame.font.SysFont("comicsansms", 25)
medium_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("Yu Mincho Demibold", 85)
vsmall_font = pygame.font.SysFont("Yu Mincho Demibold", 25)


def score(score_):
    """ """
    text = small_font.render(f"Score: {str(score_)}", True, white)
    game_display.blit(text, [0, 0])


def text_objects(text, color, size="small"):
    """ """
    if size == "small":
        text_surface = small_font.render(text, True, color)
    if size == "medium":
        text_surface = medium_font.render(text, True, color)
    if size == "large":
        text_surface = large_font.render(text, True, color)
    if size == "vsmall":
        text_surface = vsmall_font.render(text, True, color)

    return text_surface, text_surface.get_rect()


def text_to_button(msg, color, button_x, button_y, button_width, button_height, size="vsmall"):
    """ """
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = ((button_x + (button_width / 2)), button_y + (button_height / 2))
    game_display.blit(text_surf, text_rect)


def message_to_screen(msg, color, y_displace=0, size="small"):
    """ """
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    game_display.blit(text_surf, text_rect)


def tank(x, y, tur_pos):
    """ """
    x = int(x)
    y = int(y)

    possible_turrets = [
        (x - 27, y - 2),
        (x - 26, y - 5),
        (x - 25, y - 8),
        (x - 23, y - 12),
        (x - 20, y - 14),
        (x - 18, y - 15),
        (x - 15, y - 17),
        (x - 13, y - 19),
        (x - 11, y - 21),
    ]

    pygame.draw.circle(game_display, blue, (x, y), int(tank_height / 2))
    pygame.draw.rect(game_display, blue, (x - tank_height, y, tank_width, tank_height))
    pygame.draw.line(game_display, blue, (x, y), possible_turrets[tur_pos], turret_width)
    pygame.draw.circle(game_display, blue, (x - 15, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 10, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 15, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 10, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 5, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x + 5, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x + 10, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x + 15, y + 20), wheel_width)
    return possible_turrets[tur_pos]


def enemy_tank(x, y, tur_pos):
    """ """
    x = int(x)
    y = int(y)

    possible_turrets = [
        (x + 27, y - 2),
        (x + 26, y - 5),
        (x + 25, y - 8),
        (x + 23, y - 12),
        (x + 20, y - 14),
        (x + 18, y - 15),
        (x + 15, y - 17),
        (x + 13, y - 19),
        (x + 11, y - 21),
    ]

    pygame.draw.circle(game_display, blue, (x, y), int(tank_height / 2))
    pygame.draw.rect(game_display, blue, (x - tank_height, y, tank_width, tank_height))
    pygame.draw.line(game_display, blue, (x, y), possible_turrets[tur_pos], turret_width)
    pygame.draw.circle(game_display, blue, (x - 15, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 10, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 15, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 10, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x - 5, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x + 5, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x + 10, y + 20), wheel_width)
    pygame.draw.circle(game_display, blue, (x + 15, y + 20), wheel_width)
    return possible_turrets[tur_pos]


def game_controls():
    """ """
    gcont = True
    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(black)
        message_to_screen("Controls", white, -100, size="large")
        message_to_screen("Fire: Spacebar", wheat, -30)
        message_to_screen("Move Turret: Up and Down arrows", wheat, 10)
        message_to_screen("Move Tank: Left and Right arrows", wheat, 50)
        message_to_screen("Press D to raise Power % AND Press A to lower Power % ", wheat, 140)
        message_to_screen("Pause: P", wheat, 90)
        button("Play", 150, 500, 100, 50, green, light_green, action="play")
        button("Main", 350, 500, 100, 50, yellow, light_yellow, action="main")
        button("Quit", 550, 500, 100, 50, red, light_red, action="quit")
        pygame.display.update()
        clock.tick(15)


def button(text, x, y, width, height, inactive_color, active_color, action=None, size=" "):
    """ """
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(game_display, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                game_loop()
            if action == "main":
                game_intro()
    else:
        pygame.draw.rect(game_display, inactive_color, (x, y, width, height))
    text_to_button(text, black, x, y, width, height)


def pause():
    """ """
    paused = True
    message_to_screen("Paused", white, -100, size="large")
    message_to_screen("Press C to continue playing or Q to quit", wheat, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)


def barrier(x_location, random_height, barrier_width):
    """ """
    pygame.draw.rect(
        game_display,
        green,
        [x_location, display_height - random_height, barrier_width, random_height],
    )


def explosion(x, y, size=50):
    """ """
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        start_point = x, y
        color_choices = [red, light_red, yellow, light_yellow]
        magnitude = 1

        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1 * magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)
            pygame.draw.circle(
                game_display,
                color_choices[random.randrange(0, 4)],
                (exploding_bit_x, exploding_bit_y),
                random.randrange(1, 5),
            )
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False


def fire_shell(
    xy,
    tankx,
    tanky,
    tur_pos,
    gun_power,
    x_location,
    barrier_width,
    random_height,
    enemy_tank_x,
    enemy_tank_y,
):
    """ """
    fire = True
    damage = 0
    starting_shell = list(xy)
    print("FIRE!", xy)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.draw.circle(game_display, red, (starting_shell[0], starting_shell[1]), 5)
        starting_shell[0] -= (12 - tur_pos) * 2
        starting_shell[1] += int(
            (((starting_shell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2)
            - (tur_pos + tur_pos / (12 - tur_pos))
        )
        if starting_shell[1] > display_height - ground_height:
            print("Last shell:", starting_shell[0], starting_shell[1])
            hit_x = int((starting_shell[0] * display_height - ground_height) / starting_shell[1])
            hit_y = int(display_height - ground_height)
            print("Impact:", hit_x, hit_y)
            if enemy_tank_x + 10 > hit_x > enemy_tank_x - 10:
                print("Critical Hit!")
                damage = 25
            elif enemy_tank_x + 15 > hit_x > enemy_tank_x - 15:
                print("Hard Hit!")
                damage = 18
            elif enemy_tank_x + 25 > hit_x > enemy_tank_x - 25:
                print("Medium Hit")
                damage = 10
            elif enemy_tank_x + 35 > hit_x > enemy_tank_x - 35:
                print("Light Hit")
                damage = 5

            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = starting_shell[0] <= x_location + barrier_width
        check_x_2 = starting_shell[0] >= x_location
        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:", starting_shell[0], starting_shell[1])
            hit_x = int((starting_shell[0]))
            hit_y = int(starting_shell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False
        pygame.display.update()
        clock.tick(60)
    return damage


def e_fire_shell(
    xy,
    tankx,
    tanky,
    tur_pos,
    gun_power,
    xlocation,
    barrier_width,
    random_height,
    ptankx,
    ptanky,
):
    """ """
    damage = 0
    current_power = 1
    power_found = False
    while not power_found:
        current_power += 1
        if current_power > 100:
            power_found = True
        fire = True
        starting_shell = list(xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            starting_shell[0] += (12 - tur_pos) * 2
            starting_shell[1] += int(
                (((starting_shell[0] - xy[0]) * 0.015 / (current_power / 50)) ** 2)
                - (tur_pos + tur_pos / (12 - tur_pos))
            )

            if starting_shell[1] > display_height - ground_height:
                hit_x = int((starting_shell[0] * display_height - ground_height) / starting_shell[1])
                hit_y = int(display_height - ground_height)
                # explosion(hit_x,hit_y)
                if ptankx + 15 > hit_x > ptankx - 15:
                    print("target acquired!")
                    power_found = True
                fire = False

            check_x_1 = starting_shell[0] <= xlocation + barrier_width
            check_x_2 = starting_shell[0] >= xlocation
            check_y_1 = starting_shell[1] <= display_height
            check_y_2 = starting_shell[1] >= display_height - random_height

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int((starting_shell[0]))
                hit_y = int(starting_shell[1])
                # explosion(hit_x,hit_y)
                fire = False

    fire = True
    starting_shell = list(xy)
    print("FIRE!", xy)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(game_display, red, (starting_shell[0], starting_shell[1]), 5)

        starting_shell[0] += (12 - tur_pos) * 2
        gun_power = random.randrange(int(current_power * 0.90), int(current_power * 1.10))

        starting_shell[1] += int(
            (((starting_shell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2)
            - (tur_pos + tur_pos / (12 - tur_pos))
        )

        if starting_shell[1] > display_height - ground_height:
            print("last shell:", starting_shell[0], starting_shell[1])
            hit_x = int((starting_shell[0] * display_height - ground_height) / starting_shell[1])
            hit_y = int(display_height - ground_height)
            print("Impact:", hit_x, hit_y)

            if ptankx + 10 > hit_x > ptankx - 10:
                print("Critical Hit!")
                damage = 25
            elif ptankx + 15 > hit_x > ptankx - 15:
                print("Hard Hit!")
                damage = 18
            elif ptankx + 25 > hit_x > ptankx - 25:
                print("Medium Hit")
                damage = 10
            elif ptankx + 35 > hit_x > ptankx - 35:
                print("Light Hit")
                damage = 5

            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = starting_shell[0] <= xlocation + barrier_width
        check_x_2 = starting_shell[0] >= xlocation

        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:", starting_shell[0], starting_shell[1])
            hit_x = int((starting_shell[0]))
            hit_y = int(starting_shell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage


def power(level):
    """ """
    text = small_font.render(f"Power: {str(level)}%", True, wheat)
    game_display.blit(text, [display_width / 2, 0])


def game_intro():
    """ """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:

                    pygame.quit()
                    quit()

        game_display.fill(black)
        message_to_screen("Welcome to Tanks!", white, -100, size="large")
        button("Play", 150, 500, 100, 50, wheat, light_green, action="play", size="vsmall")
        button(
            "Controls",
            350,
            500,
            100,
            50,
            wheat,
            light_yellow,
            action="controls",
            size="vsmall",
        )
        button("Quit", 550, 500, 100, 50, wheat, light_red, action="quit", size="vsmall")
        pygame.display.update()

        clock.tick(15)


def game_over_call():
    """ """
    game_over = True

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(black)
        message_to_screen("Game Over", white, -100, size="large")
        message_to_screen("You died.", wheat, -30)
        button("Play Again", 150, 500, 150, 50, wheat, light_green, action="play")
        button("Controls", 350, 500, 100, 50, wheat, light_yellow, action="controls")
        button("Quit", 550, 500, 100, 50, wheat, light_red, action="quit")
        pygame.display.update()
        clock.tick(15)


def you_win():
    """ """
    win = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(black)
        message_to_screen("You won!", white, -100, size="large")
        message_to_screen("Congratulations!", wheat, -30)
        button("play Again", 150, 500, 150, 50, wheat, light_green, action="play")
        button("controls", 350, 500, 100, 50, wheat, light_yellow, action="controls")
        button("quit", 550, 500, 100, 50, wheat, light_red, action="quit")
        pygame.display.update()
        clock.tick(15)


def health_bars(player_health, enemy_health):
    """ """
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red
    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(game_display, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(game_display, enemy_health_color, (20, 25, enemy_health, 25))


def game_loop():
    """ """
    game_exit = False
    game_over = False
    FPS = 15
    player_health = 100
    enemy_health = 100
    barrier_width = 50
    main_tank_x = display_width * 0.9
    main_tank_y = display_height * 0.9
    tank_move = 0
    current_tur_pos = 0
    change_tur = 0
    enemy_tank_x = display_width * 0.1
    enemy_tank_y = display_height * 0.9
    fire_power = 50
    power_change = 0
    x_location = (display_width / 2) + random.randint(-0.1 * display_width, 0.1 * display_width)
    random_height = random.randrange(display_height * 0.1, display_height * 0.6)

    while not game_exit:
        if game_over:
            message_to_screen("Game Over", red, -50, size="large")
            message_to_screen("Press C to play again or Q to exit", black, 50)
            pygame.display.update()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit = True
                        game_over = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            game_loop()
                        elif event.key == pygame.K_q:

                            game_exit = True
                            game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank_move = -5
                elif event.key == pygame.K_RIGHT:
                    tank_move = 5
                elif event.key == pygame.K_UP:
                    change_tur = 1
                elif event.key == pygame.K_DOWN:
                    change_tur = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    damage = fire_shell(
                        gun,
                        main_tank_x,
                        main_tank_y,
                        current_tur_pos,
                        fire_power,
                        x_location,
                        barrier_width,
                        random_height,
                        enemy_tank_x,
                        enemy_tank_y,
                    )
                    enemy_health -= damage

                    possible_movement = ["f", "r"]
                    move_index = random.randrange(0, 2)

                    for x in range(random.randrange(0, 10)):

                        if display_width * 0.3 > enemy_tank_x > display_width * 0.03:
                            if possible_movement[move_index] == "f":
                                enemy_tank_x += 5
                            elif possible_movement[move_index] == "r":
                                enemy_tank_x -= 5

                            game_display.fill(black)
                            health_bars(player_health, enemy_health)
                            gun = tank(main_tank_x, main_tank_y, current_tur_pos)
                            enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, 8)
                            fire_power += power_change
                            power(fire_power)
                            barrier(x_location, random_height, barrier_width)
                            game_display.fill(
                                green,
                                rect=[
                                    0,
                                    display_height - ground_height,
                                    display_width,
                                    ground_height,
                                ],
                            )
                            pygame.display.update()

                            clock.tick(FPS)

                    damage = e_fire_shell(
                        enemy_gun,
                        enemy_tank_x,
                        enemy_tank_y,
                        8,
                        50,
                        x_location,
                        barrier_width,
                        random_height,
                        main_tank_x,
                        main_tank_y,
                    )
                    player_health -= damage
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_move = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    change_tur = 0

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0

        main_tank_x += tank_move
        current_tur_pos += change_tur

        if current_tur_pos > 8:
            current_tur_pos = 8
        elif current_tur_pos < 0:
            current_tur_pos = 0

        if main_tank_x - (tank_width / 2) < x_location + barrier_width:
            main_tank_x += 5

        game_display.fill(black)
        health_bars(player_health, enemy_health)
        gun = tank(main_tank_x, main_tank_y, current_tur_pos)
        enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, 8)

        fire_power += power_change
        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1

        power(fire_power)
        barrier(x_location, random_height, barrier_width)
        game_display.fill(
            green,
            rect=[0, display_height - ground_height, display_width, ground_height],
        )
        pygame.display.update()

        if player_health < 1:
            game_over_call()
        elif enemy_health < 1:
            you_win()
        clock.tick(FPS)

    pygame.quit()
    quit()


game_intro()
game_loop()
