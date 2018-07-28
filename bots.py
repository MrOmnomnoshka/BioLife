import pygame
import random

pygame.init()

size = width, height = 800, 500
length = 10

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
    # 2 - пустота, 3 - стена, 4 - бот, 5 - еда, 6 - труп, 7 - яд.
Map.append([])
for el in range(map_width):
    Map[0].append(3)

for el in range(map_height - 2):    # 3333333333
    Map.append([])                  # 3222222223
                                    # 3222222223  -  что-то типо такого
    for e in range(map_width):      # 3222222223
        Map[el + 1].append(2)       # 3333333333

Map.append([])
for num in range(map_width):
    Map[map_height - 1].append(3)
# /////////////////////////////////////


class Bot:
    def __init__(self, x_map, y_map, counter, direction, best_gens):
        self.x_map = x_map
        self.y_map = y_map
        self.counter = counter
        self.direction = direction
        self.best_gens = best_gens
        self.energy = 100
        self.dna = []
        # /////////////////////////////////////
        self.new_y = 0
        self.new_x = 0
        self.new_direction = 0
        self.what = 0

        if self.best_gens:
            self.dna = self.best_gens
        else:
            for gen in range(64):
                self.dna.append(random.randint(0, 63))
                # print("[", gen, "] =", self.dna[gen])
            # print("dna =", self.dna)

    # ///////////////////////////////////// (вспомогательные)
    def mutate(self):
        for m in range(num_of_mutations):
            # print(m+1, "mut")
            self.dna[random.randint(0, 63)] = random.randint(0, 63)
            # print("mut dna =", self.dna)

    def trans(self, where):
        if where == 0:  # Вверх
            self.new_x = self.x_map
            self.new_y = self.y_map - 1
            self.new_direction = 0

        if where == 1:  # Вверх-вправо
            self.new_x = self.x_map + 1
            self.new_y = self.y_map - 1
            self.new_direction = 1

        if where == 2:  # Вправо
            self.new_x = self.x_map + 1
            self.new_y = self.y_map
            self.new_direction = 2

        if where % 8 == 3:  # Вниз-вправо
            self.new_x = self.x_map + 1
            self.new_y = self.y_map + 1
            self.new_direction = 3

        if where == 4:  # Вниз
            self.new_x = self.x_map
            self.new_y = self.y_map + 1
            self.new_direction = 4

        if where == 5:  # Вниз-влево
            self.new_x = self.x_map - 1
            self.new_y = self.y_map + 1
            self.new_direction = 5

        if where == 6:  # Влево
            self.new_x = self.x_map - 1
            self.new_y = self.y_map
            self.new_direction = 6

        if where == 7:  # Вверх-влево
            self.new_x = self.x_map - 1
            self.new_y = self.y_map - 1
            self.new_direction = 7

        # Зацикливаем мир
        if self.new_x >= map_width:
            self.new_x = 0
        if self.new_x < 0:
            self.new_x = map_width-2
        # /////////////////////////////////////

    def just_go(self):
        Map[self.y_map][self.x_map] = 2
        self.x_map = self.new_x
        self.y_map = self.new_y
        Map[self.new_y][self.new_x] = 4

    def en(self, en):
        self.energy += en
        if self.energy > 100:
            self.energy = 100
    # ///////////////////////////////////// (вспомогательные)
    # 2 - пустота, 3 - стена, 4 - бот, 5 - еда, 6 - труп, 7 - яд.

    def move(self):
        self.energy -= 1
        where = (self.dna[self.counter] % 8 + self.direction) % 8
        self.trans(where)
        coord = Map[self.new_y][self.new_x]

        if coord == 2:
            self.just_go()

        elif coord == 5 or coord == 6:  # Если там еда или труп
            self.just_go()
            self.en(10)
            if coord == 5:
                new_food()
            # print("бот", self.number, "съел еду")

        elif coord == 7:  # Если там яд
            self.just_go()
            self.energy = 0
            new_tox()
        place = self.counter + coord
        if place > 63:
            place -= 64
        self.counter += self.dna[place]

    def catch(self):
        self.energy -= 1
        where = (self.dna[self.counter] % 8 + self.direction) % 8
        self.trans(where)

        coord = Map[self.new_y][self.new_x]
        if coord == 5 or coord == 6:  # Если там еда или труп
            self.en(10)
            Map[self.new_y][self.new_x] = 2
            if coord == 5:
                new_food()
                # print("бот", self.number, "съел еду")

        elif coord == 7:  # Если там яд
            self.en(20)
            Map[self.new_y][self.new_x] = 2
            # print("Преобразовал яд - красавчик!")
            new_tox()
        place = self.counter + coord
        if place > 63:
            place -= 64
        self.counter += self.dna[place]

    def turn(self):  # 16-23
        # print("turn вызвали?")
        where = (self.dna[self.counter] % 8 + self.direction) % 8
        self.trans(where)
        self.direction = self.new_direction
        # print(" dir-", self.direction)
        self.counter += 1

    def move_rel(self):  # 24
        self.energy -= 1
        cou = self.counter
        if cou == 63:
            cou -= 64
        where = (self.dna[cou+1] % 8 + self.direction) % 8
        self.trans(where)
        coord = Map[self.new_y][self.new_x]

        if coord == 2:
            self.just_go()
        elif coord == 5 or coord == 6:  # Если там еда или труп
            self.just_go()
            self.en(10)
            if coord == 5:
                new_food()
        elif coord == 7:  # Если там яд
            self.just_go()
            self.energy = 0
            new_tox()
        place = self.counter + coord
        if place > 63:
            place -= 64
        self.counter += self.dna[place]

    def look(self):  # 25
        cou = self.counter
        if cou == 63:
            cou -= 64
        where = (self.dna[cou+1] % 8 + self.direction) % 8
        self.trans(where)
        # print("where -", where)
        coord = Map[self.new_y][self.new_x]
        # print("Впереди вижу", coord)
        place = self.counter + coord
        if place > 63:
            place -= 64
        self.counter += self.dna[place]

    def energy_amo(self):  # 26
        cou = self.counter
        if cou == 63:
            cou -= 64

        need = self.dna[cou + 1] * 15
        if self.energy >= need:
            place = self.counter + 3
            if place > 63:
                place -= 64
            self.counter += self.dna[place]
        else:
            place = self.counter + 2
            if place > 63:
                place -= 64
            self.counter += self.dna[place]

    def catch_rel(self):  # 27
        self.energy -= 1
        cou = self.counter
        if cou == 63:
            cou -= 64
        where = (self.dna[cou + 1] % 8 + self.direction) % 8
        self.trans(where)

        coord = Map[self.new_y][self.new_x]
        if coord == 5 or coord == 6:  # Если там еда или труп
            self.en(10)
            Map[self.new_y][self.new_x] = 2
            if coord == 5:
                new_food()
                # print("бот", self.number, "съел еду")

        elif coord == 7:  # Если там яд
            self.en(20)
            Map[self.new_y][self.new_x] = 2
            # print("Преобразовал яд - красавчик!")
            new_tox()
        place = self.counter + coord
        if place > 63:
            place -= 64
        self.counter += self.dna[place]

    def jump(self):
        self.counter += code

