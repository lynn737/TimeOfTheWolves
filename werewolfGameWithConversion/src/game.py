import random

import math
import pygame

"""
Audio credits:
"Medieval Modernity" by MASERPAN is licensed under a Attribution-NonCommercial 4.0 International License.
URL: https://freemusicarchive.org/music/maserpan/ambient-soundtracks/medieval-modernity/

"""
def displayText(text,size,x,y,color):
    font = pygame.font.Font("font/Readablegothic-DJW3.ttf", size)
    textSurf = font.render(text, False, color)
    textRect = textSurf.get_rect(center=(x, y))
    screen.blit(textSurf, textRect)

def displayTextLeft(text,size,x,y,color):
    font = pygame.font.Font("font/Readablegothic-DJW3.ttf", size)
    textSurf = font.render(text, False, color)
    textRect = textSurf.get_rect(midleft=(x, y))
    screen.blit(textSurf, textRect)

def distance(x1,y1,x2,y2):
    return math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))

class Game():
    def __init__(self,playerGroup,wolfGroup,barGroup):
        self.playerGroup = playerGroup
        self.wolfGroup = wolfGroup
        self.treeGroup = treeGroup
        self.barGroup = barGroup

        self.wolfCount = 5
        self.villagerCount = 0

    def fight(self):
        playerWolfCollisions = pygame.sprite.groupcollide(self.playerGroup,self.wolfGroup,False,False)
        if playerWolfCollisions:
            collidedWolf = pygame.sprite.spritecollideany(self.playerGroup.sprite,self.wolfGroup)
            if playerGroup.sprite.state == "fight" and collidedWolf.state == "wolf":
                if self.playerGroup.sprite.rect.x < collidedWolf.rect.x:
                    self.playerGroup.sprite.rect.x -= 30
                else:
                    self.playerGroup.sprite.rect.x += 30

                fightParameter = 1.2
                # decide if hunter or wolf are hurt
                randomNums = []
                for i in range(0, 2):
                    num = random.uniform(0, 1)
                    randomNums.append(num)
                randomNumHunter = randomNums[0] * fightParameter
                randomNumWolf = randomNums[1]


                #collidedWolf.hearts -= 1
                if randomNumHunter > randomNumWolf:
                    collidedWolf.hearts -= 1
                else:
                    self.playerGroup.sprite.hearts -= 1

                if collidedWolf.hearts <= 0:
                    collidedWolf.kill()
                    self.wolfCount -= 1
            elif playerGroup.sprite.state == "heal" and collidedWolf.state == "wolf":
                if self.playerGroup.sprite.rect.x < collidedWolf.rect.x:
                    self.playerGroup.sprite.rect.x -= 30
                else:
                    self.playerGroup.sprite.rect.x += 30

                healParameter = 1.1
                # decide if potion works
                randomNums = []
                for i in range(0, 2):
                    num = random.uniform(0, 1)
                    randomNums.append(num)
                randomNumHunter = randomNums[0] * healParameter
                randomNumWolf = randomNums[1]

                #collidedWolf.wolfness -= 1
                if randomNumHunter > randomNumWolf:
                    collidedWolf.wolfness -= 1
                else:
                    self.playerGroup.sprite.hearts -= 1

                if collidedWolf.wolfness <= 0:
                    self.wolfCount -= 1
                    self.villagerCount +=1


    def update(self,playerX,playerY,hearts):
        self.playerGroup.update()
        self.wolfGroup.update(playerX,playerY)
        self.fight()
        self.barGroup.update(playerX,playerY,hearts)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # hunter graphics
        self.hsl = pygame.image.load("images/hunterStandL.png").convert_alpha()
        self.hsr = pygame.image.load("images/hunterStandR.png").convert_alpha()
        self.hwl1 = pygame.image.load("images/hunterWalkL1.png").convert_alpha()
        self.hwl2 = pygame.image.load("images/hunterWalkL2.png").convert_alpha()
        self.hwr1 = pygame.image.load("images/hunterWalkR1.png").convert_alpha()
        self.hwr2 = pygame.image.load("images/hunterWalkR2.png").convert_alpha()
        self.pl1 = pygame.image.load("images/potionwalkL1.png").convert_alpha()
        self.pl2 = pygame.image.load("images/potionwalkL2.png").convert_alpha()
        self.pr1 = pygame.image.load("images/potionwalkR1.png").convert_alpha()
        self.pr2 = pygame.image.load("images/potionwalkR2.png").convert_alpha()

        self.hunterDirection = "L"
        self.image = self.hsl
        self.rect = self.image.get_rect(center=(1100, 400))

        self.walkingIndex = 0

        self.playerTimer = 0

        self.hearts = 5

        self.state = "fight"

    def move(self):
        # keyboard input
        keys = pygame.key.get_pressed()
        # speed deduction if health low
        if self.hearts <= 2:
            speedParameter = 1
        else:
            speedParameter = 2

        # move and change image direction
        if keys[pygame.K_UP]:
            self.rect.y += -speedParameter
        elif keys[pygame.K_DOWN]:
            self.rect.y += speedParameter
        elif keys[pygame.K_LEFT]:
            self.rect.x += -speedParameter
            self.hunterDirection = "L"
        elif keys[pygame.K_RIGHT]:
            self.rect.x += speedParameter
            self.hunterDirection = "R"

        # keep from falling off screen
        if self.rect.x >= screenX:
            self.rect.x -= 2
        elif self.rect.x <= 0:
            self.rect.x += 2
        elif self.rect.y >= screenY:
            self.rect.y -= 2
        elif self.rect.y <= 0:
            self.rect.y += 2

    def walkAnimate(self):
        if self.state == "fight":
            walkingLSurfs = [self.hwl1, self.hwl2]
            walkingRSurfs = [self.hwr1, self.hwr2]
        elif self.state == "heal":
            walkingLSurfs = [self.pl1, self.pl2]
            walkingRSurfs = [self.pr1, self.pr2]
        if (self.playerTimer % 20) == 0:
            self.walkingIndex += 1
            if self.walkingIndex > 1: self.walkingIndex = 0
            if self.hunterDirection == "L":
                self.image = walkingLSurfs[self.walkingIndex]
            elif self.hunterDirection == "R":
                self.image = walkingRSurfs[self.walkingIndex]

    def changeState(self):
        # keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.state == "fight":
                self.state = "heal"
            elif self.state == "heal":
                self.state = "fight"

    def regenerateHearts(self):
        if self.hearts < 5 and self.playerTimer % 500 == 0:
            self.hearts += 1

    def tickTimer(self):
        self.playerTimer += 1

    def update(self):
        self.changeState()
        self.move()
        self.walkAnimate()
        self.regenerateHearts()
        self.tickTimer()


