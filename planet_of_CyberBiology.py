import random

place = []
place_x = 174
place_y = 174

place.append([])
for el in range(place_x):
    place[0].append(2)

for el in range(place_y-2):
    place.append([])
    place[el+1].append(2)
    for e in range(place_x-2):
        place[el+1].append(1)
    place[el+1].append(2)

place.append([])
for num in range(place_x):
    place[place_y-1].append(2)

print(len(place[173]))

# переменная  command_counter указывает количество команд, доступных в этом мире
command_counter = 8


class bot():
    global place
    # жизни бота
    lifes = 100
    # координаты. 1-я - сторона куба, 2,3 соответственно, координаты поля
    coord1 = random.randint(0,len(place)-1)
    coord2 = random.randint(1,len(place[1])-2)

    # указатель текущей команды
    UTK = 0
    # Направление
    way = 1
    # алгоритм
    algoritm = [random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter),
             random.randint(1, command_counter), random.randint(1, command_counter), random.randint(1, command_counter),
             random.randint(1, command_counter)
             ]
    # функция, которая будет определять следующую команду
    def doing(self):
        # если указатель текущей команды равен максимальному, прираниваем его к нулю
        if self.UTK == len(self.algoritm)-1:
            self.UTK = 0
        else:
            self.UTK += 1
    # движение вперёд
    def move_to_way(self):
        new_coord1 = self.coord1
        new_coord2 = self.coord2


        if self.way == 1:
            if self.coord1 == 1:
                new_coord1 = 172

            else:
                new_coord1 = self.coord1 - 1
        if self.way == 2:
            if self.coord2 == 172:
                new_coord2 = 1


            else:
                new_coord2 = self.coord2 + 1

            if self.way ==4:
                if self.coord2 == 1:
                    new_coord2 = 172


                else:
                    new_coord2 = self.coord2 - 1
            if self.way == 3:
                if self.coord1 == 172:
                    new_coord1 = 1

                else:
                    new_coord1 = self.coord1 + 1
            if place[new_coord1][new_coord2] == 1:
                   place[self.coord1][self.coord2][self.coord3] = 0
                   self.coord1 = new_coord1
                   self.coord2 = new_coord2
                   self.coord3 = new_coord3
                   place[self.coord1][self.coord2][self.coord3] = 3

            self.UTK += [new_coord1][new_coord2][new_coord3]
            if self.UTK > len(self.algoritm) - 1:
                self.UTK = 0 + (self.UTK - len(self.algoritm) + 1)
            self.UTK += self.algoritm[self.UTK]
            if self.UTK > len(self.algoritm) - 1:
                self.UTK = 0 + (self.UTK - len(self.algoritm) + 1)











