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
    def __init__(self, x_map, y_map, counter, direction, best_gens, numb):
        self.x_map = x_map
        self.y_map = y_map
        self.counter = counter
        self.direction = direction
        self.best_gens = best_gens
        self.numb = numb
        # /////////////////////////////////////
        self.energy = 100
        self.dna = []
        self.new_y = 0
        self.new_x = 0
        self.new_direction = 0
        self.coord = 0

        if self.best_gens:
            self.dna = self.best_gens
        else:
            for gen in range(DnaAmount):
                self.dna.append(random.randint(0, 63))
                # print("[", gen, "] =", self.dna[gen])
            # print("dna =", self.dna)

    # ///////////////////////////////////// (вспомогательные)
    def mutate(self):
        for m in range(num_of_mutations):
            self.dna[random.randint(0, DnaAmount-1)] = random.randint(0, 63)
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
        self.coord = Map[self.new_y][self.new_x]

    def try_to_move(self):

        if self.coord == 2:  # Если там пусто
            self.just_go()

        elif self.coord == 5 or self.coord == 6:  # Если там еда или труп
            self.just_go()
            self.en(10)
            if self.coord == 5:  # Пересоздаем еду
                new_food()

        elif self.coord == 7:  # Если там яд
            self.just_go()
            self.energy = 0
            new_tox()

    def try_to_catch(self):
        if self.coord == 5 or self.coord == 6:  # Если там еда или труп
            self.en(10)
            Map[self.new_y][self.new_x] = 2
            if self.coord == 5:
                new_food()

        elif self.coord == 7:  # Если там яд
            self.en(20)
            Map[self.new_y][self.new_x] = 2
            new_tox()

    def just_go(self):
        Map[self.y_map][self.x_map] = 2
        self.x_map = self.new_x
        self.y_map = self.new_y
        Map[self.new_y][self.new_x] = 4

    def norm_jump(self):
        place = self.counter + self.coord
        if place > DnaAmount-1:
            place -= DnaAmount
        self.counter += self.dna[place]

    def en(self, en):
        self.energy += en
        if self.energy > 100:
            self.energy = 100

    # ///////////////////////////////////// (вспомогательные)
    # 2 - пустота, 3 - стена, 4 - бот, 5 - еда, 6 - труп, 7 - яд.

    def move(self):  # 0 - 7
        self.energy -= 1
        where = (self.dna[self.counter] % 8 + self.direction) % 8
        self.trans(where)
        self.try_to_move()

        self.counter += 1

    def catch(self):
        self.energy -= 1
        where = (self.dna[self.counter] % 8 + self.direction) % 8
        self.trans(where)

        self.try_to_catch()

        self.counter += 1

    def turn(self):  # 16-23
        where = (self.dna[self.counter] % 8 + self.direction) % 8
        self.trans(where)
        self.direction = self.new_direction
        self.counter += 1

    def move_rel(self):  # 24
        self.energy -= 1

        cou = self.counter
        if cou == DnaAmount-1:
            cou -= DnaAmount
        where = (self.dna[cou+1] % 8 + self.direction) % 8
        self.trans(where)
        self.try_to_move()

        self.counter += 1

    def look(self):  # 25
        cou = self.counter
        if cou == DnaAmount-1:
            cou -= DnaAmount
        where = (self.dna[cou+1] % 8 + self.direction) % 8
        self.trans(where)
        # print("where -", where)
        # print("Впереди вижу", self.coord)
        self.norm_jump()

    def energy_amo(self):  # 26
        cou = self.counter
        if cou == DnaAmount-1:
            cou -= DnaAmount

        need = self.dna[cou + 1] * 15
        if self.energy >= need:
            place = self.counter + 3
            if place > DnaAmount-1:
                place -= DnaAmount
            self.counter += self.dna[place]
        else:
            place = self.counter + 2
            if place > DnaAmount-1:
                place -= DnaAmount
            self.counter += self.dna[place]

    def catch_rel(self):  # 27
        self.energy -= 1
        cou = self.counter
        if cou == DnaAmount-1:
            cou -= DnaAmount
        where = (self.dna[cou + 1] % 8 + self.direction) % 8
        self.trans(where)
        self.try_to_catch()

        self.norm_jump()

    def jump(self):
        self.counter += code

# Создаем ботов, еду
bots = []
BotsAmount = 25
DnaAmount = 64
SurvivorsAmount = int(pow(BotsAmount, 0.5))
FoodAmount = int(map_width * map_height * 0.05)
ToxAmount = int(map_width * map_height * 0.07)
BestGens = []


