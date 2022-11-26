import pygame as pg
import sys
import time
import random as rd
import copy

#Initializing
pg.init()

#Setting the screen
display = pg.display.set_mode((800, 600))

#Setting some default colors
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_maize = (231, 210, 190)
color_lblue = (157, 189, 241)
color_dorange = (211, 143, 93)
color_dkorange = (180, 150, 60)

#Render number
number_font = pg.font.SysFont(None, 48)

number_txt = dict()
#Render the powers of 2 into images
for i in range(1, 16):
    number_txt[2 ** i] = number_font.render(str(2 ** i), True, color_black)


#Create the main object of the game2048
class game_2048():

    #Initial the skeleton
    def __init__(self):
        self.skeleton = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],]

        #Initial the first two numbers
        self.new_num()
        self.new_num()

        #Create the history
        self.history = []

        #Indicate whether the game is ended
        self.end = False
        self.won = False

        #Counting scores
        # self.score = 0


        # Define a function to generate a new number in empty slot
    def new_num(self):

        # Use a list to store which slots are empty
        empty = []

        for i in range(0, 4):
            for j in range(0, 4):
                if self.skeleton[i][j] == 0:
                    empty.append(i * 4 + j)

        if len(empty) == 1:
            a = empty[0]

            i = a // 4
            j = a % 4

            self.skeleton[i][j] = 2

            count = 0
            for i in range(4):
                for j in range(4):
                    if j + 1 < 4:
                        if self.skeleton[i][j] != self.skeleton[i][j + 1]:
                            count += 1
                    if i + 1 < 4:
                        if self.skeleton[i][j] != self.skeleton[i + 1][j]:
                            count += 1

            if count == 24:
                self.end = True


        # Randomly choose an empty slot as 2
        a = rd.choice(empty)

        i = a // 4
        j = a % 4

        self.skeleton[i][j] = 2

        # Render the number and get its image location
        temp = number_txt[self.skeleton[i][j]]
        temp_locat = temp.get_rect()

        # Display the number according to its location in the skeleton
        temp_locat.x += (j + 2) * 100
        temp_locat.y += (i + 1) * 100 + 25
        display.blit(temp, temp_locat)

    #Define a function to operate when the user enters left
    def move_left(self):

        #Store the original skeleton to compare if any change is made and to store in the history
        flag = copy.deepcopy(self.skeleton)

        #Use a for loop to operate for each row of numbers
        for temp in self.skeleton:

            #leave all the zeros to the right
            temp.sort(key = lambda x: 1 if x == 0 else 0)

            temp = self.sum_forward(temp)
            # #Add the first two numbers if they are the same
            # if temp[0] == temp[1]:
            #     temp[0] = temp[0] + temp[1]
            #
            #     #Add the last two numbers if they are the same and leave the two sums in the first two slots
            #     if temp[2] == temp[3]:
            #         temp[1] = temp[2] + temp[3]
            #         temp[2] = 0
            #         temp[3] = 0
            #
            #     #Else keep the relative location
            #     else:
            #         temp[1], temp[2] = temp[2], temp[3]
            #         temp[3] = 0
            #
            #     if (temp[0] == 2048 or temp[1] == 2048) and not self.won:
            #         self.win()
            # else:
            #     #If the first two numbers are not the same, check the second and the third number
            #     if temp[1] == temp[2]:
            #         temp[1] = temp[1] + temp[2]
            #         temp[2] = temp[3]
            #         temp[3] = 0
            #
            #         if temp[1] == 2048 and not self.won:
            #             self.win()
            #
            #     #If they are not the same, check the last two numbers, leaving the remaining slots as zeros
            #     else:
            #         if temp[2] == temp[3]:
            #             temp[2] = temp[2] + temp[3]
            #             temp[3] = 0
            #
            #             if temp[2] == 2048 and not self.won:
            #                 self.win()

        #If the original numbers are different to the result, generate a new number and store the last version into the history
        if flag != self.skeleton:
            self.new_num()

            #Drop the first version in the history if the history contains more than 10 records
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)


    #See also move_left
    def move_right(self):
        flag = copy.deepcopy(self.skeleton)
        for temp in self.skeleton:
            temp.sort(key = lambda x: 0 if x == 0 else 1)
            # if temp[3] == temp[2]:
            #     temp[3] = temp[3] + temp[2]
            #
            #     if temp[1] == temp[0]:
            #         temp[2] = temp[1] + temp[0]
            #         temp[1] = 0
            #         temp[0] = 0
            #     else:
            #         temp[2], temp[1] = temp[1], temp[0]
            #         temp[0] = 0
            #
            #     if (temp[0] == 2048 or temp[1] == 2048) and not self.won:
            #         self.win()
            # else:
            #     if temp[2] == temp[1]:
            #         temp[2] = temp[2] + temp[1]
            #         temp[1] = temp[0]
            #         temp[0] = 0
            #
            #         if temp[1] == 2048 and not self.won:
            #             self.win()
            #
            #     else:
            #         if temp[1] == temp[0]:
            #             temp[1] = temp[1] + temp[0]
            #             temp[0] = 0
            temp = self.sum_backword(temp)

        if flag != self.skeleton:
            self.new_num()
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)


    #See also move_left
    def move_up(self):
        flag = copy.deepcopy(self.skeleton)
        for i in range(0,4):
            temp = [x[i] for x in self.skeleton]
            temp.sort(key = lambda x: 1 if x == 0 else 0)
            # if temp[0] == temp[1]:
            #     temp[0] = temp[0] + temp[1]
            #
            #     if temp[2] == temp[3]:
            #         temp[1] = temp[2] + temp[3]
            #         temp[2] = 0
            #         temp[3] = 0
            #     else:
            #         temp[1], temp[2] = temp[2], temp[3]
            #         temp[3] = 0
            #
            #     if (temp[0] == 2048 or temp[1] == 2048) and not self.won:
            #         self.win()
            #
            # else:
            #     if temp[1] == temp[2]:
            #         temp[1] = temp[1] + temp[2]
            #         temp[2] = temp[3]
            #         temp[3] = 0
            #
            #     else:
            #         if temp[2] == temp[3]:
            #             temp[2] = temp[2] + temp[3]
            #             temp[3] = 0
            temp = self.sum_forward(temp)

            for j in range(0,4):
                self.skeleton[j][i] = temp[j]
        if flag != self.skeleton:
            self.new_num()
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)


    #See also move_left
    def move_down(self):
        flag = copy.deepcopy(self.skeleton)
        for i in range(0, 4):
            temp = [x[i] for x in self.skeleton]
            temp.sort(key=lambda x: 0 if x == 0 else 1)

            temp = self.sum_backword(temp)
            # if temp[3] == temp[2]:
            #     temp[3] = temp[3] + temp[2]
            #
            #     if temp[1] == temp[0]:
            #         temp[2] = temp[1] + temp[0]
            #         temp[1] = 0
            #         temp[0] = 0
            #     else:
            #         temp[2], temp[1] = temp[1], temp[0]
            #         temp[0] = 0
            #
            #     if (temp[0] == 2048 or temp[1] == 2048) and not self.won:
            #         self.win()
            #
            # else:
            #     if temp[2] == temp[1]:
            #         temp[2] = temp[2] + temp[1]
            #         temp[1] = temp[0]
            #         temp[0] = 0
            #     else:
            #         if temp[1] == temp[0]:
            #             temp[1] = temp[1] + temp[0]
            #             temp[0] = 0

            for j in range(0, 4):
                self.skeleton[j][i] = temp[j]

        if flag != self.skeleton:
            self.new_num()
            if len(self.history) == 10:
                self.history = self.history[1:]
            self.history.append(flag)

    def sum_forward(self, temp):
        # Add the first two numbers if they are the same
        if temp[0] == temp[1]:
            temp[0] = temp[0] + temp[1]

            # Add the last two numbers if they are the same and leave the two sums in the first two slots
            if temp[2] == temp[3]:
                temp[1] = temp[2] + temp[3]
                temp[2] = 0
                temp[3] = 0

            # Else keep the relative location
            else:
                temp[1], temp[2] = temp[2], temp[3]
                temp[3] = 0

            if (temp[0] == 2048 or temp[1] == 2048) and not self.won:
                self.win()
        else:
            # If the first two numbers are not the same, check the second and the third number
            if temp[1] == temp[2]:
                temp[1] = temp[1] + temp[2]
                temp[2] = temp[3]
                temp[3] = 0

                if temp[1] == 2048 and not self.won:
                    self.win()

            # If they are not the same, check the last two numbers, leaving the remaining slots as zeros
            else:
                if temp[2] == temp[3]:
                    temp[2] = temp[2] + temp[3]
                    temp[3] = 0

                    if temp[2] == 2048 and not self.won:
                        self.win()
        return temp

    def sum_backword(self, temp):
        if temp[3] == temp[2]:
            temp[3] = temp[3] + temp[2]

            if temp[1] == temp[0]:
                temp[2] = temp[1] + temp[0]
                temp[1] = 0
                temp[0] = 0
            else:
                temp[2], temp[1] = temp[1], temp[0]
                temp[0] = 0

            if (temp[3] == 2048 or temp[2] == 2048) and not self.won:
                self.win()
        else:
            if temp[2] == temp[1]:
                temp[2] = temp[2] + temp[1]
                temp[1] = temp[0]
                temp[0] = 0

                if temp[2] == 2048 and not self.won:
                    self.win()

            else:
                if temp[1] == temp[0]:
                    temp[1] = temp[1] + temp[0]
                    temp[0] = 0

                    if temp[1] == 2048 and not self.won:
                        self.win()
        return temp


    #If any history is stored, return to the last version
    def undo(self):
        if len(self.history) > 0:
            self.skeleton = self.history.pop()


    def end_game(self):

        note = pg.font.SysFont(None, 56)
        note1 = note.render("There's no empty slot!!", True, color_black)
        note2 = note.render("Game Over", True, color_black)
        restart = note.render("Restart", True, color_black)

        note1_locat = note1.get_rect()
        note1_locat.x += 200
        note1_locat.y += 150

        note2_locat = note2.get_rect()
        note2_locat.x += 300
        note2_locat.y += 250

        restart_locat = restart.get_rect()
        restart_locat.x += 325
        restart_locat.y += 350

        display.fill(color_maize)
        mouse = pg.mouse.get_pos()

        if 325 <= mouse[0] <= 475 and 350 <= mouse[1] <= 400:
            pg.draw.rect(display, color_dkorange, [325, 350, 150, 50])
        else:
            pg.draw.rect(display, color_dorange, [325, 350, 150, 50])

        display.blit(note1, note1_locat)
        display.blit(note2, note2_locat)
        display.blit(restart, restart_locat)
        pg.display.flip()


    def win(self):
        self.won = True

        note = pg.font.SysFont(None, 56)
        note1 = note.render("You've reached 2048!!", True, color_black)
        conti = note.render("Continue", True, color_black)
        restart = note.render("Restart", True, color_black)

        note1_locat = note1.get_rect()
        note1_locat.x += 200
        note1_locat.y += 150

        conti_locat = conti.get_rect()
        conti_locat.x += 325
        conti_locat.y += 250

        restart_locat = restart.get_rect()
        restart_locat.x += 325
        restart_locat.y += 350

        display.fill(color_maize)
        mouse = pg.mouse.get_pos()

        if 325 <= mouse[0] <= 475 and 250 <= mouse[1] <= 300:
            pg.draw.rect(display, color_dkorange, [325, 250, 150, 50])
        else:
            pg.draw.rect(display, color_dorange, [325, 250, 150, 50])

        if 325 <= mouse[0] <= 475 and 350 <= mouse[1] <= 400:
            pg.draw.rect(display, color_dkorange, [325, 350, 150, 50])
        else:
            pg.draw.rect(display, color_dorange, [325, 350, 150, 50])

        display.blit(note1, note1_locat)
        display.blit(conti, conti_locat)
        display.blit(restart, restart_locat)

        pg.display.flip()



