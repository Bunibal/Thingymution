from Bildermusicsounds import *

# Widget-Klassen
class ButtonNormal:
    def __init__(self, pos, label):
        self.font = FONT1
        self.pos, self.label = pos, label
        self.rect = pygame.rect.Rect(self.pos, (GROESSEBUTTONS, GROESSEBUTTONS // 5))
        self.text = self.font.render(self.label, 1, SCHWARZ)

    def blitButton(self, screen):
        pygame.draw.rect(screen, (100, 100, 0), self.rect)
        screen.blit(self.text, (self.pos[0] + 20, self.pos[1] + 20))

    def checkCollision(self, pos):
        return self.rect.collidepoint(pos)


class ButtonGame(ButtonNormal):
    def __init__(self, pos, label):
        ButtonNormal.__init__(self, pos, label)
        self.rect = pygame.rect.Rect(self.pos, (GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5))

    def blitButton(self, screen):
        screen.blit(buttons1, self.rect)
        screen.blit(self.text, (self.pos[0] + 20, self.pos[1] + 20))


class TextFeld:
    def __init__(self, pos, initText, font, laenge=400):
        self.pos = pos
        self.font = font
        self.text = initText
        self.rendered = font.render(self.text, 1, WEISS)
        self.laenge = laenge

    def blitTextFeld(self, screen):
        pygame.draw.rect(screen, SCHWARZ,
                         (self.pos, (self.laenge, 60)))
        screen.blit(self.rendered, self.pos)

    def keystroke(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text = self.text + event.unicode
        self.rendered = self.font.render(self.text, 1, WEISS)
