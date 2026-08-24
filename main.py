import pygame
import random
import sys
import math

pygame.init()

# ============================================================
# GAME SETTINGS
# ============================================================

WIDTH = 400
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Error 404: nob/bot")

clock = pygame.time.Clock()

# ============================================================
# VARIABLES
# ============================================================

lives = 3
score = 0
kill = 0

menu = 1

easy = 0
medium = 0
hard = 0
impossible = 0

rng = 0

hitboxes_on = False

# ============================================================
# FONTS
# ============================================================

font20 = pygame.font.SysFont("Times New Roman", 20)
font18 = pygame.font.SysFont("Times New Roman", 18)
font32 = pygame.font.SysFont("Times New Roman", 32)
font35 = pygame.font.SysFont("Times New Roman", 35)

# ============================================================
# LOAD IMAGES
# ============================================================

def load_image(filename):
    return pygame.image.load(
        "assets/" + filename
    ).convert_alpha()


background1_image = load_image(
    "background1.gif"
)

background2_image = load_image(
    "background2.gif"
)

backe_image = load_image(
    "backe.png_1.gif"
)

playerleft_image = load_image(
    "playerleft.gif"
)

playerright_image = load_image(
    "playerright.gif"
)

potion_image = load_image(
    "Potion_of_Harming_JE3-removebg-preview.png_1.gif"
)

# Remove white background
potion_image = potion_image.convert_alpha()

for x in range(potion_image.get_width()):
    for y in range(potion_image.get_height()):

        r, g, b, a = potion_image.get_at((x, y))

        if r > 240 and g > 240 and b > 240:
            potion_image.set_at(
                (x, y),
                (255, 255, 255, 0)
            )

enemy1_image = load_image(
    "retrocreature_04_1.gif"
)

enemy2_image = load_image(
    "retrocreature_03_1.gif"
)

enemy3_image = load_image(
    "retrocreature_05_1.gif"
)

enemy4_image = load_image(
    "retrocreature_06_1.gif"
)

sword_right_image = load_image(
    "sword_diamond_1.gif"
)

sword_left_image = load_image(
    "sword_left.gif"
)

# ============================================================
# IMAGE SCALING
# ============================================================

def scale_image(image, scale):

    width = int(
        image.get_width() * scale
    )

    height = int(
        image.get_height() * scale
    )

    return pygame.transform.smoothscale(
        image,
        (width, height)
    )


background1_image = pygame.transform.scale(
    background1_image,
    (WIDTH, HEIGHT)
)

background2_image = pygame.transform.scale(
    background2_image,
    (WIDTH, HEIGHT)
)

backe_image = pygame.transform.scale(
    backe_image,
    (WIDTH, HEIGHT)
)

# Player scale = 0.32

playerleft_image = scale_image(
    playerleft_image,
    0.32
)

playerright_image = scale_image(
    playerright_image,
    0.32
)

# Enemy scale = 0.13

enemy1_image = scale_image(
    enemy1_image,
    0.13
)

enemy2_image = scale_image(
    enemy2_image,
    0.13
)

enemy3_image = scale_image(
    enemy3_image,
    0.13
)

enemy4_image = scale_image(
    enemy4_image,
    0.13
)

# Sword scale = 0.4

sword_right_image = scale_image(
    sword_right_image,
    0.4
)

sword_left_image = scale_image(
    sword_left_image,
    0.4
)

# Potion scale = 0.3

potion_image = scale_image(
    potion_image,
    0.3
)

# ============================================================
# SPRITE CLASS
# ============================================================

class Sprite:

    def __init__(self, image, x, y):

        self.image = image

        self.x = float(x)
        self.y = float(y)

        self.visible = True

        self.debug = False

    def draw(self):

        if not self.visible:
            return

        rect = self.image.get_rect(
            center=(
                int(self.x),
                int(self.y)
            )
        )

        screen.blit(
            self.image,
            rect
        )

    def get_rect(self):

        return self.image.get_rect(
            center=(
                int(self.x),
                int(self.y)
            )
        )

# ============================================================
# CREATE SPRITES
# ============================================================

background = Sprite(
    background1_image,
    200,
    200
)

player = Sprite(
    playerright_image,
    200,
    200
)

