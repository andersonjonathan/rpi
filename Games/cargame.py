# !/usr/bin/python
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..'))
sys.path.append(os.path.join(sys.path[0], '..', 'Adafruit'))
sys.path.append(os.path.join(sys.path[0], '..', 'Adafruit', 'Adafruit_CharLCD'))
sys.path.append(os.path.join(sys.path[0], '..', 'Adafruit', 'Adafruit_CharLCDPlate'))

import time
import Adafruit_CharLCD
import random

__author__ = 'jonathan'

LCD = Adafruit_CharLCD.Adafruit_CharLCDPlate()

# create some custom characters
LCD.create_char(1, [10, 31, 31, 10, 0, 0, 0, 0])  # Car in upper part of char
LCD.create_char(2, [0, 0, 0, 0, 10, 31, 31, 10])  # Car in lower part of char
LCD.create_char(3, [10, 31, 31, 10, 10, 31, 31, 10])  # 2 Cars in same char
LCD.create_char(4, [0, 0, 0, 0, 0, 0, 0, 0])  # No car
UPPER_CAR = '\x01'
LOWER_CAR = '\x02'
BOTH_CARS = '\x03'
NO_CARS = '\x04'
SELECT = Adafruit_CharLCD.SELECT
LEFT = Adafruit_CharLCD.LEFT
UP = Adafruit_CharLCD.UP
DOWN = Adafruit_CharLCD.DOWN
RIGHT = Adafruit_CharLCD.RIGHT


def draw_object(column, row, char):
    LCD.set_cursor(column, row)
    LCD.message(char)


def draw_car(car):
    draw_object(car.get_column(), car.get_row(), car.get_char())


def clear_screen():
    LCD.clear()


class UnknownDirectionError(Exception):
    pass


class Car(object):

    def __init__(self, column=None, row=None, char=None):
        if column:
            self._column = column
        else:
            self._column = 3
        if row:
            self._row = row
        else:
            self._row = 0
        if char:
            self._char = char
        else:
            self._char = UPPER_CAR

    def get_column(self):
        return self._column

    def get_row(self):
        return self._row

    def get_char(self):
        return self._char

    def set_column(self, column):
        self._column = column

    def set_row(self, row):
        self._row = row

    def set_char(self, char):
        self._char = char

    def move_up(self):
        if self.get_row() == 0:
            if self.get_char() == UPPER_CAR:
                pass
            else:
                self.set_char(UPPER_CAR)
        else:
            if self.get_char() == UPPER_CAR:
                self.set_row(0)
                self.set_char(LOWER_CAR)
            else:
                self.set_char(UPPER_CAR)

    def move_down(self):
        if self.get_row() == 0:
            if self.get_char() == UPPER_CAR:
                self.set_char(LOWER_CAR)
            else:
                self.set_row(1)
                self.set_char(UPPER_CAR)
        else:
            if self.get_char() == UPPER_CAR:
                self.set_char(LOWER_CAR)
            else:
                pass

    def move_left(self):
        self.set_column(self.get_column()-1)

    def move_right(self):
        self.set_column(self.get_column()+1)

    def move_forward(self):
        self.move_right()

    def __str__(self):
        return "col={:}, row={:}, char={:}".format(self._column, self._row, self._char)


