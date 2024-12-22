import pygame
import random
import os
from sys import exit

pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 50)

# Game Window
size_x = 610
size_y = 610

game_window = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption('Snakes By Prathmesh')

bgImage = pygame.image.load('Snakes.jpg')
bgImage = pygame.transform.scale(bgImage, (size_x, size_y)).convert_alpha()

clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
navy = (0, 255, 255)
blue = (0, 0, 180)
black = (0, 0, 0)


# Game Commands
def showText(text, color, x, y):
    screenScore = font.render(text, True, color)
    game_window.blit(screenScore, [x, y])


def plotSnake(surface, color, List, snakeSize):
    for x, y in List:
        pygame.draw.rect(surface, color, [x, y, snakeSize, snakeSize])


def plotEyesR(surface, color, List, size):
    for x, y in List:
        pygame.draw.rect(surface, color, [x, y, size, size])


def plotEyesL(surface, color, List, size):
    for x, y in List:
        pygame.draw.rect(surface, color, [x, y, size, size])


def wlcScreen():
    exit_screen = False

    while not exit_screen:
        game_window.fill(white)
        showText("Welcome To Snakes", black, 140, 280)
        showText("Press SpaceBar To Play", black, 110, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_screen = True
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    exit_screen = True

        pygame.display.update()
        clock.tick(60)


def gameLoop():
    snake_x = 25
    snake_y = 40
    snakeSize = 20
    snakeLen = 1
    snakeList = []
    apple_x = random.randint(25, 570)
    apple_y = random.randint(40, 570)
    appleSize = 15
    eyesList1 = []
    eyesList2 = []
    speed_x = 0
    speed_y = 0
    score = 0
    exit_game = False
    game_over = False
    fps = 60
    a = 2
    b = 14

    snake_x_1 = snake_x + a
    snake_x_2 = snake_x + b
    snake_y_1 = snake_y + b
    snake_y_2 = snake_y + b

    eyes1 = [snake_x_1, snake_y_1]
    eyes2 = [snake_x_2, snake_y_2]
    eyesList1.append(eyes1)
    eyesList2.append(eyes2)

    plotEyesR(game_window, black, eyesList1, 4)
    plotEyesL(game_window, black, eyesList2, 4)

    if not os.path.exists("Highscore.txt"):
        with open("Highscore.txt", "w") as f:
            f.write("0")

    with open("Highscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("Highscore.txt", "w") as f:
                f.write(str(hiscore))

            game_window.fill(navy)
            showText("Score: " + str(score), blue, 15, 0)
            showText("Hiscore: " + str(hiscore), blue, 390, 0)
            showText("Game Over", red, 200, 300)
            showText("Press Enter To Continue", black, 100, 355)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        snake_x = 25
                        snake_y = 40
                        snakeLen = 1
                        snakeList = []
                        apple_x = random.randint(25, 570)
                        apple_y = random.randint(40, 570)
                        speed_x = 0
                        speed_y = 0
                        score = 0
                        game_over = False
                        snake_x_1 = snake_x + a
                        snake_x_2 = snake_x + b
                        snake_y_1 = snake_y + b
                        snake_y_2 = snake_y + b

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        speed_x = 2
                        speed_y = 0
                        snake_x_1 = snake_x + b
                        snake_x_2 = snake_x + b
                        snake_y_1 = snake_y + a
                        snake_y_2 = snake_y + b

                    if event.key == pygame.K_LEFT:
                        speed_x = -2
                        speed_y = 0
                        snake_x_1 = snake_x + a
                        snake_x_2 = snake_x + a
                        snake_y_1 = snake_y + a
                        snake_y_2 = snake_y + b

                    if event.key == pygame.K_UP:
                        speed_x = 0
                        speed_y = -2
                        snake_x_1 = snake_x + a
                        snake_x_2 = snake_x + b
                        snake_y_1 = snake_y + a
                        snake_y_2 = snake_y + a

                    if event.key == pygame.K_DOWN:
                        speed_x = 0
                        speed_y = 2
                        snake_x_1 = snake_x + a
                        snake_x_2 = snake_x + b
                        snake_y_1 = snake_y + b
                        snake_y_2 = snake_y + b

                    if event.key == pygame.K_TAB:
                        if speed_x > 1:
                            speed_x -= 0.2

                        elif speed_x < -1:
                            speed_x += 0.2

                        if speed_y > 1:
                            speed_y -= 0.2

                        elif speed_y < -1:
                            speed_y += 0.2

            if abs(snake_x - apple_x) < 10 and abs(snake_y - apple_y) < 10:
                score += 10
                apple_x = random.randint(25, 570)
                apple_y = random.randint(40, 570)
                snakeLen += snakeSize

            if score > int(hiscore):
                hiscore = score

            snake_x += speed_x
            snake_y += speed_y
            snake_x_1 += speed_x
            snake_y_1 += speed_y
            snake_x_2 += speed_x
            snake_y_2 += speed_y

            eyes1 = [snake_x_1, snake_y_1]
            eyes2 = [snake_x_2, snake_y_2]
            eyesList1.append(eyes1)
            eyesList2.append(eyes2)

            game_window.fill(white)
            game_window.blit(bgImage, (0, 0))

            showText("Score: " + str(score), blue, 15, 0)
            showText("Hiscore: " + str(hiscore), blue, 390, 0)
            pygame.draw.rect(game_window, red, [apple_x, apple_y, appleSize, appleSize])

            head = [snake_x, snake_y]
            appleInSnake = [apple_x, apple_y]
            snakeList.append(head)

            if appleInSnake in snakeList:
                apple_x = random.randint(25, 570)
                apple_y = random.randint(40, 570)

            if len(eyesList1) and len(eyesList2) > 1:
                del eyesList1[0]
                del eyesList2[0]

            plotSnake(game_window, green, snakeList, snakeSize)
            plotEyesL(game_window, black, eyesList1, 4)
            plotEyesR(game_window, black, eyesList2, 4)

            if len(snakeList) > snakeLen:
                del snakeList[0]
            print(snakeList)

            if head in snakeList[:-1]:
                pygame.mixer.music.load('Hit.mp3')
                pygame.mixer.music.play()
                game_over = True

            if snake_x < 20 or snake_x + snakeSize >= 590 or snake_y < 35 or snake_y + snakeSize >= 585:
                pygame.mixer.music.load('Hit.mp3')
                pygame.mixer.music.play()
                game_over = True

            pygame.draw.rect(game_window, navy, [15, 30, 5, 555])
            pygame.draw.rect(game_window, navy, [15, 585, 575, 5])
            pygame.draw.rect(game_window, navy, [590, 35, 5, 555])
            pygame.draw.rect(game_window, navy, [20, 30, 575, 5])

        pygame.display.update()
        clock.tick(fps)


wlcScreen()

pygame.mixer.music.load('Nagin.mp3')
pygame.mixer.music.play()

gameLoop()

pygame.quit()
exit()