# Создаем ботов, еду
bots = []
BotsAmount = 64
num_of_mutations = 1
ChildAmount = int(pow(BotsAmount, 0.5))
FoodAmount = int(map_width * map_height * 0.05)
ToxAmount = int(map_width * map_height * 0.07)
BestGens = []


def new_bot():
    x = random.randint(0, map_width - 1)  # x - для удобства
    y = random.randint(1, map_height - 2)  # y - для удобства
    if Map[y][x] == 2:
        Map[y][x] = 4
        if BestGens:
            bots.append(Bot(x, y, 0, 0, BestGens))
        else:
            # gens = [17,25,0,8,63,63,8,8,16,24,0,56,56,56,56,56,56,27,0,48,48,48,48,48,47]
            # for n in range(39):
            #     gens.append(0)
            bots.append(Bot(x, y, 0, 0, []))  # gens вместо []
    else:
        new_bot()


def new_food():
    x = random.randint(0, map_width - 1)  # x - для удобства
    y = random.randint(1, map_height - 2)  # y - для удобства
    if Map[y][x] == 2:
        Map[y][x] = 5
    else:
        new_food()


def new_tox():
    x = random.randint(0, map_width - 1)  # x - для удобства
    y = random.randint(1, map_height - 2)  # y - для удобства
    if Map[y][x] == 2:
        Map[y][x] = 7
    else:
        new_tox()


