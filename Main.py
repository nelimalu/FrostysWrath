import pygame
import Player
import Campfire
import Snowman
import TitlePage
import Helper
import random
import EndPage
import Boulder

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
character_left_image2 =  pygame.transform.flip(pygame.image.load('assets/Character-right-2.png'), True, False)
character_left = [character_left_image1,character_left_image2]
# front
character_front = [pygame.image.load('assets/Character-front-' + str(i) + ".png") for i in range(1, 4)]
# back
character_back = [pygame.image.load('assets/Character-back-' + str(i) + ".png") for i in range(1, 4)]
# shoot
character_shoot = [pygame.image.load('assets/Character-shoot-' + str(i) + ".png") for i in range(1, 4)]
character_leftshoot_image = pygame.transform.flip(pygame.image.load('assets/Character-shoot-1.png'), True, False)
character_shoot.insert(1, character_leftshoot_image)
#wood
woods = pygame.image.load('assets/Wood.png')
#projectiles
fireball_image = pygame.image.load('assets/Fireball.png')
FIREBALL = pygame.transform.scale(fireball_image, (15, 15))
snowball_image = pygame.image.load('assets/Snowball.png')
SMALL_SNOWBALL = pygame.transform.scale(snowball_image, (15, 15))
BIG_SNOWBALL = pygame.transform.scale(snowball_image, ( 25, 25))
#first snowman
first_snomwan = [pygame.image.load('assets/First-snowman-' + str(i) + ".png") for i in range(1, 4)]
firstsnowman_left_image = pygame.transform.flip(pygame.image.load('assets/First-snowman-3.png'), True, False)
first_snomwan.append(firstsnowman_left_image)
#second_snowman
second_snowman = [pygame.image.load('assets/Second-snowman-' + str(i) + ".png") for i in range(1, 4)]
secondsnowman_left_image = pygame.transform.flip(pygame.image.load('assets/Second-snowman-3.png'), True, False)
second_snowman.append(secondsnowman_left_image)


clock = pygame.time.Clock()
lost = False

# FONTS
pygame.font.init()

pygame.time.set_timer(pygame.USEREVENT, 200)

score = 0
SCORE_FONT = pygame.font.SysFont('comicsans', 60)


def update(player, fireballs, small_snowballs, big_snowballs,campfire, first_snowmen, second_snowmen, third_snowmen,boulders, keys, mousepos):
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

    for firstsnowman in first_snowmen:
        firstsnowman.draw(win, first_snomwan)

    for secondsnowman in second_snowmen:
        secondsnowman.draw(win, second_snowman)

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

    boulders = [Boulder.Boulder(300, 300, 105, 70), Boulder.Boulder(700, 250, 105, 70)]
    snowmen = []
    first_snowmen = []
    second_snowmen = []
    third_snowmen = []
    fireballs = []
    small_snowballs = []
    big_snowballs = []

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
                    fireballs.remove(fireball)
            hit = fireball.hit_snowman(second_snowmen)
            if hit is not None:
                hit.take_damage(fireball.damage)
                score += hit.points
                if hit.is_dead():
                    second_snowmen.remove(hit)
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

        if campfire.health <= 0 or player.time_freezing > 250:
            lost = True
            run = False

        #luka change this for the waves
        if score <= 200:
            if random.random() < Snowman.FIRSTSNOWMAN_SPAWN_RATE:
                first_snowmen.append(Snowman.spawn_firstsnowman(WIDTH, HEIGHT, campfire))
        elif score <= 500:
            Snowman.FIRSTSNOWMAN_SPAWN_RATE = 0.05
            if random.random() < Snowman.FIRSTSNOWMAN_SPAWN_RATE and len(first_snowmen) + len(second_snowmen) < Snowman.TOTAL_SNOWMAN:
                first_snowmen.append(Snowman.spawn_firstsnowman(WIDTH, HEIGHT, campfire))
            if random.random() < Snowman.SECONDSNOWMAN_SPAWN_RATE and len(first_snowmen) + len(second_snowmen) < Snowman.TOTAL_SNOWMAN:
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
            firstsnowman.move(campfire)

        for secondsnowman in second_snowmen:
            snowball = secondsnowman.shoot()
            if snowball is not None:
                small_snowballs.append(snowball)
            secondsnowman.move(campfire)

        campfire.spawn_wood()

        player.update(keys, campfire, boulders)
        update(player, fireballs, small_snowballs, big_snowballs,campfire, first_snowmen, second_snowmen, third_snowmen,boulders, keys, mousepos)


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