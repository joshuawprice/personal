from math import pi, sin, cos
from tkinter import *
import turtle############Importing librarys/#

class inputs :######Setting up classes##
    pass                                    #
BoundMin = inputs()                    #
BoundMax = inputs()
LHSREALINPUT = inputs()
LHSEQUATION = inputs()
VARONE=inputs()
OPONE=inputs()
VARTWO=inputs()

VARchoices = {'x','θ','R'}
OPchoices = {'+','-','x','/','^'}

GUI = Tk()
#####################Tkinter loop##

                                            ##
def Mindone() :                             ###Button effects##
    BoundMin.input = int( Min.get() )                         #
    Minbut[ "state" ]= DISABLED                               #
    Min[ "state" ] = DISABLED                                 #
    if Max[ "state" ] == "disabled" :
        LHSREAL[ "state" ] = ACTIVE
        LHSTHETA[ "state" ] = ACTIVE
        LHSR[ "state" ] = ACTIVE
                                                
def Maxdone() :                                               #
    BoundMax.input = int( Max.get() )                         #
    Maxbut[ "state" ] = DISABLED                              #
    Max[ "state" ] = DISABLED                                 #
    if Min[ "state" ] == "disabled" :
        LHSREAL[ "state" ] = ACTIVE
        LHSTHETA[ "state" ] = ACTIVE
        LHSR[ "state" ] = ACTIVE
        
def LHSREALdone() :
    GUI.destroy()
    GUI_LHSREALINPUT = Tk()
    def  DONEdone() :
        LHSREALINPUT.input = int(INPUT.get())
        GUI_LHSREALINPUT.destroy()
    INPUT = Spinbox( GUI_LHSREALINPUT , from_ = -120000 , to = 120000 , wrap = True )
    INPUT.grid( row = 0 , column = 0 )
    DONE = Button( GUI_LHSREALINPUT , text = "done" , command = DONEdone )
    DONE.grid( row = 0 , column = 1 )
    GUI_LHSREALINPUT.mainloop()

    LHSEQUATION.input = str(LHSREALINPUT.input)
def LHSTHETAdone() :
    GUI.destroy()
    LHSEQUATION.input = str("θ")

def LHSRdone() :
    GUI.destroy()
    LHSEQUATION.input = str("R")


Bounds = Label( GUI , text = "θ = πX/120 , where X is an int, -120000<X<120000" )#########Widget setup##
Bounds.grid( row = 0 , column = 0 )                                                                    #
Mintxt = Label( GUI , text = "X                >" )                                                    #
Maxtxt = Label( GUI , text = "X                <" )                                                    #
Mintxt.grid( row = 1 , column = 0 )                                                                    #
Maxtxt.grid( row = 2 , column = 0 )                                                                    #
Min = Spinbox( GUI , from_ = -120000 , to = 120000 , wrap = True )                                     #
Min.delete(0,"end")                                                                                    #
Min.insert(0,"0")                                                                                      #
Max = Spinbox( GUI , from_ = -120000 , to = 120000 , wrap = True )                                     #
Max.delete(0,"end")                                                                                    #
Max.insert(0,"240")                                                                                    #
Min.grid( row = 1 , column = 1 )                                                                       #
Max.grid( row = 2 , column = 1 )                                                                       #
Minbut = Button( GUI , text = "done" , command = Mindone )                                             #
Maxbut = Button( GUI , text = "done" , command = Maxdone )                                             # 
Minbut.grid( row = 1 , column = 2 )                                                                    #
Maxbut.grid( row = 2 , column = 2 )
LHStxt = Label( GUI , text = "Left Hand Side of the Equation" )
LHStxt.grid( row = 3 , column = 1 )
LHSREAL = Button(GUI , text = "Real number" , command = LHSREALdone , state = "disabled" )
LHSREAL.grid( row = 4 , column = 0 )
LHSTHETA = Button(GUI , text = "Theta" , command = LHSTHETAdone , state = "disabled" )
LHSTHETA.grid( row = 4 , column = 1 )
LHSR = Button(GUI , text = "R" , command = LHSRdone , state = "disabled" )
LHSR.grid( row = 4 , column = 2 )

                                            #
                                            #
