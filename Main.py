import pygame
import Player

WIDTH = 1100
HEIGHT = 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frosty's Wrath")


def update():
    win.fill((255,255,255))

    pygame.display.flip()


def main():
    run = True
    luka_is_dumb = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        update()


if __name__ == "__main__":
    main()

pygame.quit()
