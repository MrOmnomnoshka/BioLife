import pygame
import random
import time
pygame.init()


def paint_self():
    screen.fill(black)
    # Нарисвоать линии
    w = length - 1
    for line in range(17):
        pygame.draw.line(screen, white, (0, w), (map_width*length, w), 1)
        w += sec + 1
    # //////////////////////////////////
    # Отрисовка карты
    plus = -1
    var = 0
    for hei in range(map_height):
        if var < hei <= 1+var:
            plus += 1
            var += fat
        for wid in range(map_width):
            # 2 - яд, 3 - стена, 4 - бот, 5 - еда, 6 - пусто.
            if Map[hei][wid] == 2:
                pygame.draw.rect(screen, purple, [wid * length, hei * length + plus, length, length])
            if Map[hei][wid] == 3:
                pygame.draw.rect(screen, brown, [wid * length, hei * length + plus, length, length])
            if Map[hei][wid] == 5:
                pygame.draw.rect(screen, y_green, [wid * length, hei * length + plus, length, length])
            if Map[hei][wid] == 7:
                pygame.draw.rect(screen, l_grey, [wid * length, hei * length + plus, length, length])
    for boter in bots:
        boter.draw()
    # //////////////////////////////////

# ЦВЕТА
black = 0, 0, 0  # фон
white = 255, 255, 255  # сетка
grey = 64, 64, 64  # разделитель

purple = 255, 0, 128  # яд
brown = 160, 128, 96  # стена
y_green = 96, 255, 128  # еда
l_grey = 224, 224, 224  # труп
# //////////////////////////////////

height = 640  # 80//160//240//320//400//480//560//640//720//800//880//960//1040//(1600)
sec = round(height / 16)  # 16 секторов
fat = 10  # кол-во ботов в секторе (минимально 1)
if fat > sec:
    fat = sec
length = int(sec / fat)

map_height = int(height / length) + 2
map_width = int(map_height * 1.6)
width = map_width * length
size = width + 320, height + length*2+15

# Создание массива карты
Map = [[]]
# 2 - яд, 3 - стена, 4 - бот, 5 - еда, 6 - пусто, 7 - труп.
for wid in range(map_width):
    Map[0].append(3)
for hei in range(map_height - 2):
    Map.append([])
    for w in range(map_width):
        Map[hei + 1].append(6)
Map.append([])
for wi in range(map_width):
    Map[map_height - 1].append(3)
# /////////////////////////////////////