enemy1 = Sprite(
    enemy1_image,
    -20,
    random.randint(0, 400)
)

enemy2 = Sprite(
    enemy2_image,
    random.randint(0, 400),
    420
)

enemy3 = Sprite(
    enemy3_image,
    420,
    random.randint(0, 400)
)

enemy4 = Sprite(
    enemy4_image,
    random.randint(1, 400),
    -20
)

sword = Sprite(
    sword_right_image,
    200,
    200
)

potion = Sprite(
    potion_image,
    random.randint(0, 400),
    -40
)

# ============================================================
# PLAYER HITBOX
# ============================================================

playerhitbox = pygame.Rect(
    175,
    175,
    50,
    50
)

# ============================================================
# BUTTON HITBOXES
# ============================================================

easybutton = pygame.Rect(
    115,
    110,
    110,
    40
)

mediumbutton = pygame.Rect(
    75,
    170,
    140,
    40
)

hardbutton = pygame.Rect(
    115,
    230,
    100,
    40
)

impossiblebutton = pygame.Rect(
    0,
    300,
    210,
    40
)

hitbox_button = pygame.Rect(
    0,
    350,
    235,
    40
)

# ============================================================
# POTION
# ============================================================

potion_velocity_y = 0

# ============================================================
# COLLISION
# ============================================================

def touching(sprite1, sprite2):

    return sprite1.get_rect().colliderect(
        sprite2.get_rect()
    )


def touching_player(sprite):

    return sprite.get_rect().colliderect(
        playerhitbox
    )

# ============================================================
# SWORD COLLISION
# ============================================================

def sword_touching(sprite):

    if not sword.visible:
        return False

    return sword.get_rect().colliderect(
        sprite.get_rect()
    )

# ============================================================
# ENEMY MOVEMENT
# ============================================================

def enemy_movement(speed):

    enemies = [
        enemy1,
        enemy2,
        enemy3,
        enemy4
    ]

    for enemy in enemies:

        if enemy.x < player.x:

            enemy.x += (
                0.5
                + speed * score
            )

        if enemy.x > player.x:

            enemy.x -= (
                0.5
                + speed * score
            )

        if enemy.y < player.y:

            enemy.y += (
                0.5
                + speed * score
            )

        if enemy.y > player.y:

            enemy.y -= (
                0.5
                + speed * score
            )

# ============================================================
# PLAYER MOVEMENT
# ============================================================

def player_movement():

    keys = pygame.key.get_pressed()

    # W

    if keys[pygame.K_w]:

        player.y -= 3.6

    # S

    if keys[pygame.K_s]:

        player.y += 3.6

    # A

    if keys[pygame.K_a]:

        player.x -= 3.6

    # D

    if keys[pygame.K_d]:

        player.x += 3.6

    # UP

    if keys[pygame.K_UP]:

        player.y -= 3.6

    # DOWN

    if keys[pygame.K_DOWN]:

        player.y += 3.6

    # LEFT

    if keys[pygame.K_LEFT]:

        player.x -= 3.6

    # RIGHT

    if keys[pygame.K_RIGHT]:

        player.x += 3.6

    # Update player hitbox

    playerhitbox.center = (
        int(player.x),
        int(player.y)
    )

    # ========================================================
    # PLAYER BOUNDARIES
    # ========================================================

    if playerhitbox.top < 0:

        playerhitbox.top = 0

        player.y = playerhitbox.centery

    if playerhitbox.bottom > HEIGHT:

        playerhitbox.bottom = HEIGHT

        player.y = playerhitbox.centery

    if playerhitbox.left < 0:

        playerhitbox.left = 0

        player.x = playerhitbox.centerx

    if playerhitbox.right > WIDTH:

        playerhitbox.right = WIDTH

        player.x = playerhitbox.centerx

    # ========================================================
    # MOUSE / SWORD
    # ========================================================

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_x > player.x:

        sword.image = sword_right_image

        player.image = playerright_image

    else:

        sword.image = sword_left_image

        player.image = playerleft_image

    # ========================================================
    # ORIGINAL-STYLE SWORD POSITION
    # ========================================================

    if mouse_x > player.x:

        sword.visible = True

        sword.x = mouse_x

    else:

        sword.visible = True

        sword.x = mouse_x

    if mouse_y > player.y:

        sword.visible = True

        sword.y = mouse_y

    else:

        sword.visible = True

        sword.y = mouse_y

