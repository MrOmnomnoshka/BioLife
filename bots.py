import pygame
import random

pygame.init()

size = width, height = 1200, 800
length = 5

# ЦВЕТА
black = 0, 0, 0  # фон
white = 255, 255, 255  # труп
red = 255, 0, 0  # яд
blue = 0, 32, 255  # бот
green = 0, 192, 0  # еда
gray = 224, 224, 224  # хз
brown = 160, 128, 96  # забор
# //////////////////////////////////

# Создание массива карты
Map = []
map_width = int(width / length)
map_height = int(height / length)
    # 1 - пустота, 2 - стена, 3 - бот, 4 - еда, 5 - труп, 6 - яд.
Map.append([])
for el in range(map_width):
    Map[0].append(2)

for el in range(map_height - 2):    # 2222222222
    Map.append([])                  # 2111111112
    Map[el + 1].append(2)           # 2111111112  -  что-то типо такого
    for e in range(map_width - 2):  # 2111111112
        Map[el + 1].append(1)       # 2222222222
    Map[el + 1].append(2)

Map.append([])
for num in range(map_width):
    Map[map_height - 1].append(2)
# /////////////////////////////////////


class Bot:
    def __init__(self, x_bot, y_bot, number, counter,  energy):
        self.x_bot = x_bot
        self.y_bot = y_bot
        self.number = number
        self.counter = counter
        self.energy = energy
        self.dna = []

        for gen in range(64):
            self.dna.append(random.randint(0, 63))
            # print("[", gen, "] =", self.dna[gen])

    def draw(self):
        pygame.draw.rect(screen, blue, [self.x_bot, self.y_bot, length, length])

    def move(self):
        self.energy -= 1
        """
        print("move:")
        print("dna here = ", self.dna[i])
        print("============")
        pygame.time.delay(500)
        """
        old_x = self.x_bot
        old_y = self.y_bot
        Map[int(self.y_bot / length)][int(self.x_bot / length)] = 1

        if self.dna[self.counter] == 0:
            self.y_bot -= length

        if self.dna[self.counter] == 1:
            self.x_bot += length
            self.y_bot -= length

        if self.dna[self.counter] == 2:
            self.x_bot += length

        if self.dna[self.counter] == 3:
            self.x_bot += length
            self.y_bot += length

        if self.dna[self.counter] == 4:
            self.y_bot += length

        if self.dna[self.counter] == 5:
            self.x_bot -= length
            self.y_bot += length

        if self.dna[self.counter] == 6:
            self.x_bot -= length

        if self.dna[self.counter] == 7:
            self.x_bot -= length
            self.y_bot -= length

        coord = Map[int(self.y_bot / length)][int(self.x_bot / length)]
        if coord == 2 or coord == 3:  # Если там бот или стена
            self.x_bot = old_x
            self.y_bot = old_y
            # print("бот", self.number, "не походил")
        elif coord == 4 or coord == 5:  # Если там еда или труп
            self.energy += 10
            # print("бот", self.number, "съел еду")
        # else:
            # print("бот", self.number, "походил")

        Map[int(self.y_bot / length)][int(self.x_bot / length)] = 3

    '''
    def look(self):
        #  LOOK

    def photo(self):
        #  Fotosintez
    '''

# Создаем ботов, еду
bots = []
BotsAmount = 10
FoodAmount = 200
for n in range(BotsAmount):
    x = random.randint(1, (width / length) - 2) * length  # x - для удобства
    y = random.randint(1, (height / length) - 2) * length  # y - для удобства
    Map[int(y / length)][int(x / length)] = 3
    bots.append(Bot(x, y, n, 0, 100))

for f in range(FoodAmount):
    x = random.randint(1, (width / length) - 2)  # x - для удобства
    y = random.randint(1, (height / length) - 2)  # y - для удобства
    Map[y][x] = 4
# //////////////////////////////////

# ОСНОВНОЙ ЦИКЛ ----------------------------------------------------
screen = pygame.display.set_mode(size)
pygame.display.set_caption("New World")
game = True
paint = True
botNum = 0
while game:

    # pygame.time.delay(500)  # Задержка в ms

    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print("space")
        if paint:
            paint = False
        else:
            paint = True
    # //////////////////////////////////

    # считывает бота
    ending = 0
    hod = True
    while ending < 64 and hod:

        if 0 <= bots[botNum].dna[bots[botNum].counter] <= 7:  # Движение //заверщащий
            bots[botNum].move()
            hod = False

        '''
        if 8 <= bots[botNum].dna[i] <= 15:  # Посмотреть
            bots[botNum].look()

        if 9 <= bots[botNum].dna[i] <= 63:  # Фотосинтез
            bots[botNum].photo()
        '''
        bots[botNum].counter += 1
        if bots[botNum].counter == 64:
            bots[botNum].counter = 0
        ending += 1
    # //////////////////////////////////

    # Заливка
    screen.fill(black)
    if paint:
        # Отрисовка карты
        i_y = 0
        while i_y < len(Map):
            i_x = 0
            while i_x < len(Map[i_y]):
                if Map[i_y][i_x] == 2:
                    pygame.draw.rect(screen, brown, [i_x * length, i_y * length, length, length])
                if Map[i_y][i_x] == 3:
                    pygame.draw.rect(screen,  blue, [i_x * length, i_y * length, length, length])
                if Map[i_y][i_x] == 4:
                    pygame.draw.rect(screen, green, [i_x * length, i_y * length, length, length])
                if Map[i_y][i_x] == 5:
                    pygame.draw.rect(screen, white, [i_x * length, i_y * length, length, length])
                i_x += 1
            i_y += 1
        pygame.display.flip()
        # //////////////////////////////////
    # //////////////////////////////////

    i = 0
    while i < len(bots):
        if bots[i].energy == 0:
            # print("бот", bots[i].number, " умер")
            Map[int(bots[i].y_bot / length)][int(bots[i].x_bot / length)] = 5
            bots.pop(i)
            i -= 1
            botNum -= 1
            # print("осталось ботов:", len(bots))
        i += 1

    botNum += 1
    if botNum == len(bots):
        botNum = 0

    if len(bots) == 0:
        print("GAME OVER")

# ----------------------------------------------------
pygame.quit()