class Bot:
    def __init__(self, x_map, y_map, r, g, b):
        self.x_map = x_map
        self.y_map = y_map
        self.r = r
        self.g = g
        self.b = b
        # /////////////////////////////////////
        self.energy = 35
        self.counter = 0
        self.direction = 0
        self.age = 100
        self.mineral = 0
        self.dna = []

        self.new_y = 0
        self.new_x = 0
        self.new_direction = 0
        self.coord = 0
        self.after = 0
        self.interaction = 0
        self.shared = False
        self.kys = False
        self.step_on = False
        self.sec = 0
        self.free_place = []
        self.color = (self.r, self.g, self.b)
        self.every_third = 1
    # ///////////////////////////////////// (вспомогательные)

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

        # Зацикливаем мир горизонтально
        if self.new_x >= map_width:
            self.new_x = 0
        if self.new_x < 0:
            self.new_x = map_width - 1
        # /////////////////////////////////////
        self.coord = Map[self.new_y][self.new_x]

    def try_to_move(self):
        if self.coord == 6:  # Если там пусто
            self.just_go()

        elif self.coord == 5 or self.coord == 7:  # Если там еда или труп
            self.just_go()
            self.en(10)
            self.add_r()

        elif self.coord == 4:  # Если там бот
            # self.just_go()
            self.interaction = [self.new_y, self.new_x]
            self.step_on = True

        elif self.coord == 2:  # Если там яд
            self.energy = 0
            Map[self.y_map][self.x_map] = 2

    def try_to_catch(self):
        if self.coord == 4:  # Если там другой бот
            self.interaction = [self.new_y, self.new_x]
            self.kys = True
            self.add_r()
        elif self.coord == 5 or self.coord == 7:  # Если там еда или труп
            self.en(10)
            Map[self.new_y][self.new_x] = 6
            self.add_r()

        elif self.coord == 2:  # Если там яд
            Map[self.new_y][self.new_x] = 5
            self.add_r()

    def just_go(self):
        Map[self.y_map][self.x_map] = 6
        self.x_map = self.new_x
        self.y_map = self.new_y
        Map[self.new_y][self.new_x] = 4

    def en(self, en):
        self.energy += en+self.mineral

    def add_r(self):
        self.r += 15
        if self.r >= 255:
            self.r = 255
        self.g -= 5
        if self.g < 0:
            self.g = 0
        self.b -= 5
        if self.b < 0:
            self.b = 0

    def add_g(self):
        self.g += 15
        if self.g >= 255:
            self.g = 255
        self.r -= 5
        if self.r < 0:
            self.r = 0
        self.b -= 5
        if self.b < 0:
            self.b = 0

    def add_b(self):
        self.b += 15
        if self.b >= 255:
            self.b = 255
        self.r -= 5
        if self.r < 0:
            self.r = 0
        self.g -= 5
        if self.g < 0:
            self.g = 0

    def draw(self):
        self.witch_sec(0)
        pygame.draw.rect(screen, self.color, [self.x_map * length, self.y_map * length + self.sec-1, length, length])

    def next_dna(self, dist):
        self.after = self.counter + dist
        if self.after > 63:
            self.after -= 64

    def witch_sec(self, var):
        if var < self.y_map <= var + fat:
            self.sec = int(var / fat) + 1
        else:
            var += fat
            self.witch_sec(var)

    def am_i_surrounded(self):
        for sur in range(7):
            self.trans(sur)
            if self.coord == 6:
                self.free_place.append([self.new_y, self.new_x])

    def collect_mineral(self):
        was = self.mineral
        self.witch_sec(0)
        if self.sec == 16:
            self.mineral += 3
        elif self.sec == 15:
            self.mineral += 3
        elif self.sec == 14:
            self.mineral += 2
        elif self.sec == 13:
            self.mineral += 2
        elif self.sec == 12:
            self.mineral += 2
        elif self.sec == 11:
            self.mineral += 1
        elif self.sec == 10:
            self.mineral += 1
        elif self.sec == 9:
            self.mineral += 1
        elif self.sec == 8:
            self.mineral += 1
        if self.mineral - was:  # Если хоть чуть добыл-синеет
            self.add_b()
    # ///////////////////////////////////// (вспомогательные)
    # 2 - яд, 3 - стена, 4 - бот, 5 - еда, 6 - пусто, 7 - труп.

    # 0 - 7
    def move(self):
        self.energy -= round(self.age/100)
        where = (code % 8 + self.direction) % 8
        self.trans(where)
        self.try_to_move()
        self.counter += self.coord

    # 8 - 15
    def catch(self):
        self.energy -= round(self.age/100)
        where = (code % 8 + self.direction) % 8
        self.trans(where)
        self.try_to_catch()
        self.counter += self.coord

    # 16
    def move_rel(self):
        self.energy -= round(self.age/100)
        self.next_dna(1)
        where = (self.dna[self.after] % 8 + self.direction) % 8
        self.trans(where)
        self.try_to_move()
        self.next_dna(self.coord)
        self.counter += self.dna[self.after]

    # 17
    def catch_rel(self):
        self.energy -= round(self.age/100)
        self.next_dna(1)
        where = (self.dna[self.after] % 8 + self.direction) % 8
        self.trans(where)
        self.try_to_catch()
        self.next_dna(self.coord)
        self.counter += self.dna[self.after]

    # 18
    def look_rel(self):
        self.next_dna(1)
        where = (self.dna[self.after] % 8 + self.direction) % 8
        self.trans(where)
        self.next_dna(self.coord)
        self.counter += self.dna[self.after]

    # 19
    def turn_rel(self):
        self.next_dna(1)
        where = (self.dna[self.after] % 8 + self.direction) % 8
        self.trans(where)
        self.direction = self.new_direction
        self.counter += 2

    # 20
    def how_much_energy(self):
        self.next_dna(1)
        enr = (self.dna[self.after] % 8) * 28
        if self.energy >= enr:
            self.next_dna(3)
            self.counter += self.dna[self.after]
        else:
            self.next_dna(2)
            self.counter += self.dna[self.after]

    # 21
    def photo(self):
        self.energy -= round(self.age/100)
        was = self.energy
        self.witch_sec(0)
        if self.sec == 1:
            self.en(10)
        elif self.sec == 2:
            self.en(9)
        elif self.sec == 3:
            self.en(8)
        elif self.sec == 4:
            self.en(7)
        elif self.sec == 5:
            self.en(6)
        elif self.sec == 6:
            self.en(5)
        elif self.sec == 7:
            self.en(4)
        elif self.sec == 8:
            self.en(3)
        elif self.sec == 9:
            self.en(2)
        self.counter += 1
        if self.energy - was:  # Если хоть чуть добыл-зеленеет
            self.add_g()
        self.sec = 0

    # 22
    def share(self):
        self.next_dna(1)
        where = (self.dna[self.after] % 8 + self.direction) % 8
        self.trans(where)
        if self.coord == 4:
            self.interaction = [self.new_y, self.new_x]
            self.shared = True
        self.counter += 2

    # 23
    def clone(self):
        birth()
        self.counter += 1

    # 24
    def my_sec(self):
        self.witch_sec(0)
        self.next_dna(1)
        need_sec = (self.dna[self.after] % 16)
        if self.sec-1 >= need_sec:
            self.next_dna(3)
            self.counter += self.dna[self.after]
        else:
            self.next_dna(2)
            self.counter += self.dna[self.after]

    # 25
    def surrounded(self):
        self.am_i_surrounded()
        if self.free_place:
            self.counter += 1
        else:
            self.counter += 2
        self.free_place = []

    # 26
    def mine_to_energy(self):
        self.energy += self.mineral*4
        self.mineral = 0
        self.counter += 1

    # 27
    def how_much_mineral(self):
        self.next_dna(1)
        mi = (self.dna[self.after] % 8) * 2
        if self.mineral >= mi:
            self.next_dna(3)
            self.counter += self.dna[self.after]
        else:
            self.next_dna(2)
            self.counter += self.dna[self.after]

    # 28 - 63
    def jump(self):
        self.counter += code