for b in range(BotsAmount):
    new_bot()

for f in range(FoodAmount):
    new_food()

for t in range(ToxAmount):
    new_tox()

# //////////////////////////////////

# ОСНОВНОЙ ЦИКЛ ----------------------------------------------------
screen = pygame.display.set_mode(size)
pygame.display.set_caption("New World")
game = True
paint = True
botNum = 0
gener = 1
cyc = 0
BestCyc = 0
while game:
    for liver in bots:

        # pygame.time.delay(500)  # Задержка в ms

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pygame.time.delay(150)
            if paint:
                paint = False
            else:
                paint = True
            print(paint)
        # //////////////////////////////////

        # считывает бота
        ending = 0
        hod = True
        while ending < 15 and hod:
            code = bots[botNum].dna[bots[botNum].counter]
            if 0 <= code <= 7:  # Движение (заверщающий)
                bots[botNum].move()
                hod = False

            if 8 <= code <= 15:  # Схватить (заверщающий)
                bots[botNum].catch()
                hod = False

            if 16 <= code <= 23:  # Повернуться
                bots[botNum].turn()
                ending += 1

            if code == 24:  # Движение относительно (заверщающий)
                bots[botNum].move_rel()
                hod = False

            if code == 25:  # Посмотреть
                bots[botNum].look()
                ending += 1

            if code == 26:  # Кол-во энергии
                bots[botNum].energy_amo()
                ending += 1

            if code == 27:  # Схватить относительно (заверщающий)
                bots[botNum].catch_rel()
                hod = False

            if 28 <= code <= 63:  # Безусловный переход
                bots[botNum].jump()
                ending += 1

            if bots[botNum].counter > 63:
                bots[botNum].counter -= 64

            if ending > 14:
                bots[botNum].energy -= 5
        # //////////////////////////////////

        # Проверка на смерть
        if bots[botNum].energy <= 0:
            Map[bots[botNum].y_map][bots[botNum].x_map] = 6
            bots.pop(botNum)
            botNum -= 1
            # print("осталось ботов:", len(bots))
        # //////////////////////////////////

        botNum += 1
        if botNum == len(bots):
            botNum = 0
            cyc += 1

        if len(bots) == ChildAmount:
            botNum = 0
            if BestCyc < cyc:
                BestCyc = cyc
            print("Поколение", gener, "Тут -", cyc, "Лучший - ", BestCyc)
            cyc = 0
            gener += 1
            # Создаем новую карту
            i_y = 0
            while i_y < len(Map):
                i_x = 0
                while i_x < len(Map[i_y]):
                    if Map[i_y][i_x] != 3:
                        Map[i_y][i_x] = 2
                    i_x += 1
                i_y += 1
            for f in range(FoodAmount):
                new_food()
            for t in range(ToxAmount):
                new_tox()
            # //////////////////////////////////

            # Создаем новое поколение
            for b in range(ChildAmount):
                BestGens = bots[0].dna
                # print("best-", bots[0].dna)
                # print(len(BestGens))
                # print("Бот", bots[0].number, "дал потомков - ", ChildAmount)
                bots.pop(0)
                for child in range(ChildAmount-1):
                    new_bot()
                    # и один с мутацией
                new_bot()
                bots[len(bots)-1].mutate()
                BestGens = []
            # //////////////////////////////////

    # Заливка
    screen.fill(black)
    if paint:
        # Отрисовка карты
        i_y = 0
        while i_y < len(Map):
            i_x = 0
            while i_x < len(Map[i_y]):
                if Map[i_y][i_x] == 3:
                    pygame.draw.rect(screen, brown, [i_x * length, i_y * length, length, length])
                if Map[i_y][i_x] == 4:
                    pygame.draw.rect(screen,  blue, [i_x * length, i_y * length, length, length])
                if Map[i_y][i_x] == 5:
                    pygame.draw.rect(screen, green, [i_x * length, i_y * length, length, length])
                if Map[i_y][i_x] == 6:
                    pygame.draw.rect(screen, white, [i_x * length, i_y * length, length, length])
                if Map[i_y][i_x] == 7:
                    pygame.draw.rect(screen, red, [i_x * length, i_y * length, length, length])
                i_x += 1
            i_y += 1
        pygame.display.flip()
        # //////////////////////////////////
    # //////////////////////////////////
# ----------------------------------------------------
pygame.quit()
