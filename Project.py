import pygame as pg
import sys
import time
import random as rd
import copy

#Initializing
pg.init()
display = pg.display.set_mode((800, 600))

color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_maize = (231, 210, 190)
color_lblue = (157, 189, 241)
color_dorange = (211, 143, 93)

#Render number
number_font = pg.font.SysFont(None, 48)
number_txt = dict()
number_rect = dict()
for i in range(1, 16):
    number_txt[2 ** i] = number_font.render(str(2 ** i), True, color_black)
    # number_rect[2 ** i] = number_txt[2 ** i].get_rect()

class game_2048():

    def __init__(self):
        self.skeleton = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],]
        self.new_num()
        self.history = []



    def new_num(self):
        empty = []

        for i in range(0, 4):
            for j in range(0, 4):
                if self.skeleton[i][j] == 0:
                    empty.append(i * 4 + j)

        a = rd.sample(empty, 1)

        i = a[0] // 4
        j = a[0] % 4

        self.skeleton[i][j] = 2
        temp = number_txt[self.skeleton[i][j]]
        temp_locat = temp.get_rect()
        temp_locat.x += (j + 2) * 100
        temp_locat.y += (i + 1) * 100 + 25
        display.blit(temp, temp_locat)



    def move_left(self):
        flag = copy.deepcopy(self.skeleton)
        for temp in self.skeleton:
            temp.sort(key = lambda x: 1 if x == 0 else 0)

            if temp[0] == temp[1]:
                temp[0] = temp[0] + temp[1]


                if temp[2] == temp[3]:
                    temp[1] = temp[2] + temp[3]
                    temp[2] = 0
                    temp[3] = 0
                else:
                    temp[1], temp[2] = temp[2], temp[3]
                    temp[3] = 0
            else:
                if temp[1] == temp[2]:
                    temp[1] = temp[1] + temp[2]
                    temp[2] = temp[3]
                    temp[3] = 0


                else:
                    if temp[2] == temp[3]:
                        temp[2] = temp[2] + temp[3]
                        temp[3] = 0


        if flag != self.skeleton:
            self.new_num()
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)

    def move_right(self):
        flag = copy.deepcopy(self.skeleton)
        for temp in self.skeleton:
            temp.sort(key = lambda x: 0 if x == 0 else 1)
            if temp[3] == temp[2]:
                temp[3] = temp[3] + temp[2]


                if temp[1] == temp[0]:
                    temp[2] = temp[1] + temp[0]
                    temp[1] = 0
                    temp[0] = 0
                else:
                    temp[2], temp[1] = temp[1], temp[0]
                    temp[0] = 0
            else:
                if temp[2] == temp[1]:
                    temp[2] = temp[2] + temp[1]
                    temp[1] = temp[0]
                    temp[0] = 0


                else:
                    if temp[1] == temp[0]:
                        temp[1] = temp[1] + temp[0]
                        temp[0] = 0

        if flag != self.skeleton:
            self.new_num()
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)

    def move_up(self):
        flag = copy.deepcopy(self.skeleton)
        for i in range(0,4):
            temp = [x[i] for x in self.skeleton]
            temp.sort(key = lambda x: 1 if x == 0 else 0)
            if temp[0] == temp[1]:
                temp[0] = temp[0] + temp[1]


                if temp[2] == temp[3]:
                    temp[1] = temp[2] + temp[3]
                    temp[2] = 0
                    temp[3] = 0
                else:
                    temp[1], temp[2] = temp[2], temp[3]
                    temp[3] = 0
            else:
                if temp[1] == temp[2]:
                    temp[1] = temp[1] + temp[2]
                    temp[2] = temp[3]
                    temp[3] = 0

                else:
                    if temp[2] == temp[3]:
                        temp[2] = temp[2] + temp[3]
                        temp[3] = 0


            for j in range(0,4):
                self.skeleton[j][i] = temp[j]
        if flag != self.skeleton:
            self.new_num()
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)

    def move_down(self):
        flag = copy.deepcopy(self.skeleton)
        for i in range(0, 4):
            temp = [x[i] for x in self.skeleton]
            temp.sort(key=lambda x: 0 if x == 0 else 1)
            if temp[3] == temp[2]:
                temp[3] = temp[3] + temp[2]


                if temp[1] == temp[0]:
                    temp[2] = temp[1] + temp[0]
                    temp[1] = 0
                    temp[0] = 0
                else:
                    temp[2], temp[1] = temp[1], temp[0]
                    temp[0] = 0

            else:
                if temp[2] == temp[1]:
                    temp[2] = temp[2] + temp[1]
                    temp[1] = temp[0]
                    temp[0] = 0
                else:
                    if temp[1] == temp[0]:
                        temp[1] = temp[1] + temp[0]
                        temp[0] = 0

            for j in range(0, 4):
                self.skeleton[j][i] = temp[j]

        if flag != self.skeleton:
            self.new_num()
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)

    def undo(self):
        if len(self.history) > 0:
            self.skeleton = self.history.pop()


display.fill(color_maize)

for i in range(0, 4):
    for j in range(0, 4):
        temp_x = (j + 2) * 100
        temp_y = (i + 1) * 100
        pg.draw.rect(display, color_dorange, (temp_x, temp_y, 80, 80), 0)

game = game_2048()

pg.display.flip()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                game.move_left()
            if event.key == pg.K_RIGHT:
                game.move_right()
            if event.key == pg.K_UP:
                game.move_up()
            if event.key == pg.K_DOWN:
                game.move_down()
            if event.key == pg.K_BACKSPACE:
                game.undo()

            display.fill(color_maize)
            pg.display.flip()
            temp = []
            for i in range(0, 4):
                for j in range(0, 4):

                    temp_x = (j + 2) * 100
                    temp_y = (i + 1) * 100
                    pg.draw.rect(display, color_dorange, (temp_x, temp_y, 80, 80), 0)

                    if game.skeleton[i][j] != 0:
                        temp = number_txt[game.skeleton[i][j]]
                        temp_locat = temp.get_rect()
                        temp_locat.x += (j + 2) * 100
                        temp_locat.y += (i + 1) * 100 + 25
                        display.blit(temp, temp_locat)
                    pg.display.flip()