import pygame
import Player
import Campfire
import Waves
import TitlePage
import Helper
import EndPage
import Boulder
import Snowman
import random

pygame.mixer.init()

WIDTH = 1100
HEIGHT = 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frosty's Wrath")
pygame.display.set_icon(pygame.image.load('assets/Outersloth.png'))

background = pygame.image.load('assets/Background-snow.png')
trees = pygame.image.load('assets/Background-trees.png')
freezing = pygame.image.load('assets/Freezing.png').convert()
campfires = [pygame.image.load('assets/Campfire-' + str(i) + ".png") for i in range(1, 4)]
outersloth = pygame.image.load('assets/Outersloth-white.png')
rocks = [pygame.image.load("assets/rock-1.png"), pygame.image.load("assets/rock-2.png")]

# right
character_right = [pygame.image.load('assets/Character-right-' + str(i) + ".png") for i in range(1, 3)]
# left
character_left_image1 = pygame.transform.flip(pygame.image.load('assets/Character-right-1.png'), True, False)
character_left_image2 = pygame.transform.flip(pygame.image.load('assets/Character-right-2.png'), True, False)
character_left = [character_left_image1,character_left_image2]
# front
character_front = [pygame.image.load('assets/Character-front-' + str(i) + ".png") for i in range(1, 4)]
# back
character_back = [pygame.image.load('assets/Character-back-' + str(i) + ".png") for i in range(1, 4)]
# shoot
character_shoot = [pygame.image.load('assets/Character-shoot-' + str(i) + ".png") for i in range(1, 4)]
character_leftshoot_image = pygame.transform.flip(pygame.image.load('assets/Character-shoot-1.png'), True, False)
character_shoot.insert(1, character_leftshoot_image)
# wood
woods = pygame.image.load('assets/Wood.png')
# projectiles
fireball_image = pygame.image.load('assets/Fireball.png')
FIREBALL = pygame.transform.scale(fireball_image, (15, 15))
snowball_image = pygame.image.load('assets/Snowball.png')
SMALL_SNOWBALL = pygame.transform.scale(snowball_image, (15, 15))
BIG_SNOWBALL = pygame.transform.scale(snowball_image, (30, 30))
# first snowman
first_snomwan = [pygame.image.load('assets/First-snowman-' + str(i) + ".png") for i in range(1, 4)]
firstsnowman_left_image = pygame.transform.flip(pygame.image.load('assets/First-snowman-3.png'), True, False)
first_snomwan.append(firstsnowman_left_image)
# second_snowman
second_snowman = [pygame.image.load('assets/Second-snowman-' + str(i) + ".png") for i in range(1, 4)]
secondsnowman_left_image = pygame.transform.flip(pygame.image.load('assets/Second-snowman-3.png'), True, False)
second_snowman.append(secondsnowman_left_image)

second_snowman_shooting = [pygame.image.load('assets/Second-snowman-shooting-' + str(i) + ".png") for i in range(1, 4)]
secondsnowman_leftshooting_image = pygame.transform.flip(pygame.image.load('assets/Second-snowman-shooting-3.png'), True, False)
second_snowman_shooting.append(secondsnowman_leftshooting_image)
#thid_snowman
third_snowman = [pygame.image.load('assets/Third-snowman-' + str(i) + ".png") for i in range(1, 4)]
thirdsnowman_left_image = pygame.transform.flip(pygame.image.load('assets/Third-snowman-3.png'), True, False)
third_snowman.append(thirdsnowman_left_image)

third_snowman_shooting = [pygame.image.load('assets/Third-snowman-shooting-' + str(i) + ".png") for i in range(1, 4)]
thirdsnowman_leftshooting_image = pygame.transform.flip(pygame.image.load('assets/Third-snowman-shooting-3.png'), True, False)
third_snowman_shooting.append(thirdsnowman_leftshooting_image)

clock = pygame.time.Clock()
lost = False

# FONTS
pygame.font.init()