def new_bot(nomer_bot):
    x = random.randint(0, map_width - 1)  # x - для удобства
    y = random.randint(1, map_height - 2)  # y - для удобства
    if Map[y][x] == 2:
        Map[y][x] = 4
        if BestGens:
            bots.append(Bot(x, y, 0, 0, BestGens, nomer_bot))
        else:
            # gens = [17,25,0,63,8,8,16,16,24,25,4,25,55,55,25,25,32,24,0,47,47,47,47,47,47,27,0,
            #        39,39,39,39,39,39,24,4,31,31,31,31,31,31,27,4,23,23,23,23,23,23]
            # gens = [17, 25, 0, 8, 63, 63, 8, 8, 10, 0, 55, 8, 53, 53, 53, 53, 53, 53]
            # gens = [17, 25, 7, 8, 8, 8, 16, 16, 16, 25, 0, 10, 55, 55, 10, 10, 12, 15, 48, 0, 46, 8, 44]
            # for n in range(DnaAmount-len(gens)):
                # gens.append(random.randint(0, 63))
            bots.append(Bot(x, y, 0, 0, [], nomer_bot))  # gens вместо []
            # print(len(gens))
    else:
        new_bot(nomer_bot)


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
    new_bot(b)

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
    cyc += 1
    for bot in bots:
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
                # print("move")
                bots[botNum].move()
                hod = False

            if 8 <= code <= 15:  # Схватить (заверщающий)
                # print("catch")
                bots[botNum].catch()
                hod = False

            if 16 <= code <= 23:  # Повернуться
                # print("turn")
                bots[botNum].turn()
                ending += 1

            if code == 24:  # Движение относительно (заверщающий)
                bots[botNum].move_rel()
                hod = False

            if code == 25:  # Посмотреть
                bots[botNum].look()
                ending += 1
                # print("look")

            if code == 26:  # Кол-во энергии
                bots[botNum].energy_amo()
                ending += 1

            if code == 27:  # Схватить относительно (заверщающий)
                bots[botNum].catch_rel()
                hod = False

            if 28 <= code <= DnaAmount-1:  # Безусловный переход
                bots[botNum].jump()
                ending += 1

            if bots[botNum].counter > DnaAmount-1:
                bots[botNum].counter -= DnaAmount

            if ending > 14:
                bots[botNum].energy -= 1
        # //////////////////////////////////

        # Проверка на смерть
        if bots[botNum].energy <= 0:
            # print(len(bots[botNum].dna))
            Map[bots[botNum].y_map][bots[botNum].x_map] = 6
            bots.pop(botNum)
            botNum -= 1
            # print("осталось ботов:", len(bots))
        # //////////////////////////////////

        # Ходит следующий бот
        botNum += 1
        if botNum == len(bots):
            botNum = 0
        # //////////////////////////////////

        if len(bots) == SurvivorsAmount:
            botNum = 0
            if BestCyc < cyc:
                BestCyc = cyc
            print("Поколение", gener, "Тут -", cyc, "Лучший - ", BestCyc)
            cyc = 0
            gener += 1
            # Создаем новую карту
            for hei in range(map_height):
                for wid in range(map_width):
                    if Map[hei][wid] != 3:
                        Map[hei][wid] = 2
                    wid += 1
                hei += 1
            for f in range(FoodAmount):
                new_food()
            for t in range(ToxAmount):
                new_tox()
            # //////////////////////////////////

            # Создаем новое поколение
            i = 0
            ChildMutAmount = random.randint(0, SurvivorsAmount)
            num_of_mutations = random.randint(1, int(DnaAmount*0.05))
            for S in range(SurvivorsAmount):
                # print(i)
                BestGens = bots[0].dna
                # print("best-", bots[0].dna)
                # print(len(BestGens))
                print("Бот родитель", bots[0].numb, "имел энергии", bots[0].energy, "днк -", bots[0].dna)
                bots.pop(0)
                for child in range(SurvivorsAmount-ChildMutAmount):  # Нормальное потомство
                    new_bot(i)
                    i += 1
                for r in range(ChildMutAmount):
                    new_bot(i)  # и пара с мутацией
                    i += 1
                    bots[len(bots)-1].mutate()
                BestGens = []
            # //////////////////////////////////

    # Заливка
    screen.fill(black)
    if paint:
        # Отрисовка карты
        for hei in range(map_height):
            for wid in range(map_width):
                if Map[hei][wid] == 3:
                    pygame.draw.rect(screen, brown, [wid * length, hei * length, length, length])
                if Map[hei][wid] == 4:
                    pygame.draw.rect(screen, blue, [wid * length, hei * length, length, length])
                if Map[hei][wid] == 5:
                    pygame.draw.rect(screen, green, [wid * length, hei * length, length, length])
                if Map[hei][wid] == 6:
                    pygame.draw.rect(screen, white, [wid * length, hei * length, length, length])
                if Map[hei][wid] == 7:
                    pygame.draw.rect(screen, red, [wid * length, hei * length, length, length])
                wid += 1
        pygame.display.flip()
        # //////////////////////////////////
    # //////////////////////////////////
# ----------------------------------------------------
pygame.quit()
