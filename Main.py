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
#right
character_right = [pygame.image.load('assets/Character-right-' + str(i) + ".png") for i in range(1, 3)]
#left
character_left_image1 = pygame.transform.flip(pygame.image.load('assets/Character-right-1.png'), True, False)
character_left_image2 =  pygame.transform.flip(pygame.image.load('assets/Character-right-2.png'), True, False)
character_left = [character_left_image1,character_left_image2]
#front
character_front = [pygame.image.load('assets/Character-front-' + str(i) + ".png") for i in range(1, 4)]
#back
character_back = [pygame.image.load('assets/Character-back-' + str(i) + ".png") for i in range(1, 4)]
#shoot
character_shoot = [pygame.image.load('assets/Character-shoot-' + str(i) + ".png") for i in range(1, 4)]
character_leftshoot_image = pygame.transform.flip(pygame.image.load('assets/Character-shoot-1.png'), True, False)
character_shoot.insert(1, character_leftshoot_image)



clock = pygame.time.Clock()
lost = False

# FONTS
pygame.font.init()

pygame.time.set_timer(pygame.USEREVENT, 200)

score = 0
SCORE_FONT = pygame.font.SysFont('comicsans', 60)


def update(player, fireballs, snowballs, campfire, snowmen, boulders, keys, mousepos):
    win.blit(background, (0, 0))

    campfire.draw(win, campfires)

    score_text = SCORE_FONT.render(str(score), 1, (255, 255, 0))

    for wood in campfire.wood:
        wood.draw(win)
        if Helper.collide(player.x, player.y, player.WIDTH, player.HEIGHT, wood.x, wood.y):
            campfire.wood.remove(wood)
            if campfire.health < campfire.max_health:
                campfire.health += wood.HEAL_AMOUNT
                if campfire.health > 100:
                    campfire.health = 100

    for x, projectile in enumerate([*fireballs, *snowballs]):
        projectile.draw(win)

    player.draw(win, keys, mousepos, character_right, character_left, character_front, character_back, character_shoot)

    for snowman in snowmen:
        snowman.draw(win)

    win.blit(trees, (0, 0))

    for boulder in boulders:
        boulder.draw(win, player)

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

    boulders = [Boulder.Boulder(350, 300, 50, 70)]
    snowmen = []
    first_snowmen = []
    second_snowmen = []
    third_snowmen = []
    fireballs = []
    snowballs = []

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
                    print(mousepos)
                    fireball = player.shoot(mousepos)
                    if fireball is not None:
                        fireballs.append(fireball)
                    # campfire.take_damage(5)

        for fireball in fireballs:
            fireball.move()
            hit = fireball.hit_snowman(snowmen)
            if hit is not None:
                hit.take_damage(fireball.damage)
                score += hit.points
                if hit.is_dead():
                    snowmen.remove(hit)
                    fireballs.remove(fireball)
            if fireball.is_out_of_bounds(WIDTH, HEIGHT):
                fireballs.remove(fireball)

        for snowball in snowballs:
            snowball.move()
            if snowball.hit_goal():
                if snowball.goal == campfire:
                    campfire.take_damage(snowball.damage)
                    snowballs.remove(snowball)

            if snowball.is_out_of_bounds(WIDTH, HEIGHT):
                snowballs.remove(snowball)

        if campfire.health <= 0 or player.time_freezing > 250:
            lost = True
            run = False

        if random.random() < Snowman.SNOWMAN_SPAWN_RATE:
            snowmen.append(Snowman.spawn_snowman(WIDTH, HEIGHT, campfire))

        for snowman in snowmen:
            snowball = snowman.shoot()
            if snowball is not None:
                snowballs.append(snowball)
            snowman.move()

        campfire.spawn_wood()
        player.update(keys, campfire)
        update(player, fireballs, snowballs, campfire, snowmen, boulders, keys, mousepos)


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