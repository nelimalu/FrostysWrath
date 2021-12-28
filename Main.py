import pygame
import Player

WIDTH = 1100
HEIGHT = 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frosty's Wrath")

clock = pygame.time.Clock()


def update(player, fireballs, snowballs):
    win.fill((255,255,255))

    player.draw(win)

    for x, projectile in enumerate([*fireballs, *snowballs]):
        projectile.draw(win)

    pygame.display.flip()


def main():
    player = Player.Player(100, 100, 1)

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
                fireballs.append(player.shoot(mousepos))

        for x, projectile in enumerate([*fireballs, *snowballs]):
            projectile.move()
            if projectile.is_out_of_bounds(WIDTH, HEIGHT):
                if x >= len(fireballs):
                    snowballs.remove(projectile)
                else:
                    fireballs.remove(projectile)

        player.move(keys)
        update(player, fireballs, snowballs)


if __name__ == "__main__":
    main()

pygame.quit()
