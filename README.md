# 2DGcodePlotter
Plots Gcode using Python (2D only)

The option to use arcs (G2 and G3 commands) is now working correctly.

I added a few Cycrillic and Roman letters. You can however use any Gcode of your own.

Edits you can make are:

f = 10                    # size increase factor 

p = 3                     # size of pen tip

debugmode = 'y'           # y/n will display coordinates of G0 (goto) commands in window

drawcolor = (211,211,211) # RGB code or name e.g. "blue" of color you want to draw with

The " Generate_GCode_Text V....py " now produces code that can actually be used on the 3D printer. However, the M0 (=stop) command in the beginning may cause issues and you may have to replace or remove it.

