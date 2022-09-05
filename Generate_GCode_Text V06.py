#-*- coding: utf-8 -*-
# ---------------------------------------------------------------------
import re
from hyphen import Hyphenator
# ---------------------------------------------------------------------
# For linebreak, use: ~
#UserText = input("Enter Text: ")
Formatting = 'r'   # c or r (cycrillic or roman) (will be automized)
h = Hyphenator('de_DE')  #language defaults to 'en_US'
#h = Hyphenator('en_US')  #language defaults to 'en_US'
# ---------------------------------------------------------------------
#UserText = 'АБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮФХЦЧШЩЫЬЭЮЯ'
#UserText = 'САЙН УУ. НЯМ ГАРАГ САЙХАН ӨНГӨРҮҮЛЭЭРЭЙ!'
#UserText = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvxyzäöüß0123456789+-!?...'
UserText = 'Die Gefechte um Tulagi und Gavutu-Tanambogo waren eine Reihe von Kämpfen zwischen Einheiten der Kaiserlich Japanischen Marine und des United States Marine Corps. Sie fanden vom 7. bis zum 9. August 1942 im Zuge des Pazifikkriegs statt.'
SaveName= "MyTestText.txt" # where to save it 

# ---------------------------------------------------------------------
# Choose layout option
# 1 for 3d printer text, 2 for displayability on computer, 3 for singular characters (allows adjusting)
option = 2

if option == 1:
    Xltr_init = 0      # tracks x-offset to next letter. Default 0 (can be set to a positive or negative value to displace start or zero letter)
    Yltr = 220    # tracks y-offset.
    sf = 0.5142857142857142        # scale factor: Default 1
    spacing = 4   #spacing between letters (use -1 for roman, 2 for cyrillic)
    linespacing = 3 #space between lines
    Xmin = 40+20    # min. x coord. (this must include the distance between nozzle and the pen holder)
    Xmax = 225-40      # max. x coord. after which a line break will occur (criterion for linebreak: space)
if option == 2:
    Xltr_init = 0      # tracks x-offset to next letter. Default 0 (can be set to a positive or negative value to displace start or zero letter)
    Yltr = 100    # tracks y-offset.
    sf = 0.4      # scale factor: Default 1
    spacing = -1   #spacing between letters (e.g. use -1 for roman, 4 for cyrillic)
    linespacing = 6 #space between lines
    Xmin = -140     # min. x coord. (this must include the distance between nozzle and the pen holder)
    Xmax = 230      # max. x coord. after which a line break will occur (criterion for linebreak: space)
if option == 3:
    Xltr_init = 0      # tracks x-offset to next letter. Default 0 (can be set to a positive or negative value to displace start or zero letter)
    Yltr = 0    # tracks y-offset.
    sf = 18/10.837837837837839      # scale factor: Default 1
    spacing = 4; linespacing = 6; Xmax = 10
    Xmin = -1     # min. x coord. (this must include the distance between nozzle and the pen holder)
    

# if you want an outline:
draw_outline = 'y'
cntr = 0      # counts charcaters
letterheight = 18
# -----------------------------------------------------------------

Xltr = Xltr_init
with open('user_texts/'+SaveName, 'w', encoding="utf-8") as f:
    f.write('(User\'s Text: '+UserText+')\n')
    f.write('G28 X Y Z \n') # Auto Home
    f.write('G0 Z30 F6000 \n')
    f.write('G0 X'+str(Xmax)+' Y20 Z30 F6000 \n')
    f.write('G0 X'+str(Xmax)+' Y20 Z13.2 F6000 \n') #go to locattion to allow user to set pen down
    f.write('M0 \n') # allows user to set pen down
    f.write('G0 Z15 F6000 \n')

    f.write('G0 X'+str(Xmax)+' Y'+str(Yltr)+' Z30 F6000 \n')
    f.write('G1 X'+str(Xmax)+' Y0 Z30 F6000 \n')

    # Split users input into words while preserving spaces:
    # UserWords = re.split(r'(\s+)', UserText)
    UserWords = re.split('(\W)', UserText) #split at nonword-characters (space, etc)
    print('Split Text: ',UserWords)
    wordcounter = 0
    for word in UserWords:
        for ltr in word:
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
                    ltr="space" # replace by a space
                    Xltr=Xmax   # force new line
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
                    # -- round Y (optional): -----------------------------
                    oldY = float(splitstring[2][1:])
                    newY=round((oldY+Yltr)*sf,3)
                    splitstring[2] = 'Y'+ str(newY)

                    # -- position new item at the correct x coordinate: --
                    oldX = float(splitstring[1][1:])
                    # Nesting: oldY is set to 7 to prevent essissive offsets between e.g. T and a
                    if oldX > Xcoord and oldY<7:
                        Xcoord = oldX
                    newX = round((oldX+Xltr+Xmin)*sf,3)
                    splitstring[1] = 'X'+str(newX)

                    # -- Scale the radius: -------------------------------
                    if 'R' in item:
                        oldR = float(splitstring[3][1:])
                        newR = round(oldR*sf,3)
                        splitstring[3] = 'R'+str(newR)

                    # -- concatenate the newitem -------------------------
                    for elem in splitstring:
                        newitem += str(elem) + " "


                else:
                    newitem = item.rstrip('\n')  # if the Gcode doesn't contain coordinates, just copy, but remove line break

                # write each item on a new line
                print(newitem)
                f.write("%s\n" % newitem)
                #f.write(newitem)
            cntr += 1
            Xltr = Xltr+Xcoord+spacing
            
        # Introduce line breaks:
        awgLetterWidth = 12
        XmaxTolerance = 2*awgLetterWidth*sf
        try:
            nextword = UserWords[wordcounter+1]
            LengthNextWord = len(nextword)
            ExtendNextWord = Xltr + LengthNextWord*awgLetterWidth*sf
            
            # Introduce line break if the next word doesn't fit within a tolerance (next word must not be punctuation)
            if ExtendNextWord > Xmax+XmaxTolerance and LengthNextWord > 1:
                # check if next word can be split:

                splitSuccess = 0
                if Xltr + 5*awgLetterWidth*sf < Xmax+XmaxTolerance:
                    try:
                        splitword = h.wrap(nextword, 5) # see: https://github.com/dr-leo/PyHyphen
                        UserWords[wordcounter+1]=splitword[0]
                        UserWords.insert(wordcounter+2, splitword[1])
                        splitSuccess = 1
                    except:
                        pass

                if splitSuccess == 0:
                    Yltr = Yltr-linespacing-letterheight #move down
                    Xltr = Xltr_init # return x carriage e.g. to 0
        except:
            print("Exception thrown (could be last word in Text)")
            pass
        # increase wordcounter
        wordcounter=wordcounter+1
        print("----------------------------")
    f.write('(End)')
    f.write('G0 Z30 F6000 \n')#raise pen
    f.write('G0 X0 Y235 \n')
f.close()
file.close()   
    
