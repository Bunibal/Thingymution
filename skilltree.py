from Bildermusicsounds import *
from mutations import *

skilltreeslug = [[{"Mutation": getFitness}, {"Mutation": getEvasion}],
                 [{"Mutation": getFast, "Parent": 1}, {"Mutation": getInt, "Parent": 1}]]
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
            for buttoni, button in enumerate(tier):
                pos = self.getplacement(tierNR, buttoni)
                buttonsInTier.append(Mutationbutton(button["Mutation"], pos, (tierNR, buttoni)))
            self.buttons.append(buttonsInTier)

    def getplacement(self, tierindex, buttonindex):
        x = BREITE // (len(self.treeinfo[tierindex]) + 1) * (buttonindex + 1)
        y = POSTIER[tierindex]
        return x, y

    def createImage(self):
        self.image.blit(self.background, (0, 0))
        for tierNR, buttons in enumerate(self.buttons):
            if tierNR == 0:  # Erste Ebene ignoriert
                continue
            buttonsInfo = self.treeinfo[tierNR]
            for index, button in enumerate(buttons):
                parent = buttonsInfo[index]["Parent"]
                endButton = self.buttons[tierNR - 1][parent]
                pygame.draw.line(self.image, WEISS, button.rect.center, endButton.rect.center)

        for tier in self.buttons:
            for button in tier:
                button.blitButton(self.image)

    def blitSkilltree(self, surface, pos):
        surface.blit(self.image, pos)

    def findParent(self, button):
        if button.tier == 0:
            return None
        index = self.treeinfo[button.tier][button.indexInTier]["Parent"]
        return self.buttons[button.tier - 1][index]

    def findChildren(self, button):
        if button.tier == self.tiers - 1:
            return []
        children = []
        for index, button2 in enumerate(self.buttons[button.tier + 1]):
            if self.treeinfo[button.tier + 1][index]["Parent"] == button.indexInTier:
                children.append(button2)
        return children

    def unlock(self, pos):
        button = self.clicked(pos)
        if button == None:
            return None
        if button.tier == 0 or self.findParent(button).unlocked:
            button.unlock()
            button.blitButton(self.image)
            return button.mutation
        return None

    def clicked(self, pos):
        for tier in self.buttons:
            for button in tier:
                if button.checkCollision(pos):
                    return button


class Mutationbutton:
    def __init__(self, mutation, pos, indizes):
        self.font = pygame.font.SysFont("chiller", 50)
        self.mutation = mutation
        self.rect = pygame.rect.Rect(pos, (100, 100))
        self.text = self.font.render(self.mutation["Name"], 1, SCHWARZ)
        self.pos = pos
        self.unlocked = False
        self.indizes = self.tier, self.indexInTier = indizes

    def blitButton(self, screen):
        if self.unlocked:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        else:
            pygame.draw.rect(screen, (100, 100, 0), self.rect)
        screen.blit(self.text, (self.pos[0] + 20, self.pos[1] + 20))

    def checkCollision(self, pos):
        return self.rect.collidepoint(pos)

    def unlock(self):
        self.unlocked = True

    def __str__(self):
        return f"Button mit Index {self.tier}, {self.indexInTier} und Mutation {self.mutation['Name']}"

if __name__ == "__main__":
    s = Skilltree(pygame.surface.Surface((1, 1)), "Schnecke")
    print(s.findChildren(s.buttons[0][1])[1])
    pygame.quit()