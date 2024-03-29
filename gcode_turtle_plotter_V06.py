# GCode Plotter
# Program written by Leo Rauschenberger
# Source: https://github.com/LeoRauschenberger/2DGcodePlotter

import turtle
import math

# user settings
f = 10                     # size increase factor
p = 1.2                   # size of pen tip
debugmode = 'n'           # y/n will display coordinates of G0 (goto) commands in window
drawcolor = "blue"        #(211,211,211) # RGB code or name e.g. "blue" of color you want to draw with

#Draw Gcode: link the file you want to draw here:
# Note: You can genererate a file using "Generate_GCode_Text.py"
file1 = open("cyrillic/ltr_О.txt", "r", encoding='utf-8')
#file1 = open("user_texts/trial2_G3.txt", "r", encoding='utf-8')

# ------------------------------
def centers(x1, y1, x2, y2, r):
    q = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    x3 = (x1 + x2) / 2
    y3 = (y1 + y2) / 2
    xx = (r ** 2 - (q / 2) ** 2) ** 0.5 * (y1 - y2) / q
    yy = (r ** 2 - (q / 2) ** 2) ** 0.5 * (x2 - x1) / q
    return ((x3 + xx, y3 + yy), (x3 - xx, y3 - yy))
# ------------------------------

t=turtle
t.clear() #clear drawing window
# screen layout (can mess up aspect ratio if chosen too big!)
#t.setworldcoordinates(-50, -50, 400, 300)
t.setworldcoordinates(0, 0, 500, 300)
t.title("Python 2D GCode Plotter and Debugger")
t.colormode(255)
t.mode("logo")

#t.ht() #render drawing-arrow invisible
t.pensize(p)

t.goto(0,0) # default start is 0,0
if debugmode == 'y':
    t.up()
    t.color("grey")
    t.write("X0 Y0" , move=True,align='left',font=('Arial',7))
    t.up()
t.color(drawcolor)

# Process from file
Lines = file1.readlines()
count = 0
lList = []
# Strips the newline character
for line in Lines:
    count += 1
    # save previous List before overwriting
    prevlList=lList
    #strip newline character and split at spaces
    lList = line.strip().split(' ')
    print("{}: {}".format(count, lList)) # prints out line number and contents
    #draw
    
    if lList[0] == 'G0':
        if 'X' in lList[1]:
            x = float(lList[1].strip('X'))
            y = float(lList[2].strip('Y'))
            t.up()
            t.goto(x*f,y*f)
            # now write position if desired
            if debugmode == "y":
                t.color("grey")
                t.dot(p*2)
                t.write("X"+str(round(x, 2))+" \nY"+str(round(y, 2)) , move=True,align='right',font=('Arial',8))
                t.color(drawcolor)
                t.up()
                t.goto(x*f,y*f)
        else:
            print("------------------------------------------------------")
            pass
    elif lList[0] == 'G1':
        x = float(lList[1].strip('X'))
        y = float(lList[2].strip('Y'))
        t.down()
        t.goto(x*f,y*f)
    elif lList[0] == 'G2' or lList[0] == 'G3':
        # retrieve starting point of arc from previous line:
        x1 = float(prevlList[1].strip('X'))
        y1 = float(prevlList[2].strip('Y'))
        # retrieve end point and radius of arc form current line:
        x2 = float(lList[1].strip('X'))
        y2 = float(lList[2].strip('Y'))
        r = float(lList[3].strip('R')) # can be negative!
        # calculate straight line distance between points
        dLength = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        # calculate opening angle in degrees
        openingAngle = math.acos(1-0.5*(dLength/r)**2)*180/math.pi
        # https://lydxlx1.github.io/blog/2020/05/16/circle-passing-2-pts-with-fixed-r/
        nl=centers(x1, y1, x2, y2, r)
        xc = nl[0][0]
        yc = nl[0][1]
        if lList[0] == 'G2':
            xc = nl[1][0]
            yc = nl[1][1]
        if debugmode == "y":
            print("circle center: xc=",round(xc,2), "yc=",round(yc,2))
            t.up()
            t.goto(xc*f,yc*f)
            t.color("grey")
            t.dot(p*2)
            t.write("CC" , move=True,align='left',font=('Arial',8))
            t.color(drawcolor)
            t.up()
        try:
            startheading = math.atan((x1-xc)/(y1-yc))*180/math.pi
            print("Start Heading",round(startheading,2))
        except:
            print("exception occurred, y1-yc=0 means division by 0.")
            if lList[0] == 'G3':                   #counterclockwise
                if y1-y2>0: startheading = 180     #point straight down
                elif y1-y2<0: startheading = 0     #point straight up
            if lList[0] == 'G2':                   #clockwise
                if y1-y2>0: startheading = 0       #point straight down
                elif y1-y2<0: startheading = 180   #point straight up
                
        # mode "logo" is being used!
        # with G2 you have to account for the fact that the pen is drawing "backwards"
        # this means that the orientation of the pen must always be 180° offset!
        if lList[0] == 'G2':
            openingAngle = -openingAngle #clockwise, in degres
            if yc-y1<0: startheading = startheading-90
            if yc-y1>0: startheading = startheading+90
        if lList[0] == 'G3':
            if yc-y1<0: startheading = startheading-90
            if yc-y1>0: startheading = startheading+90

        # go to starting point and draw
        #print("Start Heading",round(startheading,2))
        t.goto(x1*f,y1*f)
        t.down()
        #print("preset Hd:",round(t.heading(),2))
        t.setheading(startheading)
        print("adjusted Hd:",round(t.heading(),2))
        t.circle(abs(r)*f,openingAngle)
        print("end Hd:",round(t.heading(),2))
    else:
        pass

file1.close()
