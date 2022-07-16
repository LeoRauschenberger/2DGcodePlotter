#-*- coding: utf-8 -*-

#UserText = input("Enter Text in Cyrillic: ")
UserText = 'АД БЖ'

cntr = 0      # counts charcaters
Xltr = 0      # tracks where the last letter ends

spacing = 2   #spacing between letters

with open('cyrillic/UserText.txt', 'w', encoding="utf-8") as f:
    f.write('(User\'s Text: '+UserText+')\n')
    for ltr in UserText:
        #print(ltr, end=' ')
        #print("\n")
        file = open("cyrillic/ltr_"+ltr+".txt", "r", encoding="utf-8")
        Lines = file.readlines()
        Xcoord = 0    # Xcoord tracks the letter's width
        for item in Lines:
            newitem = str()
            if 'X' in item:
                splitstring = item.split()
                oldX = float(splitstring[1][1:])
                if oldX > Xcoord:
                    Xcoord = oldX
                newX = round(oldX+Xltr,2)
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
    f.write('(End)')

f.close()
    
    
