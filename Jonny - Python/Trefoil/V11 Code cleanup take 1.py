#!/usr/bin/env python3

from math import pi, sin, cos
import turtle
from time import time

loop = "y"
while loop != "n" :
    print("The recommended resolution is 90")
    while not (resolution := input("Enter a resolution: ")).isdigit():
        pass
    resolution = int(resolution)

    try: grapher = turtle.Turtle()
    except turtle.Terminator: grapher = turtle.Turtle()
    grapher.penup()
    grapher.pensize(100)
    screen = grapher.getscreen()

    screen.tracer(0)

    startTime = time()
    for i in range(2 * resolution):
        supersubX = ( ( i * 247 ) / resolution ) / 3

        lsubX = 249 + supersubX
        usubX = 250 + supersubX
        lX = ( ( ( 3 * pi ) * ( lsubX + 1 ) ) / 500 )
        uX = ( ( ( 3 * pi ) * ( usubX + 1 ) ) / 500 )
        lbaseZ = int(round(( ( sin( lX ) + 1 ) / 2 ) * 16777215))
        ubaseZ = int(round(( ( sin( uX ) + 1 ) / 2 ) * 16777215))


        for j in range(resolution):
            T = ( 2 * pi * ( j + 1 ) ) / resolution
            X = 100 * ( ( ( 2 ) + ( cos( 3 * T ) ) ) * ( cos( 2 * T ) ) )
            Y = 100 * ( ( ( 2 ) + ( cos( 3 * T ) ) ) * ( sin( 2 * T ) ) )
            Z = int(round( ( ( 16777215 * sin( 3 * T ) ) + ( 16777215 ) ) / 2))

            if lbaseZ < Z < ubaseZ :
                colour = hex(Z)

                # Remove 0x from hex string for grapher.pencolor.
                colour = colour[2:]

                colour = "#" + colour.zfill(6)

                grapher.pencolor( colour )
                grapher.pendown()
            else:
                grapher.penup()
            grapher.goto(X, Y)

            # percent = str( ( j + 1 ) / ( resolution / 10 ) ) + "%"

        screen.title(f"{int((i + 1) / 2)}")

    screen.update()
    endTime = time()

    timing = round( endTime - startTime , 2 )

    print( timing , "seconds" )

    print("Loop? y/n")
    loop = input("> ")
    if not screen:
        print("here")
        screen.bye()