class CarGame(object):
    
    def __init__(self):
        LCD.set_color(1.0, 1.0, 1.0)  # Turn on display
        clear_screen()  # Clear display
        self.player = Car()
        self.player.set_column(15)
        self.player.set_row(0)
        self.player.set_char(UPPER_CAR)
        self.score = 0
        self.opponents = []
        self.speed = 700
        self.probability = 40

    def init_screen(self):
        LCD.message('Driver \x01 \x02')
        time.sleep(1.0)

        # Show button state.
        clear_screen()
        LCD.message('PRESS SELECT TO \nSTART GAME...')
        while True:
            if LCD.is_pressed(SELECT):
                clear_screen()
                break
        self.game()

    def game(self):
        self.score = 0
        self.opponents = []
        gt = int(round(time.time() * 1000))
        up = False
        down = False
        right = False
        at = gt
        self.speed = 700
        self.probability = 40
        self.add_new_opponent()
        self.update()
        time.sleep(1.0)
        last3cars = [True]
        while True:
            gt = int(round(time.time() * 1000))
            update = False

            if LCD.is_pressed(UP):
                if not up:
                    up = True
                    update = True
                    self.player.move_up()
            else:
                up = False
            
            if LCD.is_pressed(DOWN):
                if not down:
                    down = True
                    update = True
                    self.player.move_down()
            else:
                down = False

            if LCD.is_pressed(SELECT):
                self.exit_game()
                break

            if LCD.is_pressed(RIGHT):
                if not right:
                    clear_screen()
                    draw_object(0, 0, "     PAUSE!\nPress > to cont.")
                    time.sleep(0.3)
                    while True:
                        if LCD.is_pressed(RIGHT):
                            break
                    update = True
                    diff = gt - at
                    gt = int(round(time.time() * 1000))
                    at = gt - diff
                    right = True
            else:
                right = False

            if at + self.speed < gt:
                at = gt
                update = True
                i = 0
                to_remove = []
                while i < len(self.opponents):
                    if self.opponents[i].get_column() == 15:
                        to_remove.append(i)
                        self.score += 1
                        if self.score % 10 == 0:
                            self.go_faster()
                    else:
                        self.opponents[i].move_forward()
                    i += 1
                for i in to_remove:
                    self.opponents.pop(i)
                r = random.randint(0, 100)
                if len(last3cars) == 3:
                    if False in last3cars:
                        pass
                    else:
                        r = 100
                    last3cars.pop(0)

                last3cars.append(r < self.probability)
                if r < self.probability:
                    self.add_new_opponent()
                
            if update:
                # update
                self.update()

    def go_faster(self):
        self.speed = int(round(self.speed*0.9))
        if self.speed < 300:
            self.speed = 300
            self.probability = int(round(self.probability*1.1))
        if self.probability > 95:
            self.probability = 95

    def add_new_opponent(self):
        if random.randint(0, 1):
            char = UPPER_CAR
        else:
            char = LOWER_CAR
        self.opponents.append(Car(3, random.randint(0, 1), char))

    def update(self):
        clear_screen()
        if self.collision_check():
            self.exit_game()
        draw_object(0, 0, "{0:03d}".format(self.score))
        draw_car(self.player)
        for o in self.opponents:
            draw_car(o)

    def collision_check(self):
        collision = False
        for o in self.opponents:
            if o.get_column() == 15:
                if o.get_row() == self.player.get_row():
                    if o.get_char() == self.player.get_char():
                        return True
                    else:
                        o.set_char(BOTH_CARS)
        return collision

    def exit_game(self):
        clear_screen()
        draw_object(0, 0, "   GAME OVER!!!\n SCORE: {0:07d}".format(self.score))
        try:
            highscore_file = open("car_game_highscore.txt", 'r')
            highscore = highscore_file.readline()
            highscore_file.close()
        except:
            highscore = ""

        if highscore == "":
            highscore = self.score
        new_highscore = False
        highscore = int(highscore)
        if highscore <= self.score:
            new_highscore = True
            highscore = self.score

            highscore_file = open("car_game_highscore.txt", 'w')
            highscore_file.write(str(self.score))
            highscore_file.close()

        time.sleep(3)
        clear_screen()
        if new_highscore:
            draw_object(0, 0, "NEW HIGHSCORE!!!\n    {0:08d}".format(highscore))
        else:
            draw_object(0, 0, "   HIGHSCORE:\n    {0:08d}".format(highscore))
        time.sleep(3)
        clear_screen()
        LCD.message('PRESS SELECT TO \nSTART GAME...')
        while True:
            if LCD.is_pressed(SELECT):
                clear_screen()
                self.game()
            if LCD.is_pressed(RIGHT):
                break
            if LCD.is_pressed(LEFT):
                break
            if LCD.is_pressed(UP):
                break
            if LCD.is_pressed(DOWN):
                break

        LCD.set_color(0, 0, 0)
        clear_screen()
        sys.exit()

if __name__ == '__main__':
    CarGame().init_screen()
