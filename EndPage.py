import pygame
import pygame.gfxdraw
import TitlePage
pygame.font.init()

FONT = pygame.font.Font('assets/Typewriter.ttf', 100)
SUB_FONT = pygame.font.Font('assets/Typewriter.ttf', 40)
run = True
retry = False


def highscore(score):
    with open("highscore.txt", "r") as file:
        temp = file.read()
        current = temp.split('\n')[0]

    if score > int(current):
        with open("highscore.txt", "w") as file:
            file.write(str(score))
            file.write("\ndont cheat >:(")
            return score
    return current


def next_game():
    global run, retry
    run = False
    retry = True
    TitlePage.go_next = False
    TitlePage.run = True


def play(win, width, height, clock, score):
    global run, retry
    run = True

    best_score = highscore(score)

    string = "Game Over"
    game_over_text = FONT.render(string, 1, (0, 0, 0))
    pygame.gfxdraw.filled_polygon(win, ((0, 0), (0, height), (width, height), (width, 0)), (200, 20, 20, 175))
    for i in range(-1, len(string)):
        if not run:
            break
        text = FONT.render(string[:i + 1], True, (0, 0, 0))
        win.blit(text, (width // 2 - game_over_text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.update()
        clock.tick(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    clock.tick(60)
    text = SUB_FONT.render("Highscore: " + str(best_score), 1, (0, 0, 0))
    win.blit(text, (width // 2 - text.get_width() // 2, height // 2 + 70))
    pygame.display.flip()

    buttons = [TitlePage.Button(win, height // 2 + 150, "Main Menu", 40, "Typewriter.ttf", next_game)]

    while run:
        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                retry = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for button in buttons:
                        button.click(mousepos)

        for button in buttons:
            button.hover(mousepos)
            button.draw(win)

        pygame.display.flip()
