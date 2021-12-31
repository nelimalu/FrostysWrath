import pygame
pygame.font.init()
pygame.mixer.init()

STAT_FONT = pygame.font.Font('assets/Snowby.ttf', 90)
ANIMATION_RATE = 5

campfiresounds = pygame.mixer.music.load("assets/CampfireSounds.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()

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
            self.colour = (0,128,128)
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
    pygame.mixer.music.pause()
    go_next = True
    run = False


def update(win, buttons, background, trees, campfires, animation_step, outersloth):
    win.blit(background, (0, 0))
    win.blit(trees, (0, 0))
    win.blit(campfires[animation_step], (win.get_width() // 2 - 70, win.get_height() // 2 - 70))

    draw_text(win, 80, "FROSTY'S WRATH", (0,0,0))

    for button in buttons:
        button.draw(win)

    win.blit(outersloth, (win.get_width() - 70, win.get_height() - 70))

    pygame.display.flip()


def play(win, background, trees, campfires, outersloth):
    global run

    buttons = [Button(win, 400, "PLAY", 80, 'Typewriter.ttf', cont)]
    animation_step = 0
    frame = 0

    pygame.mixer.music.unpause()

    while run:
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for button in buttons:
                        button.click(mousepos)

        frame += 1
        if frame % ANIMATION_RATE == 0:
            animation_step += 1
        if animation_step == 3:
            animation_step = 0

        for button in buttons:
            button.hover(mousepos)

        update(win, buttons, background, trees, campfires, animation_step, outersloth)