# ----------------------------------------------------------------------------
class Wolf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sl = pygame.image.load("images/werewolfStandL.png").convert_alpha()
        self.wl1 = pygame.image.load("images/werewolfWalkL1.png").convert_alpha()
        self.wl2 = pygame.image.load("images/werewolfWalkL2.png").convert_alpha()
        self.wr1 = pygame.image.load("images/werewolfWalkR1.png").convert_alpha()
        self.wr2 = pygame.image.load("images/werewolfWalkR2.png").convert_alpha()

        # villager left surfs not needed
        self.vl1 = pygame.image.load("images/villagerWalkL1.png").convert_alpha()
        self.vl2 = pygame.image.load("images/villagerWalkL2.png").convert_alpha()
        self.vr1 = pygame.image.load("images/villagerWalkR1.png").convert_alpha()
        self.vr2 = pygame.image.load("images/villagerWalkR2.png").convert_alpha()

        self.image = self.sl
        self.rect = self.image.get_rect(center=(random.uniform(10, 600), random.uniform(10, 400)))
        self.wolfTimer = 0
        self.moveX = 0
        self.moveY = 0

        self.hearts = 5
        self.wolfness = 3

        self.walkingIndex = 0
        self.direction = "L"

        self.state = "wolf"

    def move(self,playerX,playerY):
        distanceToPlayer = distance(playerX,playerY,self.rect.x,self.rect.y)

        speedParameter = 1.3
        if (self.state == "wolf"):
            if (distanceToPlayer <= 400):
                if (playerX > self.rect.x and playerY > self.rect.y):
                    self.moveX = speedParameter
                    self.moveY = speedParameter
                elif (playerX > self.rect.x and playerY < self.rect.y):
                    self.moveX = speedParameter
                    self.moveY = -speedParameter
                elif (playerX < self.rect.x and playerY > self.rect.y):
                    self.moveX = -speedParameter
                    self.moveY = speedParameter
                elif (playerX < self.rect.x and playerY < self.rect.y):
                    self.moveX = -speedParameter
                    self.moveY = -speedParameter
            else:
                if (self.wolfTimer % 50 == 0):
                    self.moveX = random.uniform(-1, 1)
                    self.moveY = random.uniform(-1, 1)

            if self.moveX < 0:
                self.direction = "L"
            else:
                self.direction = "R"

            self.rect.x += self.moveX
            self.rect.y += self.moveY
        elif (self.state == "villager"):
            self.rect.x += 2


        # bouncing off the edge
        if self.rect.x >= screenX:
            self.rect.x -= 10
            self.moveX = -0.5
        elif self.rect.x <= 0:
            self.rect.x += 10
            self.moveX = 0.5
        elif self.rect.y >= screenY:
            self.rect.y -= 10
            self.moveY = -0.5
        elif self.rect.y <= 0:
            self.rect.y += 10
            self.moveY = 0.5

    def walkAnimate(self):
        if self.state == "wolf":
            walkingLSurfs = [self.wl1, self.wl2]
            walkingRSurfs = [self.wr1, self.wr2]
        else:
            walkingLSurfs = [self.vl1, self.vl2]
            walkingRSurfs = [self.vr1, self.vr2]

        if (self.wolfTimer % 20) == 0:
            self.walkingIndex += 1
            if self.walkingIndex > 1: self.walkingIndex = 0
            if self.direction == "L":
                self.image = walkingLSurfs[self.walkingIndex]
            elif self.direction == "R":
                self.image = walkingRSurfs[self.walkingIndex]

    def transformIntoVillager(self):
        if self.wolfness <= 0:
            self.state = "villager"

    def tickTimer(self):
        self.wolfTimer += 1

    def update(self, playerX,playerY):
        self.transformIntoVillager()
        self.move(playerX,playerY)
        self.walkAnimate()
        self.tickTimer()

