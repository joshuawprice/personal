#!/usr/bin/env python3


from math import pi, sin, cos, asin
import turtle
from time import time

loop = "y"
while loop != "n":
    print("The recommended resolution is 90")
    while not (resolution := input("Enter a resolution: ")).isdigit():
        pass
    resolution = int(resolution)

    try:
        grapher = turtle.Turtle()
    except turtle.Terminator:
        grapher = turtle.Turtle()
    grapher.penup()
    grapher.pensize(100)
    screen = grapher.getscreen()

    screen.tracer(0)

    startTime = time()

    X_previous = [0 for _ in range(6)]
    Y_previous = [0 for _ in range(6)]

    for i in range(resolution+1):
        Z = i*(1/resolution)

        colour = hex(round(Z * 16777215))
        # Remove 0x from hex string for grapher.pencolor().
        colour = colour[2:]
        colour = "#" + colour.zfill(6)
        grapher.pencolor(colour)

        T_equations = []
        T_equations.extend(
            [(2*pi*k-asin(1-(2*Z)))/3 for k in range(3)])
        T_equations.extend(
            [(2*pi*k+asin(1-(2*Z))+pi)/3 for k in range(3)])

        X = []
        Y = []

        for n, T in enumerate(T_equations):
            X.append(100 * (((2) + (cos(3 * T))) * (cos(2 * T))))
            Y.append(100 * (((2) + (cos(3 * T))) * (sin(2 * T))))

            if i > 0:
                grapher.goto(X_previous[n], Y_previous[n])
                grapher.pendown()
                grapher.goto(X[n], Y[n])
                grapher.penup()

            X_previous[n], Y_previous[n] = X[n], Y[n]

        screen.title(f"{round(i/(resolution)*100,2)}%")
    screen.update()
    endTime = time()

    timing = round(endTime - startTime, 2)

    print(timing, "seconds")

    print("Loop? y/n")
    loop = input("> ")

    if not screen:
        print("here")
        screen.bye()
