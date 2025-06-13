#!/usr/bin/env python3
import sys
import tkinter as tk
import threading

from tkinter import ttk, Menu, Toplevel, StringVar, OptionMenu, END, HORIZONTAL
import PyShoot
import HitAnalysis
import PyShootHelp
import PyShootMathModel

themeColor='#4D377B'
buttonColor='#2B0042'
minx=300
miny=110
#buttonColor='Indigo'
maxTests=10000
totalTests=0
top = tk.Tk()
top.configure(bg=themeColor)
top.minsize(minx,miny)
#top.geometry("320x320")
top.option_add("*font", "TkFixedFont")
numClicks = 1
showDebugModeNext=True
showHitModeNext=True

# Kick off the PyShoot diagram
def callback():

    accuracy = accuracyEntry.get()
    shots    = shotsEntry.get()    
    heat     = heatEntry.get()
    caliber  = caliberEntry.get()
    
    print("accuracy %s, shots %s, caliber %s"%(accuracy, shots, caliber))
    
    if heat and caliber and validateEntries(accuracy, shots):
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
    accuracyEntry.insert(0, PyShoot.ACCURACY)
    shotsEntry.delete(0, END)
    shotsEntry.insert(0, PyShoot.MIN_SHOTS)
    heatEntry.delete(0, END)
    heatEntry.insert(0, PyShoot.HEAT_LITZ)
    caliberEntry.delete(0,END)
    caliberEntry.insert(0, PyShoot.CALIBER)

# Validate the input fields and reset if they are bunk
def validateEntries(accuracy, shots):
    isValid = accuracy and shots and int(shots) > 2 and float(accuracy) >= 0.01
    if not isValid:
        resetEntries()
    return isValid
    
# Displays the debug menu
def displayDebug():
    # Set up Debug

    global showDebugModeNext
    global showHitModeNext
    showHitModeNext=True
    
    if(showDebugModeNext == True):
        showDebugModeNext=False
        hitFrame.grid_remove()
        
        infoLabel = tk.Label(debugFrame,
                             text="Debug Zone",
                             anchor="w",
                             bg=themeColor,fg='plum1',font=("TkFixedFont 14 bold")).grid(
                                 row=debugStartRow, columnspan=4)


        calcMOAVariable  = StringVar()
        expMOAVariable   = StringVar()
        minMOAVariable   = StringVar()
        maxMOAVariable   = StringVar()
        calcMOAVariable.set("")
        expMOAVariable.set("")
        minMOAVariable.set("")
        maxMOAVariable.set("")
        testSliderRow    = debugStartRow+1
        calcedRow        = testSliderRow+1
        expectedRow      = calcedRow+1
        minRow           = expectedRow+1
        maxRow           = minRow+1
        debugButtonRow   = maxRow+1
        
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
                                    orient=HORIZONTAL, length=minx,
                                    bg=themeColor,fg='white')
        
        totalTestSlider.grid(row=testSliderRow, columnspan=4)
        totalTestSlider.set(1)
        
        
        debugStartButton = tk.Button(debugFrame, text="Debug Start",
                                     command= lambda: debug(
                                         totalTestSlider,
                                         calcMOAVariable,
                                         expMOAVariable,
                                         minMOAVariable,
                                         maxMOAVariable),
                                     bg=buttonColor, fg='white').grid(
                                         row=debugButtonRow, columnspan=4)
        
        debugFrame.grid()
    else:
        showDebugModeNext=True
        debugFrame.grid_remove()
    

# Kick off the debug mode
def debug(totalTestSlider, calcMOAVariable,
          expMOAVariable, minMOAVariable, maxMOAVariable):
    
    accuracy = accuracyEntry.get()
    shots    = shotsEntry.get()
    
    if validateEntries(accuracy, shots):
        totalTests  = totalTestSlider.get()
        totalResult = 0
        
        minResult = sys.maxsize
        maxResult = 0
        
        PyShoot.printProfilerTime("Starting Debug Commands")
        
        import concurrent.futures

        def run_pyshoot():
            return PyShoot.pyshootCalculate(float(accuracy), int(shots))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda _: run_pyshoot(), range(totalTests)))
            totalResult = sum(results)
            minResult = min(results)
            maxResult = max(results)
            
        PyShoot.printProfilerTime("Finishing Debug Commands")
        
        calcMOAVariable.set(format((totalResult / totalTests), '.2f'))
        expMOAVariable.set(accuracy)
        minMOAVariable.set(minResult)
        maxMOAVariable.set(maxResult)
    else:
        resetEntries()