#-------------------------------------------------------------------------
class Tree(pygame.sprite.Sprite):
    def __init__(self,treeType):
        super().__init__()
        self.liveTree = pygame.image.load("images/liveTree240.png")
        self.deadTree = pygame.image.load("images/deadTree240.png")
        if (treeType == "liveTree"):
            self.image = self.liveTree
        else:
            self.image = self.deadTree
        self.rect = self.image.get_rect(center=(random.uniform(0,600),random.uniform(0,800)))

#-------------------------------------------------------------------------
class Bar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.five = pygame.image.load("images/lifeBar5.png").convert_alpha()
        self.four = pygame.image.load("images/lifeBar4.png").convert_alpha()
        self.three = pygame.image.load("images/lifeBar3.png").convert_alpha()
        self.two = pygame.image.load("images/lifeBar2.png").convert_alpha()
        self.one = pygame.image.load("images/lifeBar1.png").convert_alpha()
        self.image = self.five
        self.rect = self.image.get_rect(center=(0,0))

    def display(self,x,y,hearts):
        self.rect.x = x
        self.rect.y = y
        if (hearts == 5):
            self.image = self.five
        elif (hearts == 4):
            self.image = self.four
        elif (hearts == 3):
            self.image = self.three
        elif (hearts == 2):
            self.image = self.two
        elif (hearts == 1):
            self.image = self.one

    def update(self,x,y,hearts):
        self.display(x,y-40,hearts)



pygame.init()

screenX = 1300
screenY = 900

screen = pygame.display.set_mode((screenX, 900))
clock = pygame.time.Clock()
pygame.display.set_caption("Time of the Wolves")

song = pygame.mixer.Sound("audio/MASERPAN - Medieval Modernity.mp3")
song.set_volume(0.5)
song.play()


# background images/surfs
forest = pygame.Surface((screenX, 900))
forest.fill("darkgreen")
blackSurf = pygame.Surface((screenX, 900))
blackSurf.fill("black")
arcadiaSurf = pygame.image.load("images/arcadia1200x800.png")
arcadiaRect = arcadiaSurf.get_rect(center = (screenX/2,screenY/2))
insigniaSurf = pygame.image.load("images/titleInsignia2,400x600.png")
insigniaRect = insigniaSurf.get_rect(center = (screenX/2,screenY/2))

playerGroup = pygame.sprite.GroupSingle()
playerGroup.add(Player())

wolfGroup = pygame.sprite.Group()

barGroup = pygame.sprite.GroupSingle()
barGroup.add(Bar())

