import pygame
import Player
import Campfire
import Snowmen
import TitlePage
import Helper

WIDTH = 1100
HEIGHT = 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frosty's Wrath")

background = pygame.image.load('assets/Background-snow.png')
trees = pygame.image.load('assets/Background-trees.png')
freezing = pygame.image.load('assets/Freezing.png').convert()

clock = pygame.time.Clock()
ticks = 0
lost = False


def update(player, fireballs, snowballs, campfire, snowmen):
    win.blit(background, (0, 0))

    campfire.draw(win)


    for wood in campfire.wood:
        wood.draw(win)
        if Helper.collide(player.x, player.y, player.WIDTH, player.HEIGHT, wood.x, wood.y):
            campfire.wood.remove(wood)
            if campfire.health < campfire.max_health:
                campfire.health += wood.HEAL_AMOUNT

    for x, projectile in enumerate([*fireballs, *snowballs]):
        projectile.draw(win)

    player.draw(win)

    win.blit(trees, (0, 0))

    for snowman in snowmen.snowmans:
        snowman.draw(win)

    player.draw_freezing(win, freezing)
    player.draw_fireball_bar(win, WIDTH)

    pygame.display.flip()


def main():
    global lost

    player = Player.Player(WIDTH // 2, HEIGHT // 2, 4)
    campfire = Campfire.Campfire(WIDTH // 2, HEIGHT // 2, 100)
    snowmen = Snowmen.Snowmen((0,0), 20, 5, 2)

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

        for x, projectile in enumerate([*fireballs, *snowballs]):
            projectile.move()
            if projectile.is_out_of_bounds(WIDTH, HEIGHT):
                if x >= len(fireballs):
                    snowballs.remove(projectile)
                else:
                    fireballs.remove(projectile)

        if player.time_freezing > 250:
            lost = True
            run = False

        campfire.spawn_wood()
        snowmen.spawn_snowman()
        player.update(keys, campfire)
        update(player, fireballs, snowballs, campfire, snowmen)


if __name__ == "__main__":
    TitlePage.play(win)
    if TitlePage.go_next:
        main()

pygame.quit()
