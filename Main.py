import pygame
import Player
import Campfire
import Snowman
import TitlePage
import Helper
import random
import EndPage

# update

WIDTH = 1100
HEIGHT = 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frosty's Wrath")

background = pygame.image.load('assets/Background-snow.png')
trees = pygame.image.load('assets/Background-trees.png')
freezing = pygame.image.load('assets/Freezing.png').convert()
campfires = [pygame.image.load('assets/Campfire-' + str(i) + ".png") for i in range(1, 4)]

clock = pygame.time.Clock()
lost = False

# FONTS
pygame.font.init()

pygame.time.set_timer(pygame.USEREVENT, 200)

score = 0
SCORE_FONT = pygame.font.SysFont('comicsans', 60)


def update(player, fireballs, snowballs, campfire, snowmen):
    win.blit(background, (0, 0))

    campfire.draw(win, campfires)

    score_text = SCORE_FONT.render(str(score), 1, (255, 255, 0))

    for wood in campfire.wood:
        wood.draw(win)
        if Helper.collide(player.x, player.y, player.WIDTH, player.HEIGHT, wood.x, wood.y):
            campfire.wood.remove(wood)
            if campfire.health < campfire.max_health:
                campfire.health += wood.HEAL_AMOUNT

    for x, projectile in enumerate([*fireballs, *snowballs]):
        projectile.draw(win)

    player.draw(win)

    for snowman in snowmen:
        snowman.draw(win)

    win.blit(trees, (0, 0))

    win.blit(score_text, (WIDTH//2 - score_text.get_width() // 2, HEIGHT-125))

    player.draw_freezing(win, freezing)
    player.draw_fireball_bar(win, WIDTH)

    pygame.display.flip()


def main():
    global lost
    global score

    player = Player.Player(WIDTH // 2, 200, 4)
    campfire = Campfire.Campfire(WIDTH // 2, HEIGHT // 2, 100)

    snowmen = []
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
        update(player, fireballs, snowballs, campfire, snowmen)


if __name__ == "__main__":
    first = True
    while EndPage.retry or first:
        first = False
        EndPage.retry = False
        TitlePage.play(win)
        if TitlePage.go_next:
            main()

        if lost:
            EndPage.play(win, WIDTH, HEIGHT, clock, score)
            lost = False
            TitlePage.go_next = False


pygame.quit()
