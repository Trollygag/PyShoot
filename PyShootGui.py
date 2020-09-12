#!/usr/bin/env python3
import tkinter as tk
from tkinter import *
import PyShoot
top = tk.Tk()


def callback():
    accuracy=e1.get()
    shots=e2.get()
    if accuracy and shots:
        PyShoot.pyshootlite(float(accuracy),int(shots))

def debug():
    accuracy=e1.get()
    shots=e2.get()
    if accuracy and shots:
        totalTests = 10000
        totalResult = 0
        for i in range(totalTests):
            totalResult += PyShoot.pyshootCalculate(float(accuracy),int(shots))
        calcMOAVariable.set(format((totalResult / totalTests), '.2f'))
        expMOAVariable.set(accuracy)


button = tk.Button(top, text="Pyshoot", command=callback).grid(row=3,column=0)
debugButton = tk.Button(top, text="Debug", command=debug).grid(row=3,column=1)
calcMOAVariable = StringVar()
calcMOAVariable.set("")
expMOAVariable = StringVar()
expMOAVariable.set("")

tk.Label(top, text="Accuracy (MOA):", anchor="w").grid(row=0)
tk.Label(top, text="Shots:", anchor="w").grid(row=1)
calcLabel = tk.Label(top, text="Calc MOA: ", anchor="w").grid(row=4, column=0)
calcResLabel = tk.Label(top, textvariable=calcMOAVariable, anchor="w").grid(row=4, column=1)
expLabel = tk.Label(top, text="Expect MOA: ", anchor="w").grid(row=5, column=0)
expMOALabel = tk.Label(top, textvariable=expMOAVariable, anchor="w").grid(row=5, column=1)

e1 = tk.Entry(top)
e2 = tk.Entry(top)
e1.insert(0, "1");
e2.insert(0, "3");

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

top.mainloop()