pygame.time.set_timer(pygame.USEREVENT, 200)

score = 0
SCORE_FONT = pygame.font.SysFont('comicsans', 60)


def update(player, fireballs, small_snowballs, big_snowballs,campfire, first_snowmen, second_snowmen, third_snowmen,secondsnowman_shooting,thirdsnowman_shooting,boulders, keys, mousepos):
    win.blit(background, (0, 0))

    campfire.draw(win, campfires)

    score_text = SCORE_FONT.render("Score: " + str(score), 1, (255, 255, 0))

    for wood in campfire.wood:
        wood.draw(win,woods)
        if Helper.collide(player.x, player.y, player.WIDTH, player.HEIGHT, wood.x, wood.y):
            campfire.wood.remove(wood)
            if campfire.health < campfire.max_health:
                campfire.health += wood.HEAL_AMOUNT
                if campfire.health > 100:
                    campfire.health = 100

    for fireball in fireballs:
        fireball.draw(win, FIREBALL)
    for snowball in small_snowballs:
        snowball.draw(win, SMALL_SNOWBALL)
    for snowball in big_snowballs:
        snowball.draw(win, BIG_SNOWBALL)

    for firstsnowman in first_snowmen:
        firstsnowman.draw(win, first_snomwan, secondsnowman_shooting)

    for secondsnowman in second_snowmen:
        secondsnowman.draw(win, second_snowman, secondsnowman_shooting)

    for thirdsnowman in third_snowmen:
        thirdsnowman.draw(win, third_snowman, thirdsnowman_shooting)

    win.blit(trees, (0, 0))

    boulders[0].draw(win, player, rocks[0])
    boulders[1].draw(win, player, rocks[1])

    player.draw(win, keys, mousepos, character_right, character_left, character_front, character_back, character_shoot)

    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT - 125))

    player.draw_freezing(win, freezing)
    player.draw_fireball_bar(win, WIDTH)

    win.blit(outersloth, (WIDTH - 70, HEIGHT - 70))

    pygame.display.flip()