# Параметры мира (можно менять)
bots = []
DnaAmount = 64
resources = False
gravity = False
beauty = True
FoodAmount = int(map_width * map_height * 0.03)
ToxAmount = int(map_width * map_height * 0.05)
# num_of_mutations(0, do)
do = 1


def new_food():
    x_f = random.randint(0, map_width - 1)  # x - для удобства
    y_f = random.randint(0, map_height - 1)  # y - для удобства
    if Map[y_f][x_f] == 6:
        Map[y_f][x_f] = 5
    else:
        new_food()


def new_tox():
    x_t = random.randint(0, map_width - 1)  # x - для удобства
    y_t = random.randint(0, map_height - 1)  # y - для удобства
    if Map[y_t][x_t] == 6:
        Map[y_t][x_t] = 2
    else:
        new_tox()


def birth():
    bots[botNum].energy -= 35  # Стоимость "родов"
    bots[botNum].am_i_surrounded()
    if bots[botNum].free_place and bots[botNum].energy > 35:
        bots[botNum].energy -= 35
        bots[botNum].every_third += 1
        index = random.randint(0, len(bots[botNum].free_place) - 1)
        baby_y = bots[botNum].free_place[index].pop(0)
        baby_x = bots[botNum].free_place[index].pop(0)
        bots.append(Bot(baby_x, baby_y, bots[botNum].r, bots[botNum].g, bots[botNum].b))
        Map[baby_y][baby_x] = 4
        parent_dna = bots[botNum].dna.copy()
        # Мутирование каждые 3 роды
        if bots[botNum].every_third >= 3:
            bots[botNum].every_third = 1
            num_of_mutations = random.randint(1, do)
            for e in range(num_of_mutations):
                parent_dna[random.randint(0, 63)] = random.randint(0, 63)
        # //////////////////////////////////
        bots[len(bots) - 1].dna = parent_dna
    else:
        bots[botNum].energy = 0
        Map[bots[botNum].y_map][bots[botNum].x_map] = 7
    bots[botNum].free_place = []


def reborn():
    bots.append(Bot(int(map_width / 2), 2, 0, 255, 0))  # ADAM
    Map[2][int(map_width / 2)] = 4
    gens = []
    if gens:
        for g in range(DnaAmount - len(gens)):
            gens.append(21)
        bots[0].dna = gens
    else:
        for Dna in range(DnaAmount):
            bots[0].dna.append(21)

reborn()

# bots.append(Bot(int(map_width/2), map_height-fat*2, 0, 0, 255))  # Miner
# Map[map_height-fat*2][int(map_width / 2)] = 4
# # for gen in range(DnaAmount):
# #     bots[1].dna.append(22)
# gens = [22,22,27,61]
# if gens:
#     for g in range(DnaAmount - len(gens)):
#         gens.append(22)
#     bots[1].dna = gens

if resources:
    for f in range(FoodAmount):
        new_food()

    for t in range(ToxAmount):
        new_tox()

