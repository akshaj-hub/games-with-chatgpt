from tkinter import *
import pygame
import random
file = open("example.txt", "r")

root = Tk()
# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Load the game assets
background = pygame.image.load("background.png").convert()
player_image = pygame.image.load("player.png").convert_alpha()
enemy_image = pygame.image.load("enemy.png").convert_alpha()
bullet_image = pygame.image.load("bullet.png").convert_alpha()
explosion_sound = pygame.mixer.Sound("metal-design-explosion-13491.mp3")
shoot_sound = pygame.mixer.Sound("9mm-pistol-shot-6349.mp3")

# Set up the game variables
player_x = 400
player_y = 500
player_speed = 5
enemies = []
bullets = []
score = 0

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + 16
                bullet_y = player_y - 32
                bullet_speed = 10
                bullets.append([bullet_x, bullet_y, bullet_speed])
                shoot_sound.play()

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 736:
        player_x += player_speed

    # Move the enemies
    for enemy in enemies:
        enemy[1] += 2
        if enemy[1] > 600:
            enemies.remove(enemy)

    # Move the bullets
    for bullet in bullets:
        bullet[1] -= bullet[2]
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Check for collisions
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy_image.get_rect())
        enemy_rect.x = enemy[0]
        enemy_rect.y = enemy[1]

        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet_image.get_rect())
            bullet_rect.x = bullet[0]
            bullet_rect.y = bullet[1]

            if enemy_rect.colliderect(bullet_rect):
                explosion_sound.play()
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10

        player_rect = pygame.Rect(player_image.get_rect())
        player_rect.x = player_x
        player_rect.y = player_y

        if enemy_rect.colliderect(player_rect):
            explosion_sound.play()
            running = False

    # Spawn new enemies
    if random.randint(0, 100) < 1:
        enemy_x = random.randint(0, 736)
        enemy_y = -64
        enemies.append([enemy_x, enemy_y])

    # Draw the game
    screen.blit(background, (0, 0))

    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))

    screen.blit(player_image, (player_x, player_y))

    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

# Clean up the game
pygame.quit()

root.mainloop()