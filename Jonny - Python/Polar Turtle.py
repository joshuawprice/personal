from math import pi, sin, cos
from tkinter import StringVar, Tk, DISABLED, N, E, S, W
from tkinter import ttk
import turtle

# Was originally 270 lines

root = Tk()  # Tkinter loop#
root.title("Polar Coordinates")


def Mindone():  # Button effects##
    Minbut["state"] = DISABLED
    Min.state(["disabled"])
    if Max.instate(["disabled"]):
        root.destroy()
def Maxdone():
    Maxbut[ "state" ] = DISABLED
    Max.state([DISABLED])
    if Min.instate(["disabled"]):
        root.destroy()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Widget Setup
Bounds = ttk.Label(mainframe, text="θ = πX/120 , where X is an int, -120000<X<120000")
Bounds.grid(row=0, column=0)
Mintxt = ttk.Label(mainframe, text="X                >")
Maxtxt = ttk.Label(mainframe, text="X                <")
Mintxt.grid(row=1, column=0)
Maxtxt.grid(row=2, column=0)
ThetaMin = StringVar()
Min = ttk.Spinbox(mainframe, from_=-120000, to=120000, wrap=True, textvariable=ThetaMin)
# Min.delete(0,"end")
Min.insert(0,0)
ThetaMax = StringVar()
Max = ttk.Spinbox(mainframe, from_=-120000, to=120000, wrap=True, textvariable=ThetaMax)
# Max.delete(0,"end")
Max.insert(0,240)
Min.grid(row=1, column=1)
Max.grid(row=2, column=1)
Minbut = ttk.Button(mainframe, text="Done", command=Mindone)
Maxbut = ttk.Button(mainframe, text="Done", command=Maxdone)
Minbut.grid(row=1, column=2)
Maxbut.grid(row=2, column=2)

# Tkinter loop
root.mainloop()
ThetaMin = int(ThetaMin.get())
ThetaMax = int(ThetaMax.get())
print("X >", ThetaMin)
print("X <",ThetaMax)


# Start turtles
screen = turtle.Screen()
screen.title("Initialising")
turtles = [turtle.Turtle() for _ in range(5)]
for t in turtles:
    t.speed(10)
    t.pensize(2)

old_tracer = screen.tracer()
screen.tracer(0)
turtles[0].goto(50, 0)
turtles[0].write("0 , 2π")
turtles[0].goto(500, 0)
screen.title("Initialising.")
turtles[0].goto(-50, 0)
turtles[0].write("π")
turtles[0].goto(- 500, 0)
screen.title("Initialising..")
turtles[0].goto(0, 0)
turtles[0].goto(0, 50)
turtles[0].write(" π/2")
turtles[0].goto(0, 500)
screen.title("Initialising...")
turtles[0].goto(0, -50)
turtles[0].write(" 3π/2")
turtles[0].goto(0, - 500)
screen.title("Initialising....")
turtles[0].goto(0, 0)
screen.tracer(old_tracer)

for i in range(101):
    percent_bar = "|" + "".join(["/" for _ in range(round(i / 5.0))]) + "".join(["-" for _ in range(round((100-i) / 5.0))]) + "|"
    screen.title("Initialising.... " + percent_bar)
    Theta = (i * 2 * pi) / 100
    for j, t in enumerate(turtles):
        t.goto((j) * 100 * cos(Theta), (j) * 100 * sin(Theta))


for j, t in enumerate(turtles):
    t.write(f"{j * 100}")
    t.ht()

del turtles


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
A=str(A)
B=str(B)
title = (A, "π<θ<", B, "π")
screen.title(title)



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
    A=str(A)
    A=str(B)
    percent = (round((((i)/(ThetaMax-ThetaMin))*100),1))

    percent_bar = "|" + "".join(["/" for _ in range(round(percent / 5))]) + "".join(["-" for _ in range(round((100-percent) / 5))]) + "|"

    percent = str(percent)
    titlev1=str(A + "π<θ<" + B)

    titlev2=str("Bounds: " + titlev1 + "π,       Equation: R=" + strR1 + " ,                    " + percent + "%" + percent_bar)

    screen.title(titlev2)

#expression#
    T1.goto( R1 * cos(Theta) , R1 * sin(Theta) )
    T1.pendown()

# ^turtle going to polar coords in cartesian form^ #

while True: input()