# Kick off the hitratecomparator
def displayHitrate():
    global showDebugModeNext
    global showHitModeNext
    
    showDebugModeNext = True
    
    if(showHitModeNext):
        showHitModeNext = False
        debugFrame.grid_remove()
        debugStartRow  = buttonRow+1
        
        infoLabel = tk.Label(hitFrame, text="Hit Analysis Zone", anchor="w",
                             bg=themeColor,fg='plum1',font=("TkFixedFont 14 bold")).grid(
                                 row=debugStartRow, columnspan=4)

        # This interface should allow you to input the size of the target,
        # your wind reading error, and your velocity error.

        targetOptions = HitAnalysis.getTargetTypes()
        # 5 Input fields
        targetSizeEntry    = tk.Entry(hitFrame)
        caliberMOAEntry    = tk.Entry(hitFrame)
        windErrorEntry     = tk.Entry(hitFrame)
        velocityErrorEntry = tk.Entry(hitFrame)
        targetSizeEntry.insert(0,"2")
        caliberMOAEntry.insert(0,"0")
        windErrorEntry.insert(0,".75")
        velocityErrorEntry.insert(0,".2")

        targetShapeStr = StringVar(hitFrame)
        targetShapeStr.set(HitAnalysis.TARGETSHAPE.name)  # Set default value
        targetShapeMenu = OptionMenu(hitFrame, targetShapeStr, *targetOptions)

        # 6 Description labels, one for each input, one for final display
        targetSizeLabel    = StringVar()
        caliberMOALabel    = StringVar()
        windErrorLabel     = StringVar()
        velocityErrorLabel = StringVar()
        targetTypeRowLabel = StringVar()
        hitrateVariable    = StringVar()

   
        # 7 rows
        targetTypeRow = debugStartRow+1
        targetRow    = targetTypeRow+1
        caliberRow   = targetRow+1
        windEntryRow = caliberRow+1
        velRow       = windEntryRow+1
        hitRateRow   = velRow+1
        goButtonRow = hitRateRow+1

        targetTypeRowLabel  = tk.Label(hitFrame, text="Target Type: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=targetTypeRow, column=0)
        
        targetShapeMenu.grid(sticky='w',row=targetTypeRow, column=1)
        
        targetLabel  = tk.Label(hitFrame, text="Target Height MOA: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=targetRow, column=0)

        targetSizeEntry.grid(
            row=targetRow, column=1,columnspan=entryspan)

        caliberLabel = tk.Label(hitFrame, text="Caliber MOA: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=caliberRow, column=0)

        caliberMOAEntry.grid(
            row=caliberRow, column=1,columnspan=entryspan)
                                
        windLabel  = tk.Label(hitFrame, text="Wind Err MOA: ",
                             anchor="w",bg=themeColor,fg='white').grid(
                                 sticky='w',row=windEntryRow, column=0)
                                
        windErrorEntry.grid(
            row=windEntryRow, column=1,columnspan=entryspan)

        velocityErrorLabel = tk.Label(hitFrame, text="Elevation Err MOA: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=velRow, column=0)

        velocityErrorEntry.grid(
            row=velRow, column=1,columnspan=entryspan)
        
        hitrateLabel  = tk.Label(hitFrame, text="Hitrate: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=hitRateRow, column=0)
                               
        hitrateResLabel = tk.Label(hitFrame, textvariable=hitrateVariable,
                                anchor="w", bg=themeColor,fg='white').grid(
                                    sticky='w',row=hitRateRow, column=1)
                                   

        # 1 additional button
        hitrateLaunchButton = tk.Button(hitFrame, text="Hit Rate",
                                        command= lambda: hitAnalysisGuiFn(
                                         targetSizeEntry,
                                         caliberMOAEntry,
                                         windErrorEntry,
                                         velocityErrorEntry,
                                         hitrateVariable,
                                         targetShapeStr),
                                        bg=buttonColor, fg='white').grid(
                                            row=goButtonRow, column=0, columnspan=3)
        
        hitFrame.grid()
    else:
        showHitModeNext = True
        hitFrame.grid_remove()

def hitAnalysisGuiFn(
    targetSizeEntry,
    caliberMOAEntry,
    windErrorEntry,
    velocityErrorEntry,
    hitrateVariable,
    targetShapeStr):
    
    targetSize  = float(targetSizeEntry.get())
    windErr     = float(windErrorEntry.get())
    velocityErr = float(velocityErrorEntry.get())
    caliber  = float(caliberMOAEntry.get())
    targetShape = getattr(HitAnalysis.TARGETSHAPE, targetShapeStr.get())
       
    accuracy = accuracyEntry.get()
    
    if accuracy and float(accuracy) > 0.01:
        hitRate = HitAnalysis.hitAnalysis(float(accuracy),targetSize,windErr,velocityErr,1,caliber,targetShape)
        hitrateVariable.set("%s%%"%int(hitRate))

def displayUsage():
    popup = Toplevel(top)

    popup.geometry("785x700")
    popup.title("Usage")
    notebook = ttk.Notebook(popup)
    
    tabOver = ttk.Frame(notebook)
    tabMainFunction  = ttk.Frame(notebook)
    tabHitrate = ttk.Frame(notebook)
    tabDebug = ttk.Frame(notebook)

    labelOver = ttk.Label(tabOver, text=PyShootHelp.getOverviewText()).grid(column=0,row=0);
    labelMain = ttk.Label(tabMainFunction, text=PyShootHelp.getMainText()).grid(column=0,row=0);
    labelHit = ttk.Label(tabHitrate, text=PyShootHelp.getHitrateText()).grid(column=0,row=0);
    labelDebug = ttk.Label(tabDebug, text=PyShootHelp.getDebugText()).grid(column=0,row=0);

    
    notebook.add(tabOver, text="Overview")
    notebook.add(tabMainFunction, text="Main Functions")
    notebook.add(tabHitrate, text="Hitrate Analysis")
    notebook.add(tabDebug, text="Debug/High Sample")

    notebook.pack(expand=1, fill="both", padx=(10,10))

def displayAbout():
    popup = Toplevel(top)

    popup.geometry("785x400")
    popup.title("About")
    labelOver = ttk.Label(popup, text=PyShootHelp.getAboutText())
    labelOver.grid(column=0,row=0, padx=(10,10));

def displayMathModelSelection():
    popup = Toplevel(top)

    popup.geometry("160x40")
    popup.title("Math Model Selection")
    options = PyShootMathModel.getMathModelOptions()
    selectedModel = StringVar(popup)
    selectedModel.set(PyShootMathModel.MATH_MODEL.name)  # Set default value

    def setMathModel( selected ):
        PyShootMathModel.setMathModel(PyShootMathModel.MathModel[selected])
        popup.destroy()

    OptionMenu(popup, selectedModel, *options, command=setMathModel).grid(column=0,row=0, padx=(10,10))
   
entryspan = 2

# Set up row layout
accuracyRow   = 0
shotsRow      = accuracyRow + 1
heatRow       = shotsRow + 1
caliberRow    = heatRow + 1
inputRow      = caliberRow
testSampleRow = inputRow + 1
buttonRow     = testSampleRow + 2
secondButtonRow = buttonRow + 1
debugStartRow = secondButtonRow + 1

# Expanded frames
debugFrame  = tk.Frame(top,bg=themeColor)
debugFrame.grid(row=debugStartRow, columnspan=3)

hitFrame    = tk.Frame(top,bg=themeColor)
hitFrame.grid(row=debugStartRow, columnspan=3)

buttonFrame = tk.Frame(top,bg=themeColor)
buttonFrame.grid(row=buttonRow, columnspan=3)

# Trials section
tk.Label(top, text="Number Trials:", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=testSampleRow, column=0)
totalTestSlider = tk.Scale(top, from_=1, to=20, orient=HORIZONTAL, bg=themeColor,fg='white', length=(minx/2 + 10))
totalTestSlider.grid(sticky='w',row=testSampleRow, column=1,columnspan=entryspan)
totalTestSlider.set(1)

# Main section
button        = tk.Button(buttonFrame, text="Pyshoot", command=callback,
                          bg=buttonColor, fg='white').grid(sticky='w',
                                                     row=buttonRow,column=2)
tk.Label(top, text="Precision (MOA):", anchor="w", bg=themeColor,fg='white').grid(sticky='w',row=accuracyRow)
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


# Set up menu
menubar = Menu(top)
functionsMenu = Menu(menubar,tearoff=0)
functionsMenu.add_command(label="HitRate Calculator", command=displayHitrate)
functionsMenu.add_command(label="Debug Analytics", command=displayDebug)

helpMenu = Menu(menubar, tearoff=0)
helpMenu.add_command(label="About", command=displayAbout)
helpMenu.add_command(label="PyShoot Usage Guide", command=displayUsage)

settingsMenu = Menu(menubar, tearoff=0)
settingsMenu.add_command(label="Select Math Model", command=displayMathModelSelection)

menubar.add_cascade(label="Expand Functions", menu=functionsMenu)
menubar.add_cascade(label="Help", menu=helpMenu)
menubar.add_cascade(label="Settings", menu=settingsMenu)

top.config(menu=menubar)
top.iconbitmap('PyShootGui.ico')
top.title("PyShoot")
top.mainloop()
