from pygame import *
import random
import json

init()

window_size = (800, 600)
display.set_caption("Впіймай яблука")
window = display.set_mode(window_size)

clock = time.Clock()
game_font = font.SysFont('Arial', 24)
failed_font = font.SysFont('Arial', 140, bold=True)
score_font = font.SysFont('Arial', 40, bold=True)
FPS = 60

player = Rect(150, window_size[1]//2 -1, 100, 100)

score = 0
lose = False
faults = 0

background_image1 = image.load("images/background1.png")
background_image1 = transform.scale(background_image1, (800, 600))
background_image2 = image.load("images/background2.png")
background_image2 = transform.scale(background_image2, (800, 600))
background_image3 = image.load("images/background3.png")
background_image3 = transform.scale(background_image3, (800, 600))
background_image4 = image.load("images/background4.png")
background_image4 = transform.scale(background_image4, (800, 600))

backgrounds=["background_image1","background_image2","background_image3","background_image4",]

basket_image = image.load("images/basket.png")
basket_image = transform.scale(basket_image, (200, 120))

red_apple_image = image.load("images/red_apple.png")
red_apple_image = transform.scale(red_apple_image, (80, 80))

green_apple_image = image.load("images/green_apple.png")
green_apple_image = transform.scale(green_apple_image, (80, 80))

golden_apple_image = image.load("images/golden_apple.png")
golden_apple_image = transform.scale(golden_apple_image, (80, 80))

bomba_image = image.load("images/bomba.png")
bomba_image = transform.scale(bomba_image, (80, 80))

mixer.init()
sound_fail= mixer.Sound("Sounds/fail.mp3")
sound_catch= mixer.Sound("Sounds/catch.mp3")
sound_speed_up= mixer.Sound("Sounds/speed_up.mp3")
sound_bonus = mixer.Sound("Sounds/bonus.mp3")
sound_game_over= mixer.Sound("Sounds/game_over.mp3")
sound_boom= mixer.Sound("Sounds/boom.mp3")

data = {}
try:
    with open("settings.json", "r") as f:
        data = json.load(f)
except:
    data = {}

apples = []

SPAWN_EVENT = USEREVENT + 1
time.set_timer(SPAWN_EVENT, 2000)

def generate_apples():
    apple_x = random.randint(0, window_size[0] - red_apple_image.get_width())
    apple_y = -red_apple_image.get_height()

    img = random.choice([red_apple_image, green_apple_image, bomba_image, golden_apple_image])
    apple_rect = Rect(apple_x, apple_y, img.get_width(), img.get_height())
    apples.append({"rect": apple_rect, "image": img})


game_over = False
faults = 0
fall_speed = 10
next_speeder = 10
current_background = background_image1

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == SPAWN_EVENT:
            generate_apples()

    window.blit(current_background, (0, 0))

    window.blit(basket_image, player)

    for apple in apples[:]:
        apple["rect"].y += fall_speed
        window.blit(apple["image"], apple["rect"])

        if apple["image"] == bomba_image and apple["rect"].colliderect(player):
            score -= 5
            apples.remove(apple)
            sound_boom.play()

        elif apple["image"] == golden_apple_image and apple["rect"].colliderect(player):
            score += 5
            apples.remove(apple)
            sound_bonus.play()


        elif apple["rect"].colliderect(player):
            score += 1
            apples.remove(apple)
            sound_catch.play()

            if score >= next_speeder:
                fall_speed += 3
                next_speeder += 10
                sound_speed_up.play()
                current_background = random.choice([background_image1, background_image2, background_image3, background_image4, background_image4])

        elif apple["image"] == bomba_image and apple["rect"].top > window_size[1]:
            apples.remove(apple)

        elif apple["rect"].top > window_size[1]:
            apples.remove(apple)
            faults += 1
            sound_fail.play()

    if faults == 3:
        game_over = True
        sound_game_over.play()
        game_over_text = failed_font.render("GAME OVER",True, (255, 0, 0))
        window.blit(game_over_text, (20, 200))

        record_text = score_font.render(f"Твій рекорд: {int(score)}", True, (255, 0, 0))
        window.blit(record_text, (40, 20))
        display.update()

        time.wait(3000)

        quit()
        break

    score_text = game_font.render(f"{int(score)}", 1, "white")
    center_x = window_size[0] // 2 - 100
    top_y = 40

    padding = 120
    btn_rect = score_text.get_rect(topleft = (center_x, top_y))

    draw.rect(window, (0, 0, 0 ), btn_rect)
    window.blit(score_text, (center_x, top_y))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_a]:
        player.x -= 16
    if keys[K_d]:
        player.x += 16