treeGroup = pygame.sprite.Group()
for i in range(5):
    treeGroup.add(Tree("deadTree"))
for i in range(10):
    treeGroup.add(Tree("liveTree"))

game = Game(playerGroup,wolfGroup,barGroup)

gameState = "start"
keyPresses = 0
keyPresses2 = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    if gameState == "playing":
        screen.blit(forest, (0, 0))
        playerGroup.draw(screen)
        wolfGroup.draw(screen)
        treeGroup.draw(screen)
        barGroup.draw(screen)
        game.update(playerGroup.sprite.rect.x,playerGroup.sprite.rect.y,playerGroup.sprite.hearts)

        if (game.playerGroup.sprite.hearts == 0) or (game.wolfCount == 0):
            gameState = "end"

    elif gameState == "start":
        # reset game

        playerGroup.sprite.hearts = 5
        playerGroup.sprite.rect.x = 1200
        playerGroup.sprite.rect.y = 450
        game.wolfCount = 5
        game.villagerCount = 0

        for wolf in wolfGroup:
            wolf.rect.x = 300
            wolf.rect.y = 300
            wolf.wolfness = 3
            wolf.state = "wolf"
            wolf.hearts = 5

        if len(wolfGroup.sprites()) < 5:
            while (len(wolfGroup.sprites()) < 5):
                wolfGroup.add(Wolf())


        screen.blit(blackSurf,(0,0))
        screen.blit(insigniaSurf,insigniaRect)
        displayText("Time of the Wolves",120,screenX/2,100,"darkgray")
        displayText("Vengeance or Mercy?",80,screenX/2,800,"darkgray")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            gameState = "arcadiaPage"

    elif gameState == "arcadiaPage":
        screen.blit(arcadiaSurf,arcadiaRect)
        displayText("A shadow has fallen ",50,400,100,"black")
        displayText("over the land of Arcadia...",50,400,150,"black")
        displayText("<press return>",30,400,200,"black")


        if keyPresses <= 4:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                keyPresses += 1
        else:
            gameState = "missionPage"
            keyPresses = 0
            print(keyPresses)

    elif gameState == "missionPage":
        screen.blit(blackSurf,(0,0))
        displayText("...and you, young hunter, are our only hope.",50,550,100,"yellow")
        displayText("Mission: ",40,screenX/2,(screenY/2 - 100),"dark gray")
        displayText("1. turn at least 3 werewolves into villagers",40,screenX/2,(screenY/2 - 50),"dark gray")
        displayText("2. leave no werewolf alive",40,screenX/2,screenY/2,"dark gray")


        if keyPresses <= 4:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                keyPresses += 1
        else:
            gameState = "weaponsPage"
            keyPresses = 0
            print(keyPresses)

    elif gameState == "weaponsPage":
        swordSurf = pygame.image.load("images/hunterStandL.png")
        potionSurf = pygame.image.load("images/potionwalkL1.png")

        screen.blit(blackSurf,(0,0))
        screen.blit(swordSurf,(screenX/2,250))
        screen.blit(potionSurf,(screenX/2,450))

        displayText("Items",50,screenX/2,100,"dark gray")
        displayText("Sword: to slay werewolves",40,screenX/2,200,"red")
        displayText("Potion: to convert werewolves",40,screenX/2,400,"purple")
        displayText("Press space to toggle between items",40,screenX/2,600,"dark gray")
        displayText("Use arrow keys to move",40,screenX/2,650,"dark gray")

        if keyPresses <= 4:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                keyPresses += 1
        else:
            gameState = "playing"
            keyPresses = 0
            print(keyPresses)

    elif gameState == "end":
        screen.blit(blackSurf,(0,0))

        if playerGroup.sprite.hearts <= 0:
            displayText("You Died.",120,screenX/2,400,"darkgray")
            displayText("Press Enter to Play Again",100,screenX/2,500,"darkgray")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                gameState = "start"

        elif game.villagerCount >= 3:
            displayText("You Won.",120,screenX/2,400,"yellow")
            displayText("Press Enter to Play Again",100,screenX/2,500,"darkgray")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                gameState = "start"
        else:
            displayText("You failed.",120,screenX/2,300,"darkgray")
            displayText("Fewer than 3 villagers were saved.",75, screenX/2,400,"darkgray")
            displayText("Press Enter to Play Again",100,screenX/2,500,"darkgray")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                gameState = "start"





    pygame.display.update()
    clock.tick(60)
