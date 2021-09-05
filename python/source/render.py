from turtle import *

k_base_box = [(0, 0), (0, 1), (1, 1), (1, 0)]
k_offset_in_pixels = (-150, -300)


def goto_offset(p):
    goto(p[0] + k_offset_in_pixels[0], p[1] + k_offset_in_pixels[1])


def draw_line(p0, p1, desired_width, desired_color):
    prev_width = width()
    color(desired_color)
    width(desired_width)
    goto_offset(p0)
    down()
    begin_fill()
    goto_offset(p1)
    end_fill()
    up()
    width(prev_width)


def draw_square(start, size, fill_color):
    color(fill_color)
    goto_offset(start)
    down()
    begin_fill()
    for p in k_base_box:
        goto_offset((start[0] + p[0] * size, start[1] + p[1] * size))
    end_fill()
    up()


def init():
    ht()
    speed(0)
    shape("classic")
    resizemode("user")
    shapesize(1, 1)
    width(1)
    up()
    colormode(255)
    color(0, 0, 0)
    return "EVENTLOOP"


def main_init(onleftclick, onmiddleclick, onrightclick):
    init()
    onscreenclick(onleftclick, 1)
    onscreenclick(onmiddleclick, 2)
    onscreenclick(onrightclick, 3)


if __name__ == "__main__":
    msg = init()
    print(msg)
    mainloop()
