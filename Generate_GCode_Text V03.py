#-*- coding: utf-8 -*-


# ---------------------------------------------------------------------
# For linebreak, use: ~
#UserText = input("Enter Text: ")
Formatting = 'r'   # c or r
#UserText = 'АД БЖ'
#UserText = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvxyzäöüß0123456789+-!?...'


# ---------------------------------------------------------------------
cntr = 0      # counts charcaters
Xltr_init = 0      # tracks x-offset to next letter. Default 0 (can be set to a positive or negative value to displace start or zero letter)
Yltr = 220    # tracks y-offset.
sf = 0.7        # scale factor: Default 1
spacing = -1   #spacing between letters (use -1 for roman)
Xmin = 40+20    # min. x coord. (this must include the distance between nozzle and the pen holder)
Xmax = 225-40      # max. x coord. after which a line break will occur (criterion for linebreak: space)
# if you want an outline of the above:
draw_outline = 'y'

# -----------------------------------------------------------------

Xltr = Xltr_init
with open('user_texts/Text_trial.gcode', 'w', encoding="utf-8") as f:
    f.write('(User\'s Text: '+UserText+')\n')
    f.write('G28 X Y Z \n') # Auto Home
    f.write('G0 Z30 F6000 \n')
    f.write('G0 X'+str(Xmax)+' Y20 Z30 F6000 \n')
    f.write('G0 X'+str(Xmax)+' Y20 Z13.2 F6000 \n') #go to locattion to allow user to set pen down
    f.write('M0 \n') # allows user to set pen down
    f.write('G0 Z15 F6000 \n')
    for ltr in UserText:
        #print(ltr, end=' ')
        #print("\n")
        # check if it is a alphabethical and lower case letter
        if ltr.isalpha():
            if ltr.islower():
                add_path = "lower/ltr_"
            else:
                add_path = "ltr_"
        else:
            add_path = "chars/char_"
            # check if letter is a space
            if ltr.isspace():ltr='space'
            elif ltr=="!":ltr='!'
            elif ltr=="?":ltr='question'
            elif ltr=="+":ltr='plus'
            elif ltr=="-":ltr='minus'
            elif ltr==".":ltr='dot'
            elif ltr==",":ltr='comma'
            elif ltr==":":ltr='doubledot'
            elif ltr==")":ltr=')'
            elif ltr=="(":ltr='('
            elif ltr=="/":ltr="slash"
            elif ltr=="~":
                ltr="space"
                Xltr=Xmax
        if Formatting == 'c':
            file = open("cyrillic/"+add_path+ltr+".txt", "r", encoding="utf-8")
        elif Formatting == 'r':
            file = open("roman/"+add_path+ltr+".txt", "r", encoding="utf-8")
        Lines = file.readlines()
        Xcoord = 0    # Xcoord tracks the letter's width
        for item in Lines:
            newitem = str()
            splitstring = item.split()
            if 'X' in item:
                splitstring = item.split()
                # round Y (optional):
                oldY = float(splitstring[2][1:])
                newY=round((oldY+Yltr)*sf,3)
                splitstring[2] = 'Y'+ str(newY)
                # position new item at the correct x coordinate:
                oldX = float(splitstring[1][1:])
                # oldY is set to 7 to prevent essissive offsets between e.g. T and a (nesting)
                if oldX > Xcoord and oldY < 7:
                    Xcoord = oldX
                newX = round((oldX+Xltr+Xmin)*sf,3)
                splitstring[1] = 'X'+str(newX)
                #print(splitstring)
                for elem in splitstring:
                    newitem += str(elem) + " "
            else:
                newitem = item
            # write each item on a new line
            print(newitem)
            f.write("%s\n" % newitem)
            #f.write(newitem)
        cntr += 1
        Xltr = Xltr+Xcoord+spacing
        # intruduce line breaks, but only on space-characters.
        if Xltr > Xmax:
            if ltr=="space" or ltr=='minus':
                Yltr = Yltr-20
                Xltr = Xltr_init
        print("----------------------------")
    f.write('(End)')
    f.write('G0 Z30 F6000 \n')#raise pen
    f.write('G0 X0 Y235 \n')
f.close()
file.close()   
    