def main():
    global lost
    global score

    player = Player.Player(WIDTH // 2, 200, 4)
    campfire = Campfire.Campfire(WIDTH // 2, HEIGHT // 2, 100)

    boulders = [Boulder.Boulder(300, 400, 105, 70), Boulder.Boulder(700, 250, 105, 70)]
    first_snowmen = []
    second_snowmen = []
    third_snowmen = []
    fireballs = []
    small_snowballs = []
    big_snowballs = []

    current_wave = 0

    run = True
    while run:
        clock.tick(60)

        keys = pygame.key.get_pressed()
        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    fireball = player.shoot(mousepos)
                    if fireball is not None:
                        fireballs.append(fireball)

        for fireball in fireballs:
            fireball.move()
            hit = fireball.hit_snowman(first_snowmen)
            if hit is not None:
                hit.take_damage(fireball.damage)
                score += hit.points
                if hit.is_dead():
                    first_snowmen.remove(hit)
                    Waves.waves[current_wave].alive -= 1
                    fireballs.remove(fireball)

            hit = fireball.hit_snowman(second_snowmen)
            if hit is not None:
                hit.take_damage(fireball.damage)
                score += hit.points
                if hit.is_dead():
                    second_snowmen.remove(hit)
                    Waves.waves[current_wave].alive -= 1
                    fireballs.remove(fireball)

            hit = fireball.hit_snowman(third_snowmen)
            if hit is not None:
                hit.take_damage(fireball.damage)
                score += hit.points
                if hit.is_dead():
                    third_snowmen.remove(hit)
                    Waves.waves[current_wave].alive -= 1
                    fireballs.remove(fireball)

            if fireball.hit_boulder(boulders) is not None:
                fireballs.remove(fireball)
            if fireball.is_out_of_bounds(WIDTH, HEIGHT):
                fireballs.remove(fireball)

        for snowball in small_snowballs:
            snowball.move()
            if snowball.hit_goal():
                if snowball.goal == campfire:
                    campfire.take_damage(snowball.damage)
                    small_snowballs.remove(snowball)

            if snowball.is_out_of_bounds(WIDTH, HEIGHT):
                small_snowballs.remove(snowball)

        for snowball in big_snowballs:
            snowball.move()
            if snowball.hit_goal():
                if snowball.goal == campfire:
                    campfire.take_damage(snowball.damage)
                    big_snowballs.remove(snowball)

            if snowball.is_out_of_bounds(WIDTH, HEIGHT):
                big_snowballs.remove(snowball)

        if campfire.health <= 0 or player.time_freezing > 250:
            lost = True
            run = False

        new_first, new_second, new_third = Waves.waves[current_wave].update(WIDTH, HEIGHT, campfire)
        first_snowmen.extend(new_first)
        second_snowmen.extend(new_second)
        third_snowmen.extend(new_third)

        if Waves.waves[current_wave].alive == 0:
            current_wave += 1
            if current_wave >= len(Waves.waves):
                if score <= 500:
                    Snowman.FIRSTSNOWMAN_SPAWN_RATE = 0.05
                    if random.random() < Snowman.FIRSTSNOWMAN_SPAWN_RATE and len(first_snowmen) + len(
                            second_snowmen) < Snowman.TOTAL_SNOWMAN:
                        first_snowmen.append(Snowman.spawn_firstsnowman(WIDTH, HEIGHT, campfire))
                    if random.random() < Snowman.SECONDSNOWMAN_SPAWN_RATE and len(first_snowmen) + len(
                            second_snowmen) < Snowman.TOTAL_SNOWMAN:
                        second_snowmen.append(Snowman.spawn_secondsnowman(WIDTH, HEIGHT, campfire))
                elif score <= 800:
                    Snowman.FIRSTSNOWMAN_SPAWN_RATE = 0.025
                    Snowman.SECONDSNOWMAN_SPAWN_RATE = 0.05
                    if random.random() < Snowman.FIRSTSNOWMAN_SPAWN_RATE:
                        first_snowmen.append(Snowman.spawn_firstsnowman(WIDTH, HEIGHT, campfire))
                    if random.random() < Snowman.SECONDSNOWMAN_SPAWN_RATE:
                        second_snowmen.append(Snowman.spawn_secondsnowman(WIDTH, HEIGHT, campfire))
                    if random.random() < Snowman.THIRDSNOWMAN_SPAWN_RATE:
                        third_snowmen.append(Snowman.spawn_thirdsnowman(WIDTH, HEIGHT, campfire))

        for firstsnowman in first_snowmen:
            if firstsnowman.shoot():
                campfire.health -= firstsnowman.damage
                first_snowmen.remove(firstsnowman)
                Waves.waves[current_wave].alive -= 1
            firstsnowman.move(campfire, boulders)

        for secondsnowman in second_snowmen:
            snowball = secondsnowman.shoot()
            if snowball is not None:
                small_snowballs.append(snowball)
            secondsnowman.move(campfire, boulders)

        for thirdsnowman in third_snowmen:
            snowball = thirdsnowman.shoot()
            if snowball is not None:
                big_snowballs.append(snowball)
            thirdsnowman.move(campfire, boulders)

        campfire.spawn_wood()

        player.update(keys, campfire, boulders)
        update(player, fireballs, small_snowballs, big_snowballs,campfire, first_snowmen, second_snowmen, third_snowmen, second_snowman_shooting, third_snowman_shooting,boulders, keys, mousepos)


if __name__ == "__main__":
    first = True
    while EndPage.retry or first:
        first = False
        EndPage.retry = False
        TitlePage.play(win, background, trees, campfires, outersloth)
        if TitlePage.go_next:
            main()

        if lost:
            EndPage.play(win, WIDTH, HEIGHT, clock, score, outersloth)
            lost = False
            score = 0
            TitlePage.go_next = False


pygame.quit()