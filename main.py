import pygame
import random
import asyncio

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cupcake Collector")
clock = pygame.time.Clock()

GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 6

async def main():

    character_image = pygame.image.load("assets/character.png").convert_alpha()
    cupcake_image = pygame.image.load("assets/cupcake.png").convert_alpha()

    character_image = pygame.transform.scale(character_image, (50, 50))
    cupcake_image = pygame.transform.scale(cupcake_image, (32, 32))

    player_rect = character_image.get_rect()
    player_rect.x = 100
    player_rect.y = 450

    player_vel_x = 0
    player_vel_y = 0
    is_grounded = False

    platforms = [
        pygame.Rect(0, 550, 800, 50),
        pygame.Rect(100, 400, 250, 20),
        pygame.Rect(450, 300, 250, 20)
    ]

    cupcakes = []

    for _ in range(10):
        x = random.randint(50, 750)
        y = random.randint(50, 500)

        cupcake_rect = cupcake_image.get_rect()
        cupcake_rect.center = (x, y)

        cupcakes.append(cupcake_rect)

    font = pygame.font.Font(None, 40)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player_vel_x = 0

        if keys[pygame.K_LEFT]:
            player_vel_x = -PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            player_vel_x = PLAYER_SPEED

        if keys[pygame.K_UP] and is_grounded:
            player_vel_y = JUMP_STRENGTH
            is_grounded = False

        player_vel_y += GRAVITY

        player_rect.x += player_vel_x

        if player_rect.left < 0:
            player_rect.left = 0

        if player_rect.right > WIDTH:
            player_rect.right = WIDTH

        player_rect.y += player_vel_y

        is_grounded = False

        for platform in platforms:
            if player_rect.colliderect(platform):

                if player_vel_y > 0:
                    player_rect.bottom = platform.top
                    player_vel_y = 0
                    is_grounded = True

                elif player_vel_y < 0:
                    player_rect.top = platform.bottom
                    player_vel_y = 0

        if player_rect.bottom > 550:
            player_rect.bottom = 550
            player_vel_y = 0
            is_grounded = True

        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)

        screen.fill((135, 206, 235))

        for platform in platforms:
            pygame.draw.rect(screen, (80, 180, 80), platform)

        for cupcake in cupcakes:
            screen.blit(cupcake_image, cupcake)

        screen.blit(character_image, player_rect)

        score = 10 - len(cupcakes)

        score_text = font.render(
            f"Cupcakes: {score}/10",
            True,
            (255, 255, 255)
        )

        screen.blit(score_text, (20, 20))

        if len(cupcakes) == 0:
            win_text = font.render(
                "You collected all the cupcakes!",
                True,
                (255, 255, 255)
            )

            screen.blit(
                win_text,
                (
                    WIDTH // 2 - win_text.get_width() // 2,
                    100
                )
            )

        pygame.display.flip()

        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())