GUI.mainloop()#################Tkinter loop/#

LHSOFTHEEQUATION = LHSEQUATION.input + "="

GUI_RHS = Tk()

def RHSconfirmationcommand() :
    Var_1[ "state" ] = DISABLED
    Op_1[ "state" ] = DISABLED
    OPONE.input = op1.get()
    Var_2[ "state" ] = DISABLED
    RHSconfirmation[ "state" ] = DISABLED
    if var1.get() == "x":
        REALVAR1["state"] = NORMAL
        Confirmrealvalues["state"] = ACTIVE
    if var2.get() == "x":
        REALVAR2["state"] = NORMAL
        Confirmrealvalues["state"] = ACTIVE
    if var2.get() != "x":
        VARTWO.input = var2.get()
    if var1.get() != "x":
        VARONE.input = var1.get()
        
        if var2.get() != "x":
            GUI_RHS.destroy()

def Confirmrealvaluescommand() :
    if var1.get() == "x":
        VARONE.input = REALVAR1.get()
        REALVAR1["state"] = DISABLED
    if var2.get() == "x":
        VARTWO.input = REALVAR2.get()
        REALVAR2["state"] = DISABLED
    GUI_RHS.destroy()
    
        
    



RHS = Label( GUI_RHS , text = "Input RHS Variables:" )
RHS.grid( row = 0 , column = 0 )
Vartext_1 = Label(GUI_RHS , text = "Var_1" )
Vartext_1.grid( row = 0 , column = 1 )
Optext_1 = Label(GUI_RHS , text = "Operation")
Optext_1.grid( row = 0 , column = 2 )
Vartext_2 = Label(GUI_RHS , text = "Var_2")
Vartext_2.grid( row = 0 , column = 3 )
LHS = Label(GUI_RHS , text = LHSOFTHEEQUATION )
LHS.grid( row = 1 , column = 0 )
var1 = StringVar(GUI_RHS)
op1 = StringVar(GUI_RHS)
var2 = StringVar(GUI_RHS)
Var_1 = OptionMenu (GUI_RHS, var1 ,*VARchoices )
Var_1.grid( row = 1 , column = 1 )
Op_1 = OptionMenu(GUI_RHS, op1 , *OPchoices )
Op_1.grid( row = 1 , column = 2 )
Var_2 = OptionMenu(GUI_RHS, var2 , *VARchoices)
Var_2.grid( row = 1 , column = 3 )
RHSconfirmation = Button(GUI_RHS , text = "confirm" , command = RHSconfirmationcommand)
RHSconfirmation.grid(row = 1 , column = 4 )
REALVAR1 = Spinbox( GUI_RHS , from_ = -120000 , to = 120000 , wrap = True , state = "disabled" )
REALVAR1.grid( row = 2 , column = 1 )
REALVAR2 = Spinbox( GUI_RHS , from_ = -120000 , to = 120000 , wrap = True , state = "disabled" )  
REALVAR2.grid( row = 2 , column = 3 )
Confirmrealvalues = Button(GUI_RHS , text="confirm values", state = "disabled" , command = Confirmrealvaluescommand)
Confirmrealvalues.grid( row = 2 , column = 4 )











GUI_RHS.mainloop()




Final = Tk()
def Startcommand() :
    Final.destroy()
Start = Button(Final, text ="start", command = Startcommand)
Start.grid(row=1,column=0)

EQUATION = str(LHSEQUATION.input + "=" + VARONE.input + OPONE.input + VARTWO.input + "    for:  "+str(BoundMin.input/120)+"π <θ< "+str(BoundMax.input/120)+"π")
equationdisplay=Label(Final,text=EQUATION)
equationdisplay.grid(row=0,column=0)




