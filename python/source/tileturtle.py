from turtle import *
from constants import SHAPESIZE


class TileTurtle(Turtle):
    def __init__(self, col, row, fill_color="white"):
        Turtle.__init__(self)
        self.shape("square")
        self.resizemode("user")
        self.shapesize(SHAPESIZE, SHAPESIZE, 0.1)
        self.pensize(0.1)
        self.col = col
        self.row = row
        self.color("black", fill_color)
        self.speed(0)
        self.pu()
        self.goto(col, row)
