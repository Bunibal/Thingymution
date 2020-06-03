from Bildermusicsounds import *
from mutations import *

skilltreeslug = [(["neuerdreck", "bla", "bla", "blabla"], [(0, 2), (), (), (1,)]),
                 (["neuerdreck", "bla", "bla", "blabla"], [(), (), (), ()])]
POSTIER4 = HOEHE // 6
POSTIER0 = POSTIER4 * 5
POSTIER1 = POSTIER4 * 4
POSTIER2 = POSTIER4 * 3
POSTIER3 = POSTIER4 * 2
POSTIER = [POSTIER0, POSTIER1, POSTIER2, POSTIER3, POSTIER4]


class Skilltree:
    def __init__(self, background, animal, treeinfo=skilltreeslug, header=None):
        self.background = background
        self.animal = animal
        self.header = header
        self.treeinfo = treeinfo
        self.tiers = len(treeinfo)
        self.buttons = []
        self.image = pygame.Surface(GROESSE)
        self.erstellen()
        self.createImage()

    def erstellen(self):
        for tierNR, tier in enumerate(self.treeinfo):
            buttonsInTier = []
            mutationen = tier[0]
            for buttoni, mut in enumerate(mutationen):
                pos = self.getplacement(tierNR, buttoni)
                buttonsInTier.append(Mutationbutton(mut, pos))
            self.buttons.append(buttonsInTier)

    def getplacement(self, tierindex, buttonindex):
        x = BREITE // (len(self.treeinfo[tierindex][0]) + 1) * (buttonindex + 1)
        y = POSTIER[tierindex]
        return (x, y)

    def createImage(self):
        self.image.blit(self.background, (0, 0))
        for tierNR, buttons in enumerate(self.buttons):
            conns = self.treeinfo[tierNR][1]
            for index, button in enumerate(buttons):
                connsbutton = conns[index]
                for con in connsbutton:
                    endButton = self.buttons[tierNR + 1][con]
                    pygame.draw.line(self.image, WEISS, button.rect.center, endButton.rect.center)
        for tier in self.buttons:
            for button in tier:
                button.blitButton(self.image)

    def blitSkilltree(self, surface, pos):
        surface.blit(self.image, pos)

    def clickedMutation(self, pos):
        for button in self.buttons:
            if button.checkCollision(pos):
                return button.mutation


class Mutationbutton:
    def __init__(self, mutation, pos):
        self.font = pygame.font.SysFont("chiller", 50)
        self.mutation = mutation
        self.rect = pygame.rect.Rect(pos, (100, 100))
        self.text = self.font.render(self.mutation, 1, SCHWARZ)
        self.pos = pos

    def blitButton(self, screen):
        pygame.draw.rect(screen, (100, 100, 0), self.rect)
        screen.blit(self.text, (self.pos[0] + 20, self.pos[1] + 20))

    def checkCollision(self, pos):
        return self.rect.collidepoint(pos)
