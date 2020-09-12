#!/usr/bin/env python3
import tkinter as tk
from tkinter import *
import PyShoot

themeColor='navy'
top = tk.Tk()
top.configure(bg=themeColor)
top.minsize(100,100)

DEBUG_MODE=True


# Kick off the PyShoot diagram
def callback():
    accuracy=accuracyEntry.get()
    shots=shotsEntry.get()
    if accuracy and shots:
        PyShoot.pyshootlite(float(accuracy),int(shots))

# Kick off the debug mode
def debug():
    accuracy=accuracyEntry.get()
    shots=shotsEntry.get()
    if accuracy and shots:
        totalTests = 10000
        totalResult = 0
        for i in range(totalTests):
            totalResult += PyShoot.pyshootCalculate(float(accuracy),int(shots))
        calcMOAVariable.set(format((totalResult / totalTests), '.2f'))
        expMOAVariable.set(accuracy)

# Set up GUI
button = tk.Button(top, text="Pyshoot", command=callback, bg='black', fg='white').grid(row=3,column=0)
tk.Label(top, text="Accuracy (MOA):", anchor="w", bg=themeColor,fg='white').grid(row=0)
tk.Label(top, text="Shots:", anchor="w", bg=themeColor,fg='white').grid(row=1)
accuracyEntry = tk.Entry(top)
shotsEntry = tk.Entry(top)
accuracyEntry.insert(0, PyShoot.ACCURACY);
shotsEntry.insert(0, PyShoot.MIN_SHOTS);

accuracyEntry.grid(row=0, column=1)
shotsEntry.grid(row=1, column=1)

if DEBUG_MODE:
    # Set up Debug
    debugButton = tk.Button(top, text="Debug", command=debug, bg='red', fg='white').grid(row=3,column=1)
    calcMOAVariable = StringVar()
    expMOAVariable = StringVar()
    calcMOAVariable.set("")
    expMOAVariable.set("")
    calcLabel = tk.Label(top, text="Calc MOA: ", anchor="w", bg=themeColor,fg='white').grid(row=4, column=0)
    calcResLabel = tk.Label(top, textvariable=calcMOAVariable, anchor="w", bg=themeColor,fg='white').grid(row=4, column=1)
    expLabel = tk.Label(top, text="Expect MOA: ", anchor="w", bg=themeColor,fg='white').grid(row=5, column=0)
    expMOALabel = tk.Label(top, textvariable=expMOAVariable, anchor="w", bg=themeColor,fg='white').grid(row=5, column=1)


top.mainloop()
