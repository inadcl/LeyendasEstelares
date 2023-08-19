from asyncio import sleep

import pygame

global x_offset
global y_offset
global scale_width
global scale_height
global full_width
global full_height

def init():
    print("Scale Width:", scale_width)
    print("Scale Height:", scale_height)
    print("X Offset:", x_offset)
    print("Y Offset:", y_offset)

def getWidthPosition(x):
    init()
    return x+ scale_width * x_offset


def getHeightPosition(y):
    return y + scale_height * y_offset

def getFullHeight():
    return scale_height+y_offset