# ============================================================
# INTERACTIONS
# ============================================================

def interactions():

    global lives
    global score
    global kill

    # Enemy 1

    if sword_touching(enemy1):

        kill += 1

        enemy1.x = -50

        enemy1.y = random.randint(
            0,
            400
        )

        score += 1

    # Enemy 2

    if sword_touching(enemy2):

        kill += 1

        enemy2.x = random.randint(
            0,
            400
        )

        enemy2.y = 450

        score += 1

    # Enemy 3

    if sword_touching(enemy3):

        kill += 1

        enemy3.x = 450

        enemy3.y = random.randint(
            0,
            400
        )

        score += 1

    # Enemy 4

    if sword_touching(enemy4):

        kill += 1

        enemy4.x = random.randint(
            0,
            400
        )

        enemy4.y = -50

        score += 1

    # ========================================================
    # ENEMY -> PLAYER
    # ========================================================

    if touching_player(enemy1):

        lives -= 1

        enemy1.x = -50

        enemy1.y = random.randint(
            0,
            400
        )

    if touching_player(enemy2):

        lives -= 1

        enemy2.x = random.randint(
            0,
            400
        )

        enemy2.y = 450

    if touching_player(enemy3):

        lives -= 1

        enemy3.x = 450

        enemy3.y = random.randint(
            0,
            400
        )

    if touching_player(enemy4):

        lives -= 1

        enemy4.x = random.randint(
            0,
            400
        )

        enemy4.y = -50

# ============================================================
# SCORE
# ============================================================

def show_score():

    text = font20.render(
        "Score:",
        True,
        "white"
    )

    screen.blit(
        text,
        (2, 0)
    )

    text = font20.render(
        str(score),
        True,
        "white"
    )

    screen.blit(
        text,
        (65, 0)
    )

    text = font20.render(
        "Lives:",
        True,
        "white"
    )

    screen.blit(
        text,
        (310, 0)
    )

    text = font20.render(
        str(lives),
        True,
        "white"
    )

    screen.blit(
        text,
        (365, 0)
    )

    text = font18.render(
        "Enemies Killed:",
        True,
        "white"
    )

    screen.blit(
        text,
        (100, 0)
    )

    text = font18.render(
        str(kill),
        True,
        "white"
    )

    screen.blit(
        text,
        (230, 0)
    )

# ============================================================
# BACKGROUND
# ============================================================

def background2():

    if score < 20:

        background.image = background1_image

    else:

        background.image = background2_image

    # Game over

    if lives <= 0:

        enemy1.visible = False
        enemy2.visible = False
        enemy3.visible = False
        enemy4.visible = False

        sword.visible = False

        background.image = backe_image

        text = font35.render(
            "Error 404: nob/bot",
            True,
            "red"
        )

        screen.blit(
            text,
            (50, 350)
        )

# ============================================================
# POTION RNG
# ============================================================

def potion_rng():

    global rng
    global lives
    global potion_velocity_y

    if (
        score == 10
        or score == 20
        or score == 30
        or score == 40
        or score == 50
        or score == 60
        or score == 70
        or score == 80
        or score == 90
        or score == 100
    ):

        rng = 1

    else:

        rng = 0

    # Potion leaves screen

    if potion.y > 420:

        potion.y = -40

        potion.x = random.randint(
            0,
            400
        )

    # Player touches potion

    if touching_player(potion):

        lives += 2

        potion.y = -40

        potion.x = random.randint(
            0,
            400
        )

        potion_velocity_y = 0

    # Sword touches potion

    if sword_touching(potion):

        lives += 1

        potion.y = -40

        potion.x = random.randint(
            0,
            400
        )

        potion_velocity_y = 0

# ============================================================
# DRAW HITBOXES
# ============================================================

