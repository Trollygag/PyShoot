#!/usr/bin/env python3
import tkinter as tk
import threading
from tkinter import *
import PyShoot
import HitAnalysis

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
    
    accuracy = accuracyEntry.get()
    shots    = shotsEntry.get()
    heat     = heatEntry.get()
    caliber  = caliberEntry.get()
    
    if accuracy and shots and heat and caliber and int(shots) > 2 and float(accuracy) >= 0.01:
        for i in range(0, int(totalTestSlider.get())) :
            PyShoot.pyshootlite(
                float(accuracy), int(shots),
                float(heat), float(caliber))
        PyShoot.show()
    else:
        resetEntries()

# Set the entries to defaults
def resetEntries():
    accuracyEntry.delete(0, END)
    accuracyEntry.insert(0, PyShoot.ACCURACY);
    shotsEntry.delete(0, END)
    shotsEntry.insert(0, PyShoot.MIN_SHOTS);
    heatEntry.delete(0, END)
    heatEntry.insert(0, PyShoot.HEAT_LITZ);
    caliberEntry.delete(0,END)
    caliberEntry.insert(0, PyShoot.CALIBER);

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
        infoLabel = tk.Label(debugFrame,
                             text="Debug Zone: Calibrated against 5 shots",
                             anchor="w",
                             bg=themeColor,fg='white').grid(
                                 sticky='w',row=debugStartRow, columnspan=2)

        calcMOAVariable  = StringVar()
        expMOAVariable   = StringVar()
        minMOAVariable  = StringVar()
        maxMOAVariable   = StringVar()
        calcMOAVariable.set("")
        expMOAVariable.set("")
        minMOAVariable.set("")
        maxMOAVariable.set("")
        testSliderRow    = debugButtonRow+1
        calcedRow        = testSliderRow+1
        expectedRow      = calcedRow+1
        minRow      = expectedRow+1
        maxRow      = minRow+1
        
        calcLabel  = tk.Label(debugFrame, text="Calc MOA: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=calcedRow, column=0)
                               
        calcResLabel = tk.Label(debugFrame, textvariable=calcMOAVariable,
                                anchor="w", bg=themeColor,fg='white').grid(
                                    sticky='w',row=calcedRow, column=1)
                                
        expLabel  = tk.Label(debugFrame, text="Expect MOA: ",
                             anchor="w",bg=themeColor,fg='white').grid(
                                 sticky='w',row=expectedRow, column=0)
                                
        expMOALabel = tk.Label(debugFrame, textvariable=expMOAVariable,
                               anchor="w", bg=themeColor,fg='white').grid(
                                   sticky='w',row=expectedRow, column=1)

        minLabel  = tk.Label(debugFrame, text="Min MOA: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=minRow, column=0)
                               
        minResLabel = tk.Label(debugFrame, textvariable=minMOAVariable,
                                anchor="w", bg=themeColor,fg='white').grid(
                                    sticky='w',row=minRow, column=1)
                                
        maxLabel  = tk.Label(debugFrame, text="Max MOA: ",
                             anchor="w",bg=themeColor,fg='white').grid(
                                 sticky='w',row=maxRow, column=0)
                                
        maxMOALabel = tk.Label(debugFrame, textvariable=maxMOAVariable,
                               anchor="w", bg=themeColor,fg='white').grid(
                                   sticky='w',row=maxRow, column=1)
        
        totalTestSlider  = tk.Scale(debugFrame, from_=1, to=maxTests,
                                    orient=HORIZONTAL,
                                    bg=themeColor,fg='white')
        
        totalTestSlider.grid(row=testSliderRow, columnspan=2)
        totalTestSlider.set(maxTests)
        
        debugStartButton = tk.Button(debugFrame, text="Debug Start",
                                     command= lambda: debug(
                                         totalTestSlider,
                                         calcMOAVariable,
                                         expMOAVariable,
                                         minMOAVariable,
                                         maxMOAVariable),
                                     bg='red', fg='white').grid(
                                         row=debugButtonRow,columnspan=2)
        
        debugFrame.grid()
    else:
        showDebugModeNext=True
        debugFrame.grid_remove()
    

# Kick off the debug mode
def debug(totalTestSlider, calcMOAVariable, expMOAVariable, minMOAVariable, maxMOAVariable):
    accuracy = accuracyEntry.get()
    shots    = shotsEntry.get()
    if accuracy and shots and float(accuracy) >= 0.01 and int(shots) > 2:
        totalTests  = totalTestSlider.get()
        totalResult = 0
        minResult = 100000
        maxResult = 0
        for i in range(totalTests):
            result = PyShoot.pyshootCalculate(
                float(accuracy),int(shots))
            totalResult += result
            minResult = min(minResult, result)
            maxResult = max(maxResult, result)
            
        calcMOAVariable.set(format((totalResult / totalTests), '.2f'))
        expMOAVariable.set(accuracy)
        minMOAVariable.set(minResult)
        maxMOAVariable.set(maxResult)
    else:
        resetEntries()

# Kick off the hitratecomparator
def hitrate():
    global showDebugModeNext
    global showHitModeNext
    
    showDebugModeNext = True
    
    if(showHitModeNext):
        showHitModeNext = False
        debugFrame.grid_remove()
        debugStartRow  = buttonRow+1
        debugButtonRow = debugStartRow+1
        infoLabel = tk.Label(hitFrame, text="Hitrate Zone:", anchor="w",
                             bg=themeColor,fg='white').grid(
                                 sticky='w',row=debugStartRow, columnspan=2)
        hitFrame.grid()
        HitAnalysis.hitAnalysis()
    else:
        showHitModeNext = True
        hitFrame.grid_remove()

entryspan = 2
# Set up row layout
accuracyRow   = 0
shotsRow      = accuracyRow + 1
heatRow       = shotsRow + 1
caliberRow    = heatRow + 1
inputRow      = caliberRow
testSampleRow = inputRow + 1
buttonRow     = testSampleRow + 1
debugStartRow = buttonRow + 1

# Expanded frames
debugFrame  = tk.Frame(top,bg=themeColor)
debugFrame.grid(row=debugStartRow, columnspan=3)

hitFrame    = tk.Frame(top,bg=themeColor)
hitFrame.grid(row=debugStartRow, columnspan=3)

buttonFrame = tk.Frame(top,bg=themeColor)
buttonFrame.grid(row=buttonRow, columnspan=3)

# Trials section
tk.Label(top, text="Number Trials:", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=testSampleRow, column=0)
totalTestSlider = tk.Scale(top, from_=1, to=20, orient=HORIZONTAL, bg=themeColor,fg='white')
totalTestSlider.grid(sticky='w',row=testSampleRow, column=1,columnspan=entryspan)
totalTestSlider.set(1)

# Main section
button        = tk.Button(buttonFrame, text="Pyshoot", command=callback, bg='black', fg='white').grid(sticky='w',row=buttonRow,column=0)
debugButton   = tk.Button(buttonFrame, text="Debug", command=displayDebug, bg='black', fg='white').grid(sticky='w',row=buttonRow,column=1)
hitrateButton = tk.Button(buttonFrame, text="HitRate", command=hitrate, bg='black', fg='white').grid(sticky='w',row=buttonRow,column=2)

tk.Label(top, text="Accuracy (MOA):", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=accuracyRow)
tk.Label(top, text="Shots:", anchor='w', bg=themeColor,fg='white').grid(sticky='w',row=shotsRow)
tk.Label(top, text="Heat (MOA/Shot):", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=heatRow)
tk.Label(top, text="Caliber (in):", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=caliberRow)

accuracyEntry = tk.Entry(top)
shotsEntry    = tk.Entry(top)
heatEntry     = tk.Entry(top)
caliberEntry  = tk.Entry(top)

resetEntries()

accuracyEntry.grid(row=accuracyRow, column=1,columnspan=entryspan)
shotsEntry.grid(row=shotsRow, column=1,columnspan=entryspan)
heatEntry.grid(row=heatRow, column=1,columnspan=entryspan)
caliberEntry.grid(row=caliberRow, column=1,columnspan=entryspan)

top.iconbitmap('PyShootGui.ico')
top.title("PyShoot")
top.mainloop()
