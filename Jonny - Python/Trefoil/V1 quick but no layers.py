from math import *
import turtle

grapher = turtle.Turtle()
grapher.penup()
grapher.pensize(100)
grapher2 = turtle.Turtle()
grapher2.penup()
grapher2.pensize(100)
grapher3 = turtle.Turtle()
grapher3.penup()
grapher3.pensize(100)

Screen = turtle.getscreen()
for i in range (100):
    T =  (2*pi*(i+101))/100
    X = 100 * ( ( ( 2 ) + ( cos( 3 * T ) ) ) * ( cos( 2 * T ) ) )
    Y = 100 * ( ( ( 2 ) + ( cos( 3 * T ) ) ) * ( sin( 2 * T ) ) )
    Z = round(((16777215*sin(3*T))+(16777215))/2,0)

    Zint = int(Z)
    Hex= hex(Zint)
    print(X,Y,Z)
    print(Hex)
    colur = str(Hex)
    if colur[1] == "0":
        colur = colur[1 :  : ]
    elif colur[1] == "x":
        colur = colur[1 :  : ]

    print(len(colur))

    print(colur)
    
    if len(colur) == 2:
        print(colur[1])
    if len(colur) == 3:
        print(colur[2])
    if len(colur) == 4:
        print(colur[3])
    if len(colur) == 5:
        print(colur[4])
    if len(colur) == 6:
        print(colur[5])
    if len(colur) == 7:
        print(colur[6])

    print(colur)
    #if len(colur) == 0:
        #colur = str("0" + "0" + "0" + "0" + "0" + "0" + "0" + colur[4] + colur[5] + colur[6])
    if len(colur) == 1:
        colur = str("0" + "0" + "0" + "0" + "0" + "0")
    if len(colur) == 2:
        colur = str("0" + "0" + "0" + "0" + "0" + colur[1])
    if len(colur) == 3:
        colur = str("0" + "0" + "0" + "0" + colur[1] + colur[2])
    if len(colur) == 4:
        colur = str("0" + "0" + "0" + colur[1] + colur[2] + colur[3])
    if len(colur) == 5:
        colur = str("0" + "0" + colur[1] + colur[2] + colur[3] + colur[4])
    if len(colur) == 6:
        colur = str("0" + colur[1] + colur[2] + colur[3] + colur[4] + colur[5] )
    if len(colur) == 7:
        colur = str(colur[1] + colur[2] + colur[3] + colur[4] + colur[5] + colur[6])
    
    print(colur)
    
    colour = str("#"+colur)
    print(colour)
    grapher.pencolor(colour)


    grapher.goto(X,Y)
    grapher.pendown()

    percent = str(((i+1)/100)*100)
    percentstr = str(percent + "%")
    print(percent)
    Screen.title(percentstr)

