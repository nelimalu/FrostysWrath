import pygame
import Player
import Campfire
import TitlePage
import Helper

WIDTH = 1100
HEIGHT = 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frosty's Wrath")

background = pygame.image.load('assets/Background-snow.png')
trees = pygame.image.load('assets/Background-trees.png')

clock = pygame.time.Clock()
lost = False


def update(player, fireballs, snowballs, campfire):
    win.blit(background, (0, 0))

    campfire.draw(win)

    for wood in campfire.wood:
        wood.draw(win)
        if Helper.collide(player.x, player.y, player.WIDTH, player.HEIGHT, wood.x, wood.y):
            campfire.wood.remove(wood)
            campfire.health += wood.HEAL_AMOUNT

    for x, projectile in enumerate([*fireballs, *snowballs]):
        projectile.draw(win)

    player.draw(win)

    win.blit(trees, (0, 0))

    player.draw_freezing(win, WIDTH, HEIGHT)

    player.draw_fireball_bar(win, WIDTH)

    pygame.display.flip()


def main():
    global lost

    player = Player.Player(WIDTH // 2, HEIGHT // 2, 4)
    campfire = Campfire.Campfire(WIDTH // 2, HEIGHT // 2, 100)

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
                    campfire.take_damage(5)

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
        player.update(keys, campfire)
        update(player, fireballs, snowballs, campfire)


if __name__ == "__main__":
    TitlePage.play(win)
    if TitlePage.go_next:
        main()

pygame.quit()