Final.mainloop()




















#####################################################
ThetaMin=BoundMin.input##############################
ThetaMax=BoundMax.input                           ###
Screen = turtle.getscreen()                       ###
Screen.title("Initialising")                      ###
Setup1 = turtle.Turtle()                          ###
Setup2 = turtle.Turtle()                          #I#
Setup3 = turtle.Turtle()                          #N#
Setup4 = turtle.Turtle()                          #I#
Setup5 = turtle.Turtle()                          #T#
class Turtle:                                     #I#
    def __init__(self, speed, pensize,):          #A#
        pass                                      #L#
Setup1.speed(10)                                  #I#
Setup2.speed(10)                                  #S#
Setup3.speed(10)                                  #A#
Setup4.speed(10)                                  #T#
Setup5.speed(10)                                  #I#
Setup1.pensize(2)                                 #O#
Setup2.pensize(2)                                 #N#
Setup3.pensize(2)                                 ###
Setup4.pensize(2)                                 ###
Setup5.pensize(2)                                 ###
Setup1.goto( 50 , 0 )                             ###
Setup1.write("0 , 2pi")                           ###
Setup1.goto( 500 , 0 )                            ###
Screen.title("Initialising.")                     ###
Setup1.goto(-50,0)                                ###
Setup1.write("pi")                                ###
Setup1.goto( - 500 , 0 )                          ###
Screen.title("Initialising..")                    ###
Setup1.goto( 0 , 0 )                              ###
Setup1.goto(0,50)                                 ###
Setup1.write(" pi/2")                             ###
Setup1.goto( 0 , 500 )                            ###
Screen.title("Initialising...")                   ###
Setup1.goto(0,-50)                                ###
Setup1.write(" 3pi/2")                            ###
Setup1.goto( 0 , - 500 )                          ###
Screen.title("Initialising....")                  ###
Setup1.goto( 0 , 0 )#################################
#####################################################
bar = {
    "0":"|--------------------|",
    "1":"|/-------------------|",
    "2":"|//------------------|",
    "3":"|///-----------------|",
    "4":"|////----------------|",
    "5":"|/////---------------|",
    "6":"|//////--------------|",
    "7":"|///////-------------|",
    "8":"|////////------------|",
    "9":"|/////////-----------|",
    "10":"|//////////----------|",
    "11":"|///////////---------|",
    "12":"|////////////--------|",
    "13":"|/////////////-------|",
    "14":"|//////////////------|",
    "15":"|///////////////-----|",
    "16":"|////////////////----|",
    "17":"|/////////////////---|",
    "18":"|//////////////////--|",
    "19":"|///////////////////-|",
    "20":"|////////////////////|graphing_complete"
    }

for i in range (101):
    percent = round((((i)/101)*100),1)
    if percent == 100 :
        percentbar = bar["20"]
    elif percent > 95:
        percentbar = bar["19"]
    elif percent > 90:
        percentbar = bar["18"]
    elif percent > 85:
        percentbar = bar["17"]
    elif percent > 80:
        percentbar = bar["16"]
    elif percent > 75:
        percentbar = bar["15"]
    elif percent > 70:
        percentbar = bar["14"]
    elif percent > 65:
        percentbar = bar["13"]
    elif percent > 60:
        percentbar = bar["12"]
    elif percent > 55:
        percentbar = bar["11"]
    elif percent > 50:
        percentbar = bar["10"]
    elif percent > 45:
        percentbar = bar["9"]
    elif percent > 40:
        percentbar = bar["8"]
    elif percent > 35:
        percentbar = bar["7"]
    elif percent > 30:
        percentbar = bar["6"]
    elif percent > 25:
        percentbar = bar["5"]
    elif percent > 20:
        percentbar = bar["4"]
    elif percent > 15:
        percentbar = bar["3"]
    elif percent > 10:
        percentbar = bar["2"]
    elif percent > 5:
        percentbar = bar["1"]
    else:
        percentbar = bar["0"]
    inttitle = str( "Initialising....    " + percentbar)
    Screen.title(inttitle)
    Theta = ( i * 2 * pi ) / 100
    Setup1.goto( 100 * cos( Theta ) , 100 * sin( Theta ) )
    Setup2.goto( 200 * cos( Theta ) , 200 * sin( Theta ) )
    Setup3.goto( 300 * cos( Theta ) , 300 * sin( Theta ) )
    Setup4.goto( 400 * cos( Theta ) , 400 * sin( Theta ) )
    Setup5.goto( 500 * cos( Theta ) , 500 * sin( Theta ) )
