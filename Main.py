import pygame
import Player
import Campfire

WIDTH = 1100
HEIGHT = 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frosty's Wrath")

clock = pygame.time.Clock()


def update(player, fireballs, snowballs, campfire):
    win.fill((255,255,255))

    campfire.draw(win)

    for x, projectile in enumerate([*fireballs, *snowballs]):
        projectile.draw(win)

    player.draw(win, WIDTH, HEIGHT)

    pygame.display.flip()


def main():
    player = Player.Player(100, 100, 4)
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
                    fireballs.append(player.shoot(mousepos))
                    campfire.take_damage(5)

        for x, projectile in enumerate([*fireballs, *snowballs]):
            projectile.move()
            if projectile.is_out_of_bounds(WIDTH, HEIGHT):
                if x >= len(fireballs):
                    snowballs.remove(projectile)
                else:
                    fireballs.remove(projectile)

        player.update(keys, campfire)
        update(player, fireballs, snowballs, campfire)


if __name__ == "__main__":
    main()

pygame.quit()
