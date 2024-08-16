#!/usr/bin/env python3

from math import pi, sin, cos, asin
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

    # screen.tracer(0)

    startTime = time()
   
    X1b=0
    Y1b=0
    X2b=0
    Y2b=0
    X3b=0
    Y3b=0
    X4b=0
    Y4b=0
    X5b=0
    Y5b=0
    X6b=0
    Y6b=0




    for i in range(2 * resolution):
        supersubX = ( ( i * 247 ) / resolution ) / 3

        lsubX = 249 + supersubX
        usubX = 250 + supersubX
        lX = ( ( ( 3 * pi ) * ( lsubX + 1 ) ) / 500 )
        uX = ( ( ( 3 * pi ) * ( usubX + 1 ) ) / 500 )
        lbaseZ = int(round(( ( sin( lX ) + 1 ) / 2 ) * 16777215))
        ubaseZ = int(round(( ( sin( uX ) + 1 ) / 2 ) * 16777215))

        Z = int(round((lbaseZ+ubaseZ)/2))
        colour = hex(Z)
        colour = colour[2:]
        colour = "#" + colour.zfill(6)
        grapher.pencolor( colour )


        T=[
            (2*pi*0-asin(1-(2*Z)/16777215))/3,
            (2*pi*1-asin(1-(2*Z)/16777215))/3,
            (2*pi*2-asin(1-(2*Z)/16777215))/3,
            (2*pi*0+asin(1-(2*Z)/16777215)+pi)/3,
            (2*pi*1+asin(1-(2*Z)/16777215)+pi)/3,
            (2*pi*2+asin(1-(2*Z)/16777215)+pi)/3
        ]
   
        X1a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[0] ) ) ) * ( cos( 2 * T[0] ) ) ))
        Y1a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[0] ) ) ) * ( sin( 2 * T[0] ) ) ))
        X2a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[1] ) ) ) * ( cos( 2 * T[1] ) ) ))
        Y2a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[1] ) ) ) * ( sin( 2 * T[1] ) ) ))
        X3a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[2] ) ) ) * ( cos( 2 * T[2] ) ) ))
        Y3a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[2] ) ) ) * ( sin( 2 * T[2] ) ) ))
        X4a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[3] ) ) ) * ( cos( 2 * T[3] ) ) ))
        Y4a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[3] ) ) ) * ( sin( 2 * T[3] ) ) ))
        X5a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[4] ) ) ) * ( cos( 2 * T[4] ) ) ))
        Y5a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[4] ) ) ) * ( sin( 2 * T[4] ) ) ))
        X6a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[5] ) ) ) * ( cos( 2 * T[5] ) ) ))
        Y6a = ( 100 * ( ( ( 2 ) + ( cos( 3 * T[5] ) ) ) * ( sin( 2 * T[5] ) ) ))

        listA = [X1a,Y1a,X2a,Y2a,X3a,Y3a,X4a,Y4a,X5a,Y5a,X6a,Y6a]
        lsitB = [X1b,Y1b,X2b,Y2b,X3b,Y3b,X4b,Y4b,X5b,Y5b,X6b,Y6b]

        grapher.goto(X1b, Y1b)
        if i != 0:
            grapher.pendown()
        grapher.goto(X1a, Y1a)
        grapher.penup()
        grapher.goto(X2b, Y2b)
        if i != 0:
            grapher.pendown()
        grapher.goto(X2a, Y2a)
        grapher.penup()
        grapher.goto(X3b, Y3b)
        if i != 0:
            grapher.pendown()
        grapher.goto(X3a, Y3a)
        grapher.penup()
        grapher.goto(X4b, Y4b)
        if i != 0:
            grapher.pendown()
        grapher.goto(X4a, Y4a)
        grapher.penup()
        grapher.goto(X5b, Y5b)
        if i != 0:
            grapher.pendown()
        grapher.goto(X5a, Y5a)
        grapher.penup()
        grapher.goto(X6b, Y6b)
        if i != 0:
            grapher.pendown()
        grapher.goto(X6a, Y6a)
        grapher.penup()

        X1b = X1a
        Y1b = Y1a
        X2b = X2a
        Y2b = Y2a
        X3b = X3a
        Y3b = Y3a
        X4b = X4a
        Y4b = Y4a
        X5b = X5a
        Y5b = Y5a
        X6b = X6a
        Y6b = Y6a

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
