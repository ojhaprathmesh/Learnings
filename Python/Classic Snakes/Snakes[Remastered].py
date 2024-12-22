import pygame
from random import randint
import os
from sys import exit

pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 50)

# Game Window
sizeX = 610
sizeY = 610

gameWindow = pygame.display.set_mode((sizeX, sizeY))
pygame.display.set_caption('Snakes By Prathmesh')

bgImage = pygame.image.load('Snakes.jpg')
bgImage = pygame.transform.scale(bgImage, (sizeX, sizeY)).convert_alpha()

clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 180)
black = (0, 0, 0)

# Game Variables
snakeX, snakeY = 25, 40
speedX, speedY = 0, 0
appleX, appleY = randint(25, 570), randint(40, 570)
a, b = 14, 2
c, d = 14, 14
fps = 90
score = 0
snakeLen = 1
snakeList = [[25, 40]]
exitGame, gameOver = False, False
snakeSize, appleSize, eyeSize = 20, 15, 4


# Game Objects
class snake(object):
    def __init__(self, x, y, Size):
        self.x = x
        self.y = y
        self.size = Size
        self.hitBox = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        mainSnake.hitBox = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(gameWindow, green, mainSnake.hitBox, 10)


class apple(object):
    def __init__(self, x, y, Size):
        self.x = x
        self.y = y
        self.size = Size
        self.hitBox = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        mainApple.hitBox = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(gameWindow, red, mainApple.hitBox, 2)


# Game Commands
def showText(text, color, x, y):
    screenScore = font.render(text, True, color)
    gameWindow.blit(screenScore, [x, y])


def drawRect(surface, color, List):
    pygame.draw.rect(surface, color, List)


def wlcScreen():
    exitScreen = False

    while not exitScreen:
        gameWindow.fill(white)
        showText("Welcome To Snakes", black, 140, 280)
        showText("Press SpaceBar To Play", black, 110, 330)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                exitScreen = True
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    exitScreen = True

        pygame.display.update()


def snakeCollision():
    global gameOver, abc
    if snakeX <= 15 or snakeX >= 575:
        gameOver = True
    if snakeY <= 30 or snakeY >= 585:
        gameOver = True
    try:
        if mainHead.hitBox.colliderect(mainSnake.hitBox) and snakeLen > 21:
            gameOver = True

    except NameError:
        pass


def createBorder():
    drawRect(gameWindow, cyan, [15, 30, 5, 555])
    drawRect(gameWindow, cyan, [15, 585, 575, 5])
    drawRect(gameWindow, cyan, [590, 35, 5, 555])
    drawRect(gameWindow, cyan, [20, 30, 575, 5])


# def gameLoop():
# global gameOver
if not os.path.exists("Highscore.txt"):
    with open("Highscore.txt", "w") as f:
        f.write("0")

with open("Highscore.txt", "r") as f:
    hiscore = f.read()

while not exitGame:
    mainEvent = pygame.event.get()
    if gameOver:
        gameWindow.fill(cyan)
        showText("Score: " + str(score), blue, 15, 0)
        showText("Hiscore: " + str(hiscore), blue, 390, 0)
        showText("Game Over", red, 200, 300)
        showText("Press Enter To Continue", black, 100, 355)

        for event in mainEvent:
            if event.type == pygame.KEYDOWN:
                gameOver = False
        score = 0
        snakeLen = 1
        a, b = 14, 2
        c, d = 14, 14
        speedX, speedY = 0, 0
        snakeX, snakeY = 25, 40
        appleX, appleY = randint(25, 570), randint(40, 570)

    else:
        gameWindow.fill(white)
        gameWindow.blit(bgImage, (0, 0))

        with open("Highscore.txt", "w") as f:
            f.write(str(hiscore))
        showText("Score: " + str(score), blue, 15, 0)
        showText("Hiscore: " + str(hiscore), blue, 390, 0)

        for event in mainEvent:
            if event.type == pygame.QUIT:
                exitGame = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    a = snakeSize - 6
                    b = snakeSize - 18
                    c = snakeSize - 6
                    d = snakeSize - 6
                    speedX = 2
                    speedY = 0

                if event.key == pygame.K_LEFT:
                    a = snakeSize - 18
                    b = snakeSize - 6
                    c = snakeSize - 18
                    d = snakeSize - 18
                    speedX = -2
                    speedY = 0

                if event.key == pygame.K_DOWN:
                    a = snakeSize - 6
                    b = snakeSize - 6
                    c = snakeSize - 18
                    d = snakeSize - 6
                    speedX = 0
                    speedY = 2

                if event.key == pygame.K_UP:
                    a = snakeSize - 18
                    b = snakeSize - 18
                    c = snakeSize - 6
                    d = snakeSize - 18
                    speedX = 0
                    speedY = -2

        snakeX = snakeX + speedX
        snakeY = snakeY + speedY
        eyeX1 = snakeX + a
        eyeY1 = snakeY + b
        eyeX2 = snakeX + c
        eyeY2 = snakeY + d

        snakeHead = [snakeX, snakeY]
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLen:
            del snakeList[0]

        # if len(snakeList) < 2:
        #     snakeList = [[25, 40], [25, 40]]

        if score > int(hiscore):
            hiscore = score

        mainApple = apple(appleX, appleY, appleSize)
        drawRect(gameWindow, red, [appleX, appleY, appleSize, appleSize])  # Apple
        if len(snakeList) < 2:
            for i, j in snakeList:
                mainSnake = snake(snakeX, snakeY, snakeSize)  # Snake
                drawRect(gameWindow, green, [i, j, snakeSize, snakeSize])
        else:
            mainHead = snake(snakeList[0][0], snakeList[0][1], snakeSize)
            drawRect(gameWindow, green, [snakeList[0][0], snakeList[0][1], snakeSize, snakeSize])
            for i, j in snakeList[1:]:
                mainSnake = snake(snakeX, snakeY, snakeSize)  # Snake
                drawRect(gameWindow, green, [i, j, snakeSize, snakeSize])

        drawRect(gameWindow, black, [eyeX1, eyeY1, eyeSize, eyeSize])  # Right Eye
        drawRect(gameWindow, black, [eyeX2, eyeY2, eyeSize, eyeSize])  # Left Eye

        if mainSnake.hitBox.colliderect(mainApple.hitBox):
            score += 1
            snakeLen += snakeSize
            appleX, appleY = randint(25, 570), randint(40, 570)

        snakeCollision()
        createBorder()

    pygame.display.update()
    clock.tick(fps)

# wlcScreen()

# gameLoop()

pygame.quit()
exit()
