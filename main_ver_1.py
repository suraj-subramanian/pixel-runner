import random
from sys import exit

import pygame


def display_score():
    """
    Updates the score on the screen
    :return: the current score
    """
    curr_time = (pygame.time.get_ticks() // 1000) - start_time
    score_surf = game_font.render(f'{curr_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return curr_time


def obstacle_movement(obstacles):
    if obstacles:
        for obstacle in obstacles:
            obstacle.x -= 5
            if obstacle.bottom == 300:
                screen.blit(snail_surf, obstacle)
            else:
                screen.blit(fly_surf, obstacle)

        obstacles = [obs for obs in obstacles if obs.x > - 100]
        return obstacles
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return True
    return False


def player_animation():
    global player_surf, player_index
    # play walking animation when on ground
    # play jump animation if player jumping
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        player_surf = player_walk[int(player_index) % len(player_walk)]


# Initialize pygame module
pygame.init()

# Set screen size
size = width, height = 800, 400
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))

# Load font
game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
score_surf = game_font.render('Test Text', False, (64, 64, 64))
score_rect = score_surf.get_rect(center=(width / 2, 50))

snail_xpos = 600
player_gravity = 0
game_active = False
start_time = 0
score = 0
obstacle_rect_list = []

# start/end screen img
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(width / 2, height / 2))
title_surf = game_font.render('Runner', False, (255, 255, 255))
title_rect = title_surf.get_rect(center=(width / 2, 50))
instruction_text = game_font.render('Press SPACE to start!', False, (255, 255, 255))
instruction_text_rect = instruction_text.get_rect(center=(width / 2, 350))

# game_message = game_font.render('Press SPACE to run', False, (111, 196, 169))
# game_message_rect = game_message.get_rect(center=(400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    # Event Loop
    for event in pygame.event.get():
        # Check for Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            # Enemy spawn event
            if event.type == obstacle_timer:
                if random.randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom=(random.randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(random.randint(900, 1100), 200)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = (pygame.time.get_ticks() // 1000)

    if game_active:

        # Blitting
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = not collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(instruction_text, instruction_text_rect)

        # Show score after game over
        if score != 0:
            score_message = game_font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 320))
            screen.blit(score_message, score_message_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

    pygame.display.update()
    # Limit framerate to 60
    clock.tick(60)