#Render instruction texts
instruct = pg.font.SysFont(None, 32)
instruct_rend = []
instruct_rend.append(instruct.render('How to play', True, color_black))
instruct_rend.append(instruct.render('Move: up/W, down/S, left/A, right/D', True, color_black))
instruct_rend.append(instruct.render('Undo: Backspace', True, color_black))

def initial_screen():
    # Paint the screen
    display.fill(color_maize)

    #Print texts at the top of the screen
    for i in range(len(instruct_rend)):
        instruct_locat = instruct_rend[i].get_rect()
        instruct_locat.y += 32 * i
        display.blit(instruct_rend[i], instruct_locat)


    #Paint the background color for numbers
    for i in range(0, 4):
        for j in range(0, 4):
            temp_x = (j + 2) * 100
            temp_y = (i + 1) * 100
            pg.draw.rect(display, color_dorange, (temp_x, temp_y, 80, 80), 0)

initial_screen()

#Initial the game
game = game_2048()


#Refresh the screen
pg.display.flip()

def game_start(game):
    #Use the while loop to run the game until user want to exit
    while True:

        #Reading user input constantly
        for event in pg.event.get():

            #If quit is entered, exit the game
            if event.type == pg.QUIT:
                sys.exit()

            #Read other possible entries( KEYDOWN: detect when user press the button)
            elif event.type == pg.KEYDOWN:

                #Run the corresponding function of game
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    game.move_left()
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    game.move_right()
                if event.key == pg.K_UP or event.key == pg.K_w:
                    game.move_up()
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    game.move_down()
                if event.key == pg.K_BACKSPACE:
                    game.undo()


                #Refresh the screen

                #Rerender the instruction
                for i in range(len(instruct_rend)):
                    instruct_locat = instruct_rend[i].get_rect()
                    instruct_locat.y += 32 * i
                    display.blit(instruct_rend[i], instruct_locat)

                #Rerender the new result and the background color
                for i in range(0, 4):
                    for j in range(0, 4):

                        #set the location of the background accordingly
                        temp_x = (j + 2) * 100
                        temp_y = (i + 1) * 100
                        pg.draw.rect(display, color_dorange, (temp_x, temp_y, 80, 80), 0)

                        #Only print the number if it's not 0
                        if game.skeleton[i][j] != 0:
                            temp = number_txt[game.skeleton[i][j]]

                            #Set the location of the number accordingly
                            temp_locat = temp.get_rect()
                            temp_locat.x += (j + 2) * 100
                            temp_locat.y += (i + 1) * 100 + 25
                            display.blit(temp, temp_locat)

                        #Refresh the screen to display
                        pg.display.flip()

                if game.end:
                    time.sleep(2.5)
                    while game.end:
                        game.end_game()
                        for event in pg.event.get():
                            # If quit is entered, exit the game
                            if event.type == pg.QUIT:
                                sys.exit()
                            elif event.type == pg.MOUSEBUTTONUP:
                                if 325 <= mouse[0] <= 475 and 350 <= mouse[1] <= 400:
                                    initial_screen()
                                    game = game_2048()
                                    pg.display.flip()

                        mouse = pg.mouse.get_pos()
