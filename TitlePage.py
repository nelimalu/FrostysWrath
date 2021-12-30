import pygame
pygame.font.init()

STAT_FONT = pygame.font.Font('assets/Snowby.ttf', 100)

go_next = False
run = True

# update


def draw_text(win, y, text, colour):
    text = STAT_FONT.render(text, True, colour)
    x = (win.get_width() // 2) - (text.get_width() // 2)
    win.blit(text, (x, y))


class Button:
    def __init__(self, win, y, string_text, size, font, target):
        self.y = y
        self.colour = (0, 0, 0)
        self.string_text = string_text
        self.target = target
        self.font = pygame.font.Font("assets/" + font, size)
        self.text = self.font.render(self.string_text, 1, self.colour)
        self.x = (win.get_width() // 2) - (self.text.get_width() // 2)

    def hover(self, mousepos):
        if self.x <= mousepos[0] <= self.x + self.text.get_width() and \
                self.y <= mousepos[1] <= self.text.get_height() + self.y:
            self.colour = (0, 200, 0)
            self.text = self.font.render(self.string_text, True, self.colour)
        else:
            self.colour = (0, 0, 0)
            self.text = self.font.render(self.string_text, 1, self.colour)

    def click(self, mousepos):
        if self.x <= mousepos[0] <= self.x + self.text.get_width() and \
                self.y <= mousepos[1] <= self.text.get_height() + self.y:
            self.target()

    def draw(self, win):
        win.blit(self.text, (self.x, self.y))


def cont():
    global run, go_next
    go_next = True
    run = False


def update(win, buttons):
    win.fill((255,255,255))

    draw_text(win, 30, "FROSTY'S WRATH", (0,0,0))

    for button in buttons:
        button.draw(win)

    pygame.display.flip()


def play(win):
    global run

    buttons = [Button(win, 200, "P LAY", 80, 'Snowby.ttf', cont)]

    while run:
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for button in buttons:
                        button.click(mousepos)

        for button in buttons:
            button.hover(mousepos)

        update(win, buttons)
