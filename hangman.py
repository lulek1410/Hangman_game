import pygame
import random

pygame.init()


guessed = []
buttons = []
img = 0
screensize = (700, 480)

win = pygame.display.set_mode(screensize)

but_font = pygame.font.SysFont('arial', 20, bold=False, italic=False)

images = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load(
    'hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]


class button(object):
    def __init__(self, let, x, y):
        self.letter = chr(let)
        self.pos_x = x
        self.pos_y = y
        self.color = (255, 255, 255)

    def render(self, win):
        pygame.draw.circle(win, (0, 128, 255), (self.pos_x, self.pos_y), 20, 0)
        pygame.draw.circle(win, (255, 255, 255),
                           (self.pos_x, self.pos_y), 20, 1)


def button_hit(par):
    for i in range(len(buttons)):
        if par[0] < buttons[i].pos_x+20 and par[0] > buttons[i].pos_x-20:
            if par[1] < buttons[i].pos_y+20 and par[1] > buttons[i].pos_y-20:
                return buttons[i]
    return None


def word_gen():
    f = open('word.txt', 'r')
    lines = f.readlines()
    return lines[random.randrange(len(lines))]


def spaced_out(password, guessed=[]):
    spaced_word = ''
    guessed_letters = guessed
    for x in password:
        if x != ' ' and x != '\n':
            spaced_word += '_ '
            for i in guessed_letters:
                if x == i:
                    spaced_word = spaced_word[:-2]
                    spaced_word += x + ' '
        elif x == ' ':
            spaced_word += '   '
    return spaced_word


def hang(password, letter):
    if letter not in password:
        return True
    return False


def end(word, password, img, win):
    count_word, count_password = 0, 0
    for x in word:
        if x != ' ' and x != '_' and x != '\n':
            count_word += 1
    for x in password:
        if x != ' ' and x != '\n':
            count_password += 1
    if count_password == count_word or img == 6:
        win.blit(images[6],
                 (screensize[0]/2 - 70, screensize[1]/2-130))
        return True
    else:
        return False


def gen_buttons():
    increase = round((screensize[0])/13)
    for i in range(26):
        if i < 13:
            x = 25+increase*i
            y = 25
        else:
            x = 25+increase*(i-13)
            y = 70
        buttons.append(button(65+i, x, y))
    return buttons


def end_win():
    global img
    win.fill((110, 140, 60))
    if img == 6:
        text = but_font.render("You lost!", 0, (0, 0, 0))
    else:
        text = but_font.render("You Win!", 0, (0, 0, 0))
    again = but_font.render(
        "Press spacebar to play again.", 0, (0, 0, 0))
    win.blit(text, (screensize[0]/2-40, screensize[1]/2-100))
    win.blit(again, (screensize[0]/2-100, screensize[1]/2))
    pygame.display.update()


def Game():
    global guessed
    global buttons
    global img
    # generate environment
    buttons = gen_buttons()

    password = word_gen()
    print(password)

    run = True
    while run:
        # time
        pygame.time.delay(20)
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if end(spaced_out(password, guessed), password, img, win) == True:
                    if event.key == pygame.K_SPACE:
                        print('a')
                        img = 0
                        guessed = []
                        password = word_gen()
                        buttons.clear()
                        buttons = gen_buttons()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                if button_hit(click_pos) != None:
                    guessed.append(button_hit(click_pos).letter)
                    if hang(password, button_hit(click_pos).letter):
                        if img < 7:
                            img += 1
                    buttons.remove(button_hit(click_pos))
                # draw
        win.fill((110, 140, 60))

        for i in range(len(buttons)):
            buttons[i].render(win)
            text = but_font.render(buttons[i].letter, 0, (0, 0, 0))
            win.blit(text, (buttons[i].pos_x-6, buttons[i].pos_y-12))
        if img < 7:
            win.blit(images[img],
                     (screensize[0]/2 - 70, screensize[1]/2-130))

        text = but_font.render(spaced_out(password, guessed), 1, (0, 0, 0))
        rectangle = text.get_rect()
        win.blit(text, (screensize[0]/2 - rectangle[2]/2, 350))
        if end(spaced_out(password, guessed), password, img, win) == True:
            end_win()
        pygame.display.update()


Game()
pygame.quit()
