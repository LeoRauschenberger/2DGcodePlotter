import turtle

# user settings
f = 15 # size increase factor
p = 1  # seize of pen tip
# ------------------------------
t=turtle
t.clear() #clear drawing window

#sc = turtle.Screen()
#sc.setup(600, 600)
# screen layout (can mess up aspect ratio if chose too big!)
turtle.setworldcoordinates(-20, -20, 400, 300)

t.ht()
t.pensize(p)

t.goto(0,0) # default start is 0,0


#Draw Gcode
file1 = open("cyrillic/ltr_А.txt", "r")
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
    print("Line{}: {}".format(count, lList))
    #draw
    
    if lList[0] == 'G0':
        if 'X' in lList[1]:
            xcoord = float(lList[1].strip('X'))
            ycoord = float(lList[2].strip('Y'))
            t.up()
            t.goto(xcoord*f,ycoord*f)
        else: pass
    elif lList[0] == 'G1':
        xcoord = float(lList[1].strip('X'))
        ycoord = float(lList[2].strip('Y'))
        t.down()
        t.goto(xcoord*f,ycoord*f)
    elif lList[0] == 'G2':
        # retrieve starting point of arc from previous line:
        pxcoord = float(prevlList[1].strip('X'))
        pycoord = float(prevlList[2].strip('Y'))
        # retrieve end point and radius of arc form current line:
        xcoord = float(lList[1].strip('X'))
        ycoord = float(lList[2].strip('Y'))
        radius = float(lList[3].strip('R'))
        # go to starting point and draw
        t.goto(pxcoord*f,pycoord*f)
        t.down()
        t.setheading(0)
        t.circle(radius*f,360/2)
        #t.circle(100,-30)
    else: pass

file1.close()
