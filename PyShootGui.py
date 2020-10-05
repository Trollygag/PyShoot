#!/usr/bin/env python3
import tkinter as tk
import threading
from tkinter import *
import PyShoot

themeColor='navy'
maxTests=10000
totalTests=0
top = tk.Tk()
top.configure(bg=themeColor)
top.minsize(100,100)
numClicks = 1
showDebugModeNext=True
showHitModeNext=True


# Kick off the PyShoot diagram
def callback():
    accuracy=accuracyEntry.get()
    shots=shotsEntry.get()
    heat=heatEntry.get()
    caliber=caliberEntry.get()
    if accuracy and shots and heat and caliber:
        for i in range(0, int(totalTestSlider.get())) :
            PyShoot.pyshootlite(float(accuracy),int(shots), float(heat), float(caliber))
        PyShoot.show()                                            

# Displays the debug menu
def displayDebug():
    # Set up Debug

    global showDebugModeNext
    global showHitModeNext
    showHitModeNext=True
    if(showDebugModeNext == True):
        showDebugModeNext=False
        hitFrame.grid_remove()
        debugButtonRow = debugStartRow+1
        infoLabel = tk.Label(debugFrame, text="Debug Zone: Calibrated against 5 shots", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=debugStartRow, columnspan=2)

        calcMOAVariable = StringVar()
        expMOAVariable = StringVar()
        calcMOAVariable.set("")
        expMOAVariable.set("")
        testSliderRow=debugButtonRow+1
        calcedRow=testSliderRow+1
        expectedRow=calcedRow+1
        calcLabel = tk.Label(debugFrame, text="Calc MOA: ", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=calcedRow, column=0)
        calcResLabel = tk.Label(debugFrame, textvariable=calcMOAVariable, anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=calcedRow, column=1)
        expLabel = tk.Label(debugFrame, text="Expect MOA: ", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=expectedRow, column=0)
        expMOALabel = tk.Label(debugFrame, textvariable=expMOAVariable, anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=expectedRow, column=1)
        totalTestSlider = tk.Scale(debugFrame, from_=1, to=maxTests, orient=HORIZONTAL, bg=themeColor,fg='white')
        totalTestSlider.grid(row=testSliderRow, columnspan=2)
        totalTestSlider.set(maxTests)
        debugStartButton = tk.Button(debugFrame, text="Debug Start", command= lambda: debug(totalTestSlider,calcMOAVariable,expMOAVariable), bg='red', fg='white').grid(row=debugButtonRow,columnspan=2)
        debugFrame.grid()
    else:
        showDebugModeNext=True
        debugFrame.grid_remove()
    

# Kick off the debug mode
def debug(totalTestSlider, calcMOAVariable, expMOAVariable):
    accuracy=accuracyEntry.get()
    shots=shotsEntry.get()
    if accuracy and shots:
        totalTests = totalTestSlider.get()
        totalResult = 0
        for i in range(totalTests):
            totalResult += PyShoot.pyshootCalculate(float(accuracy),int(shots))
        calcMOAVariable.set(format((totalResult / totalTests), '.2f'))
        expMOAVariable.set(accuracy)

# Kick off the hitratecomparator
def hitrate():
    global showDebugModeNext
    global showHitModeNext
    showDebugModeNext=True
    if(showHitModeNext):
        showHitModeNext=False
        debugFrame.grid_remove()
        debugStartRow = buttonRow+1
        debugButtonRow = debugStartRow+1
        infoLabel = tk.Label(hitFrame, text="Hitrate Zone:", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=debugStartRow, columnspan=2)
        hitFrame.grid()
    else:
        showHitModeNext=True
        hitFrame.grid_remove()

entryspan=2
# Set up row layout
accuracyRow = 0
shotsRow = accuracyRow + 1
heatRow = shotsRow + 1
caliberRow = heatRow + 1
inputRow = caliberRow
testSampleRow = inputRow + 1
buttonRow = testSampleRow + 1
debugStartRow = buttonRow + 1

# Expanded frames
debugFrame = tk.Frame(top,bg=themeColor)
debugFrame.grid(row=debugStartRow, columnspan=3)
hitFrame = tk.Frame(top,bg=themeColor)
hitFrame.grid(row=debugStartRow, columnspan=3)
buttonFrame = tk.Frame(top,bg=themeColor)
buttonFrame.grid(row=buttonRow, columnspan=3)

# Trials section
tk.Label(top, text="Number Trials:", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=testSampleRow, column=0)
totalTestSlider = tk.Scale(top, from_=1, to=20, orient=HORIZONTAL, bg=themeColor,fg='white')
totalTestSlider.grid(sticky='w',row=testSampleRow, column=1,columnspan=entryspan)
totalTestSlider.set(1)

# Main section
button = tk.Button(buttonFrame, text="Pyshoot", command=callback, bg='black', fg='white').grid(sticky='w',row=buttonRow,column=0)
debugButton = tk.Button(buttonFrame, text="Debug", command=displayDebug, bg='black', fg='white').grid(sticky='w',row=buttonRow,column=1)
hitrateButton = tk.Button(buttonFrame, text="HitRate", command=hitrate, bg='black', fg='white').grid(sticky='w',row=buttonRow,column=2)
tk.Label(top, text="Accuracy (MOA):", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=accuracyRow)
tk.Label(top, text="Shots:", anchor='w', bg=themeColor,fg='white').grid(sticky='w',row=shotsRow)
tk.Label(top, text="Heat (MOA/Shot):", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=heatRow)
tk.Label(top, text="Caliber (in):", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=caliberRow)
accuracyEntry = tk.Entry(top)
shotsEntry = tk.Entry(top)
heatEntry = tk.Entry(top)
caliberEntry = tk.Entry(top)
accuracyEntry.insert(0, PyShoot.ACCURACY);
shotsEntry.insert(0, PyShoot.MIN_SHOTS);
heatEntry.insert(0, PyShoot.HEAT_LITZ);
caliberEntry.insert(0, PyShoot.CALIBER);

accuracyEntry.grid(row=accuracyRow, column=1,columnspan=entryspan)
shotsEntry.grid(row=shotsRow, column=1,columnspan=entryspan)
heatEntry.grid(row=heatRow, column=1,columnspan=entryspan)
caliberEntry.grid(row=caliberRow, column=1,columnspan=entryspan)

top.mainloop()
