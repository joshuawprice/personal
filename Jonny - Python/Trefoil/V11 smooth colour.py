from math import *
import turtle
from time import time
loop = " y "
while loop != "n" :
    print("recomendation: 90")
    res = input( " resolution : " )
    while not res.isdigit() :
        res = input( " resolution ( as an integer ) : " )
    res = int( res )

    grapher = turtle.Turtle()
    grapher.penup()
    grapher.pensize(100)
    grapher.speed(0)
    Screen = turtle.getscreen()
    turtle.tracer(n=0,delay=0)
    
    start = time()
    for i in range ( 2 * res ) :
        runcount = i
        supersubX = ( ( i * 247 ) / res ) / 3

        lsubX = 249 + supersubX
        usubX = 250 + supersubX
        lX = ( ( ( 3 * pi ) * ( lsubX + 1 ) ) / 500 )
        uX = ( ( ( 3 * pi ) * ( usubX + 1 ) ) / 500 )
        lbaseZ = ( ( sin( lX ) + 1 ) / 2 ) * 16777215
        ubaseZ = ( ( sin( uX ) + 1 ) / 2 ) * 16777215 
        
        lbaseZint = int( lbaseZ )
        ubaseZint = int( ubaseZ )
        hexlbaseZint = hex(lbaseZint)
        hexubaseZint = hex(lbaseZint)

        for i in range ( res ) :
            
            T = ( 2 * pi * ( i + 1 ) ) / res
            X = 100 * ( ( ( 2 ) + ( cos( 3 * T ) ) ) * ( cos( 2 * T ) ) )
            Y = 100 * ( ( ( 2 ) + ( cos( 3 * T ) ) ) * ( sin( 2 * T ) ) )
            Z = sin( 3 * T )
            Z = (pi * Z) + pi
            A= floor(128*(1 + cos(Z)))
            if A < 16:
                A= str(hex(A))[1 : : ][1 : : ]
                A= "0"+A
            else:
                A= str(hex(A))[1 : : ][1 : : ]
                
            
            B= floor(128*(1 + sin(Z)))
            if B < 16:
                B= str(hex(B))[1 : : ][1 : : ]
                B= "0"+B
            else:
                B= str(hex(B))[1 : : ][1 : : ]

            C=B
            ABC = ("0x"+A+B+B)
            ABCint = int(ABC,16)
            ABC = "#" + ABC[1 : : ][1 : : ]
            
            
            






            

            if lbaseZint < ABCint < ubaseZint :
                print(lbaseZint,ABCint,ubaseZint)
                print("yes")
                
                grapher.pencolor( ABC )
                grapher.pendown()
            else:
                grapher.penup()
            grapher.goto( X , Y )
                  
            percent = str( ( i + 1 ) / ( res / 10 ) )
            percentstr = str( percent + "%" )
        
            title = str( int( ( runcount + 1 ) / 2 ) )
            Screen.title( title )
    turtle.update()
    end = time()

    timeing = round( float( end - start ) , 2 )

    print( timeing , "seconds" )

    loop = input( "loop? y/n" )
    Screen.clear()

exit()

