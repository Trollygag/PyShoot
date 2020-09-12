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

DEBUG_MODE=False


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
    debugStartRow = buttonRow+1
    debugButtonRow = debugStartRow+1
    infoLabel = tk.Label(top, text="Debug Zone: Calibrated against 5 shots", anchor="w", bg=themeColor,fg='white').grid(row=debugStartRow, columnspan=2)

    calcMOAVariable = StringVar()
    expMOAVariable = StringVar()
    calcMOAVariable.set("")
    expMOAVariable.set("")
    testSliderRow=debugButtonRow+1
    calcedRow=testSliderRow+1
    expectedRow=calcedRow+1
    calcLabel = tk.Label(top, text="Calc MOA: ", anchor="w", bg=themeColor,fg='white').grid(row=calcedRow, column=0)
    calcResLabel = tk.Label(top, textvariable=calcMOAVariable, anchor="w", bg=themeColor,fg='white').grid(row=calcedRow, column=1)
    expLabel = tk.Label(top, text="Expect MOA: ", anchor="w", bg=themeColor,fg='white').grid(row=expectedRow, column=0)
    expMOALabel = tk.Label(top, textvariable=expMOAVariable, anchor="w", bg=themeColor,fg='white').grid(row=expectedRow, column=1)
    totalTestSlider = tk.Scale(top, from_=1, to=maxTests, orient=HORIZONTAL, bg=themeColor,fg='white')
    totalTestSlider.grid(row=testSliderRow, columnspan=2)
    totalTestSlider.set(maxTests)
    debugStartButton = tk.Button(top, text="Debug Start", command= lambda: debug(totalTestSlider,calcMOAVariable,expMOAVariable), bg='red', fg='white').grid(row=debugButtonRow,columnspan=2)

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
        
# Set up GUI

# Set up row layout
accuracyRow = 0
shotsRow = accuracyRow + 1
heatRow = shotsRow + 1
caliberRow = heatRow + 1
inputRow = caliberRow
testSampleRow = inputRow + 1
buttonRow = testSampleRow + 1

# Trials section
tk.Label(top, text="Number Trials:", anchor="w", bg=themeColor,fg='white').grid(row=testSampleRow, column=0)
totalTestSlider = tk.Scale(top, from_=1, to=20, orient=HORIZONTAL, bg=themeColor,fg='white')
totalTestSlider.grid(row=testSampleRow, column=1)
totalTestSlider.set(1)

# Main section
button = tk.Button(top, text="Pyshoot", command=callback, bg='black', fg='white').grid(row=buttonRow,column=0)
debugButton = tk.Button(top, text="Debug", command=displayDebug, bg='black', fg='white').grid(row=buttonRow,column=1)
tk.Label(top, text="Accuracy (MOA):", anchor="w", bg=themeColor,fg='white').grid(row=accuracyRow)
tk.Label(top, text="Shots:", anchor="w", bg=themeColor,fg='white').grid(row=shotsRow)
tk.Label(top, text="Heat Affect (MOA/Shot):", anchor="w", bg=themeColor,fg='white').grid(row=heatRow)
tk.Label(top, text="Caliber (in):", anchor="w", bg=themeColor,fg='white').grid(row=caliberRow)
accuracyEntry = tk.Entry(top)
shotsEntry = tk.Entry(top)
heatEntry = tk.Entry(top)
caliberEntry = tk.Entry(top)
accuracyEntry.insert(0, PyShoot.ACCURACY);
shotsEntry.insert(0, PyShoot.MIN_SHOTS);
heatEntry.insert(0, PyShoot.HEAT_LITZ);
caliberEntry.insert(0, PyShoot.CALIBER);

accuracyEntry.grid(row=accuracyRow, column=1)
shotsEntry.grid(row=shotsRow, column=1)
heatEntry.grid(row=heatRow, column=1)
caliberEntry.grid(row=caliberRow, column=1)
top.mainloop()
