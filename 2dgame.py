import pygame
import sys

# Inicjalizacja pygame
pygame.init()

# Ustawienia okna gry
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer Game')

# Kolory
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Gracz
player_width = 50
player_height = 60
player_x = 100
player_y = screen_height - player_height - 100
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_strength = -15
is_jumping = False
is_running = False

# Platformy
platforms = [
    pygame.Rect(50, screen_height - 100, 200, 20),
    pygame.Rect(300, screen_height - 200, 200, 20),
    pygame.Rect(550, screen_height - 300, 200, 20)
]

# Funkcja rysująca gracza
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))

# Funkcja rysująca platformy
def draw_platforms():
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)

# Funkcja sprawdzająca kolizję z platformą
def check_platform_collision(player_rect):
    global player_y, player_velocity_y, is_jumping
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y >= 0:
            # Gracz staje na platformie
            player_y = platform.top - player_height
            player_velocity_y = 0
            is_jumping = False
            return True
    return False

# Główna pętla gry
def game_loop():
    global player_x, player_y, player_velocity_y, is_jumping, is_running

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        screen.fill(WHITE)

        # Wydarzenia w grze
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        # Ruch gracza
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Bieganie
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            player_speed = 8
        else:
            player_speed = 5

        # Skakanie
        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = jump_strength
            is_jumping = True

        # Grawitacja
        player_velocity_y += gravity
        player_y += player_velocity_y

        # Sprawdzanie kolizji z platformami
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if not check_platform_collision(player_rect):
            is_jumping = True

        # Rysowanie elementów
        draw_player(player_x, player_y)
        draw_platforms()

        pygame.display.flip()

        # Ustawienie liczby klatek na sekundę
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Uruchomienie gry
game_loop()