def draw_hitboxes():

    if not hitboxes_on:
        return

    pygame.draw.rect(
        screen,
        "red",
        playerhitbox,
        1
    )

    pygame.draw.rect(
        screen,
        "red",
        enemy1.get_rect(),
        1
    )

    pygame.draw.rect(
        screen,
        "red",
        enemy2.get_rect(),
        1
    )

    pygame.draw.rect(
        screen,
        "red",
        enemy3.get_rect(),
        1
    )

    pygame.draw.rect(
        screen,
        "red",
        enemy4.get_rect(),
        1
    )

    pygame.draw.rect(
        screen,
        "red",
        potion.get_rect(),
        1
    )

    pygame.draw.rect(
        screen,
        "red",
        sword.get_rect(),
        1
    )

# ============================================================
# HOME SCREEN
# ============================================================

def home_screen():

    screen.fill("black")

    mouse_pos = pygame.mouse.get_pos()

    # EASY

    color = "red"

    if easybutton.collidepoint(mouse_pos):

        color = "white"

    text = font32.render(
        "EASY",
        True,
        color
    )

    screen.blit(
        text,
        (160, 100)
    )

    # MEDIUM

    color = "red"

    if mediumbutton.collidepoint(mouse_pos):

        color = "white"

    text = font32.render(
        "MEDIUM",
        True,
        color
    )

    screen.blit(
        text,
        (140, 160)
    )

    # HARD

    color = "red"

    if hardbutton.collidepoint(mouse_pos):

        color = "white"

    text = font32.render(
        "HARD",
        True,
        color
    )

    screen.blit(
        text,
        (160, 225)
    )

    # IMPOSSIBLE

    color = "red"

    if impossiblebutton.collidepoint(mouse_pos):

        color = "white"

    text = font32.render(
        "IMPOSSIBLE",
        True,
        color
    )

    screen.blit(
        text,
        (110, 290)
    )

    # HITBOXES

    color = "red"

    if hitbox_button.collidepoint(mouse_pos):

        color = "white"

    text = font32.render(
        "On/Off Hitboxes",
        True,
        color
    )

    screen.blit(
        text,
        (15, 365)
    )

# ============================================================
# DRAW GAME
# ============================================================

def draw_game():

    background.draw()

    enemy1.draw()
    enemy2.draw()
    enemy3.draw()
    enemy4.draw()

    potion.draw()

    player.draw()

    sword.draw()

    draw_hitboxes()

    show_score()

# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True

while running:

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ====================================================
        # MOUSE CLICK
        # ====================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            # EASY

            if (
                menu == 1
                and easybutton.collidepoint(
                    mouse_pos
                )
            ):

                menu = 0
                easy = 1

            # MEDIUM

            elif (
                menu == 1
                and mediumbutton.collidepoint(
                    mouse_pos
                )
            ):

                menu = 0
                medium = 1

            # HARD

            elif (
                menu == 1
                and hardbutton.collidepoint(
                    mouse_pos
                )
            ):

                menu = 0
                hard = 1

            # IMPOSSIBLE

            elif (
                menu == 1
                and impossiblebutton.collidepoint(
                    mouse_pos
                )
            ):

                menu = 0
                impossible = 1

            # HITBOXES

            elif (
                menu == 1
                and hitbox_button.collidepoint(
                    mouse_pos
                )
            ):

                hitboxes_on = True

    # ========================================================
    # GAME
    # ========================================================

    if menu == 0 and lives > 0:

        # EASY

        if easy == 1:

            enemy_movement(
                0.02
            )

        # MEDIUM

        if medium == 1:

            enemy_movement(
                0.04
            )

        # HARD

        if hard == 1:

            enemy_movement(
                0.07
            )

        # IMPOSSIBLE

        if impossible == 1:

            enemy_movement(
                0.2
            )

        player_movement()

        interactions()

        potion_rng()

    # ========================================================
    # POTION MOVEMENT
    # ========================================================

    if rng == 1:

        potion_velocity_y = 9

    if rng == 0:

        potion.y = -40

        potion.x = random.randint(
            0,
            400
        )

        potion_velocity_y = 0

    potion.y += potion_velocity_y

    # ========================================================
    # DRAW
    # ========================================================

    if menu == 1:

        home_screen()

    else:

        background2()

        draw_game()

    pygame.display.flip()

    clock.tick(60)

# ============================================================
# QUIT
# ============================================================

pygame.quit()

sys.exit()