Setup1.write( "100" )
Setup2.write( "200" )
Setup3.write( "300" )
Setup4.write( "400" )
Setup5.write( "500" )
Setup1.ht()
Setup2.ht()
Setup3.ht()
Setup4.ht()
Setup5.ht()###################################################
T1 = turtle.Turtle()
T1.speed(10)
T1.pencolor("Red")
T1.pensize(3)
T1.penup()
T1.ht()
# ^expression turtle^ #
Thetastr=str(Theta)
A=int((ThetaMin/(32*pi)))
B=int((ThetaMax/(32*pi)))   
SA=str(A)
SB=str(B)
title=(SA , "π<θ<" , SB , "π")
Screen.title(title)




    

for i in range((ThetaMax - ThetaMin)+1 ):
   # ^setup loop^ #

    
    Theta = pi*((ThetaMin+i)/120)
        # ^theta intevals^ #
    print(Theta)
    print("--------------------", ThetaMin+i )
           # ^step info^ #




    R1 = 10*((Theta)*(cos(3*Theta)))
    strR1 = str("(Theta)*(cos(3*Theta))")
    A=int((ThetaMin/(32*pi)))
    B=int((ThetaMax/(32*pi)))   
    SA=str(A)
    SB=str(B)
    percent = (round((((i)/(ThetaMax-ThetaMin))*100),1))
    if percent == 100 :
        percentbar = str("|////////////////////|graphing_complete")
    elif percent > 95:
        percentbar = str("|///////////////////-|")
    elif percent > 90:
        percentbar = str("|//////////////////--|")
    elif percent > 85:
        percentbar = str("|/////////////////---|")
    elif percent > 80:
        percentbar = str("|////////////////----|")
    elif percent > 75:
        percentbar = str("|///////////////-----|")
    elif percent > 70:
        percentbar = str("|//////////////------|")
    elif percent > 65:
        percentbar = str("|/////////////-------|")
    elif percent > 60:
        percentbar = str("|////////////--------|")
    elif percent > 55:
        percentbar = str("|///////////---------|")
    elif percent > 50:
        percentbar = str("|//////////----------|")
    elif percent > 45:
        percentbar = str("|/////////-----------|")
    elif percent > 40:
        percentbar = str("|////////------------|")
    elif percent > 35:
        percentbar = str("|///////-------------|")
    elif percent > 30:
        percentbar = str("|//////--------------|")
    elif percent > 25:
        percentbar = str("|/////---------------|")
    elif percent > 20:
        percentbar = str("|////----------------|")
    elif percent > 15:
        percentbar = str("|///-----------------|")
    elif percent > 10:
        percentbar = str("|//------------------|")
    elif percent > 5:
        percentbar = str("|/-------------------|")
    else:
        percentbar = str("|--------------------|")
                

    percent = str(percent)
    titlev1=str(SA + "π<θ<" + SB)
    
    titlev2=str("Bounds: " + titlev1 + "π,       Equation: R=" + strR1 + " ,                    " + percent + "%" + percentbar)


    Screen.title(titlev2)





#expression#
    T1.goto( R1 * cos(Theta) , R1 * sin(Theta) )
    T1.pendown()

# ^turtle going to polar coords in cartesian form^ #