# ОСНОВНОЙ ЦИКЛ ----------------------------------------------------
screen = pygame.display.set_mode(size)  # pygame.FULLSCREEN)
pygame.display.set_caption("New World")
game = True
paint = True
delay = 0
botNum = 0
cyc = 0
gener = 0
every = 0
while game:
    cyc += 1
    for bot in range(len(bots)):
        pygame.time.delay(delay)  # Задержка в ms
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if paint:
                    paint = False
                else:
                    paint = True
            if keys[pygame.K_TAB]:
                paint_self()
                pygame.image.save(screen, "screenshot" + str(time.time()) + ".bmp")
            if keys[pygame.K_ESCAPE]:
                game = False
            if keys[pygame.K_g]:
                if gravity:
                    gravity = False
                else:
                    gravity = True
            if keys[pygame.K_b]:
                if beauty:
                    beauty = False
                else:
                    beauty = True
            if keys[pygame.K_RIGHTBRACKET]:
                delay += 1
            if keys[pygame.K_LEFTBRACKET]:
                delay -= 1
                if delay < 0:
                    delay = 0
            if keys[pygame.K_KP_PLUS]:
                do += 1
                if do > DnaAmount:
                    do = DnaAmount
            if keys[pygame.K_KP_MINUS]:
                do -= 1
                if do < 1:
                    do = 1
            if keys[pygame.K_r]:
                if resources:
                    resources = False
                    for hei in range(map_height):
                        for wid in range(map_width):
                            if Map[hei][wid] != 3 and Map[hei][wid] != 4 and Map[hei][wid] != 7:
                                Map[hei][wid] = 6
                else:
                    resources = True
                pygame.time.delay(150)
        # //////////////////////////////////

        # считывает бота
        ending = 0
        hod = True
        while ending < 10 and hod:
            code = bots[botNum].dna[bots[botNum].counter]
            # Движение (заверщающий)
            if 0 <= code <= 7:
                # print("move")
                # print("bot",bots[botNum].numb,"moves")
                bots[botNum].move()
                hod = False
            # Схватить (заверщающий)
            if 8 <= code <= 15:
                # print("catch")
                bots[botNum].catch()
                hod = False
            # Движение относительное (заверщающий)
            if code == 16:
                bots[botNum].move_rel()
                hod = False
            # Схватить относительно (заверщающий)
            if code == 17:
                bots[botNum].catch_rel()
                hod = False
            # Посмотреть относительно
            if code == 18:
                bots[botNum].look_rel()
                ending += 1
            # Повернуться относительно
            if code == 19:
                bots[botNum].turn_rel()
                ending += 1
            # Хватает ли энергии
            if code == 20:
                bots[botNum].how_much_energy()
                ending += 1
            # Фотосинтез (заверщающий)
            if code == 21:
                # print(botNum, "photo")
                bots[botNum].photo()
                hod = False
            # Поделиться энергией (заверщающий)
            if code == 22:
                # print(botNum, "share")
                bots[botNum].share()
                hod = False
            # Размножение отдельно (заверщающий)
            if code == 23:
                bots[botNum].clone()
                hod = False
            # Какой сектор?
            if code == 24:
                bots[botNum].my_sec()
                ending += 1
            # Я окружен?
            if code == 25:
                bots[botNum].surrounded()
                ending += 1
            # Преобразовать миреналы
            if code == 26:
                bots[botNum].mine_to_energy()
                hod = False
            # Хватает ли минералов
            if code == 27:
                bots[botNum].how_much_mineral()
                ending += 1
            # Безусловный переход
            if 28 <= code <= DnaAmount - 1:
                bots[botNum].jump()
                ending += 1
            # Всегда собирает минералы
            bots[botNum].collect_mineral()

            if ending > 9:
                bots[botNum].energy -= round(bots[botNum].age / 100)

            # Если взаимодействовал с другим ботом
            if bots[botNum].interaction:
                for vic in range(len(bots)):  # Поиск бота
                    if [bots[vic].y_map, bots[vic].x_map] == bots[botNum].interaction:
                        bots[botNum].interaction = 0
                        victim = vic
                        break
                # Наступил
                if bots[botNum].step_on:
                    bots[botNum].step_on = False
                    if bots[botNum].energy > bots[victim].energy:
                        bots[botNum].just_go()
                        bots[botNum].en(bots[victim].energy)
                        bots[botNum].mineral += bots[victim].mineral
                        bots[botNum].add_r()
                        bots.pop(victim)
                        if botNum > victim:
                            botNum -= 1
                    else:
                        bots[victim].en(round(bots[botNum].energy/2))
                        bots[victim].mineral += bots[botNum].mineral
                        bots[victim].add_r()
                        Map[bots[botNum].y_map][bots[botNum].x_map] = 6  # Бот - пустота
                        bots.pop(botNum)
                        botNum -= 1
                # Укусил
                if bots[botNum].kys:
                    bots[botNum].kys = False
                    bots[botNum].en(bots[victim].energy)
                    bots[botNum].mineral += bots[victim].mineral
                    Map[bots[victim].y_map][bots[victim].x_map] = 6
                    bots.pop(victim)
                    if botNum > victim:
                        botNum -= 1
                # Поделился
                if bots[botNum].shared:
                    bots[botNum].shared = False
                    quarter = round(bots[botNum].energy / 4)
                    bots[botNum].energy -= quarter
                    bots[victim].energy += quarter

            # Размножение
            if bots[botNum].energy > 200:
                birth()
                hod = False

            if bots[botNum].counter > DnaAmount - 1:
                bots[botNum].counter -= DnaAmount
        bots[botNum].age += 1
        # //////////////////////////////////

        # Проверка на смерть
        if bots[botNum].energy <= 0:
            # print(len(bots[botNum].dna))
            position = Map[bots[botNum].y_map][bots[botNum].x_map]
            if position != 2 and position != 7:  # Если он не стал ядом или трупом
                Map[bots[botNum].y_map][bots[botNum].x_map] = 7  # Бот - труп
            bots.pop(botNum)
            botNum -= 1
            # print("осталось ботов:", len(bots))
        # //////////////////////////////////

        # Ходит следующий бот если не все умерли
        if bots:
            botNum += 1
            if botNum == len(bots):
                botNum = 0
        else:  # Если таки все умерли
            gener += 1
            print(gener, "Боты прожили", cyc)
            paint_self()
            pygame.image.save(screen, "bots_"+str(gener)+".bmp")
            cyc = 0
            for hei in range(map_height):
                for wid in range(map_width):
                    if Map[hei][wid] != 3:  # Обнуляем все кроме стен
                        Map[hei][wid] = 6
            botNum = 0
            reborn()
            if resources:
                for f in range(FoodAmount):
                    new_food()
                for t in range(ToxAmount):
                    new_tox()
            break

            # //////////////////////////////////

    if resources:
        # Добовляем съеденные ресурсы
        real_food = 0
        real_tox = 0
        for hei in range(map_height):
            for wid in range(map_width):
                if Map[hei][wid] == 2:
                    real_tox += 1
                if Map[hei][wid] == 5:
                    real_food += 1
                wid += 1
            hei += 1
        if real_food < FoodAmount:
            for f in range(FoodAmount - real_food):
                new_food()
        if real_tox < ToxAmount:
            for t in range(ToxAmount - real_tox):
                new_tox()
        # //////////////////////////////////

    if gravity:
        if beauty:
            # Гравитация трупов красивая
            hei = map_height-1
            while hei > 0:
                wid = map_width-1
                while wid > 0:
                    if Map[hei][wid] == 7:
                        y = hei + 1
                        if y > map_height:
                            y = map_height
                        if Map[y][wid] == 6:
                            Map[hei][wid] = 6
                            Map[y][wid] = 7
                    wid -= 1
                hei -= 1
            # //////////////////////////////////
        else:
            # Гравитация трупов быстрая
            for hei in range(map_height):
                for wid in range(map_width):
                    if Map[hei][wid] == 7:
                        y = hei + 1
                        if y > map_height:
                            y = map_height
                        if Map[y][wid] == 6:
                            Map[hei][wid] = 6
                            Map[y][wid] = 7
            # //////////////////////////////////

    # Заливка
    if paint:
        paint_self()
        # Надпись
    pygame.draw.rect(screen, black, [width+length/2, 0, width + 320, height + length * 2 + 15])
    pygame.draw.line(screen, grey, (width+length/2, 0), (width+length/2, height + length * 2 + 15), length)
    inf_font = pygame.font.Font(None, 60)

    counter = inf_font.render("Особей:" + str(len(bots)), 0, white)
    screen.blit(counter, (width + length, 5))

    dos = inf_font.render("Мутаций:" + str(do), 0, white)
    screen.blit(dos, (width + length, 45))

    zd = inf_font.render("Delay:" + str(delay), 0, white)
    screen.blit(zd, (width + length, 85))
        # //////////////////////////////////
    pygame.display.flip()
    # //////////////////////////////////
    if every:
        if cyc >= every:
            every += 500
            paint_self()
            pygame.image.save(screen, "thousand_" + str(cyc/500) + ".bmp")
# ----------------------------------------------------
pygame.quit()
