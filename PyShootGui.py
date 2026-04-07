#!/usr/bin/env python3
"""PyShoot GUI - Tkinter-based graphical user interface for ballistic simulation.

Provides the main interactive interface for generating shot groups, analyzing hit
probability, and debugging ballistic models.
"""
import sys
import tkinter as tk
import threading
import concurrent.futures

from tkinter import ttk, Menu, Toplevel, StringVar, OptionMenu, END, HORIZONTAL
import PyShoot
import HitAnalysis
import PyShootHelp
import PyShootMathModel
from enum import Enum

# UI Theme Configuration
themeColor = '#4D377B'  # Main purple theme
buttonColor = '#2B0042'  # Dark purple buttons
minx = 300  # Minimum window width
miny = 110  # Minimum window height
maxTests = 10000  # Maximum batch analysis samples
totalTests=0
top = tk.Tk()
top.configure(bg=themeColor)
top.minsize(minx,miny)
#top.geometry("320x320")
top.option_add("*font", "TkFixedFont")
numClicks = 1
showDebugModeNext=True
showHitModeNext=True
showAngularHitAnalysis=False

def setupAngularHitAnalysis():
    """Toggle between simple and advanced hit analysis mode."""
    global showAngularHitAnalysis
    showAngularHitAnalysis = not showAngularHitAnalysis


def callback():
    """Generate and display simulated shot groups.
    
    Validates input parameters and generates the specified number of shot groups
    using the provided ballistic parameters.
    """
    accuracy = accuracyEntry.get()
    shots = shotsEntry.get()
    heat = heatEntry.get()
    caliber = caliberEntry.get()

    print("Shot group parameters - accuracy: %s MOA, shots: %s, caliber: %s in, heat: %s" %
          (accuracy, shots, caliber, heat))

    if heat and caliber and validateEntries(accuracy, shots):
        for i in range(0, int(totalTestSlider.get())):
            PyShoot.pyshootlite(
                float(accuracy), int(shots),
                float(heat), float(caliber))
        PyShoot.show()
    else:
        resetEntries()

def resetEntries():
    """Reset all input fields to their default values."""
    accuracyEntry.delete(0, END)
    accuracyEntry.insert(0, PyShoot.ACCURACY)
    shotsEntry.delete(0, END)
    shotsEntry.insert(0, PyShoot.MIN_SHOTS)
    heatEntry.delete(0, END)
    heatEntry.insert(0, PyShoot.HEAT_LITZ)
    caliberEntry.delete(0, END)
    caliberEntry.insert(0, PyShoot.CALIBER)

def validateEntries(accuracy, shots):
    """Validate input field values.
    
    Args:
        accuracy: Precision value in MOA.
        shots: Number of shots in group.
        
    Returns:
        True if valid, False otherwise. Resets entries if invalid.
    """
    is_valid = accuracy and shots and int(shots) > 2 and float(accuracy) >= 0.01
    if not is_valid:
        resetEntries()
    return is_valid
def displayDebug():
    """Display the debug/batch analysis interface.
    
    Allows users to run high-sample analysis to validate ballistic models
    and find statistical extremes.
    """
    # Set up Debug

    global showDebugModeNext
    global showHitModeNext
    showHitModeNext=True
    
    if showDebugModeNext:
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
        meanRadiusVariable = StringVar()
        calcMOAVariable.set("")
        expMOAVariable.set("")
        minMOAVariable.set("")
        maxMOAVariable.set("")
        meanRadiusVariable.set("")
        testSliderRow    = debugStartRow+1
        calcedRow        = testSliderRow+1
        expectedRow      = calcedRow+1
        minRow           = expectedRow+1
        maxRow           = minRow+1
        meanRadiusRow    = maxRow+1
        debugButtonRow   = meanRadiusRow+1
        
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
        
        meanRadiusLabel  = tk.Label(debugFrame, text="Mean Radius: ",
                             anchor="w",bg=themeColor,fg='white').grid(
                                 sticky='w',row=meanRadiusRow, column=0)
                                
        meanRadiusResLabel = tk.Label(debugFrame, textvariable=meanRadiusVariable,
                               anchor="w", bg=themeColor,fg='white').grid(
                                   sticky='w',row=meanRadiusRow, column=1)
        
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
                                         maxMOAVariable,
                                         meanRadiusVariable),
                                     bg=buttonColor, fg='white').grid(
                                         row=debugButtonRow, columnspan=4)
        
        debugFrame.grid()
    else:
        showDebugModeNext=True
        debugFrame.grid_remove()
    

def debug(total_test_slider, calc_moa_variable,
          exp_moa_variable, min_moa_variable, max_moa_variable, mean_radius_variable):
    """Run debug/batch analysis on specified number of samples.
    
    Args:
        total_test_slider: Slider widget for sample count.
        calc_moa_variable: Display variable for calculated MOA.
        exp_moa_variable: Display variable for expected MOA.
        min_moa_variable: Display variable for minimum MOA.
        max_moa_variable: Display variable for maximum MOA.
        mean_radius_variable: Display variable for mean radius.
    """
    
    accuracy = accuracyEntry.get()
    shots    = shotsEntry.get()
    
    if validateEntries(accuracy, shots):
        totalTests  = total_test_slider.get()
        totalResult = 0
        
        minResult = sys.maxsize
        maxResult = 0
        
        PyShoot.printProfilerTime("Starting Debug Commands")
        
        def run_pyshoot():
            return PyShoot.pyshootCalculate(float(accuracy), int(shots))


        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda _: run_pyshoot(), range(totalTests)))
            totalResult = sum(result.es for result in results)
            minResult = min(result.es for result in results)
            maxResult = max(result.es for result in results)
            mean_radius = sum(result.mr for result in results) / len(results) if results else 0
            
        PyShoot.printProfilerTime("Finishing Debug Commands")
        
        if totalTests > 0:
            calc_moa_variable.set(format((totalResult / totalTests), '.2f'))
        else:
            calc_moa_variable.set("0.00")
        exp_moa_variable.set(accuracy)
        min_moa_variable.set(format(minResult, '.2f'))
        max_moa_variable.set(format(maxResult, '.2f'))
        mean_radius_variable.set(format(mean_radius, '.2f'))
    else:
        resetEntries()

def displayAdvHitrate():
    """Display the advanced hit rate analysis interface.
    
    Provides detailed hit probability calculation with wind handling,
    elevation error, and shooter skill level modeling.
    """
    global showDebugModeNext
    global showHitModeNext
    
    showDebugModeNext = True
    
    if showHitModeNext:
        showHitModeNext = False
        debugFrame.grid_remove()
        debugStartRow  = buttonRow+1
        
        infoLabel = tk.Label(hitFrame, text="Advanced Hit Analysis Zone", anchor="w",
                             bg=themeColor,fg='plum1',font=("TkFixedFont 14 bold")).grid(
                                 row=debugStartRow, columnspan=4)

        # This interface should allow you to input the size of the target,
        # your wind reading error, and your velocity error.

        targetOptions = HitAnalysis.getTargetTypes()
        targetShapeStr = StringVar(hitFrame)
        targetShapeStr.set(HitAnalysis.TARGETSHAPE.name)  # Set default value

        # 5 Input fields
        targetSizeEntry    = tk.Entry(hitFrame)
        caliberMOAEntry    = tk.Entry(hitFrame)
        windErrorEntry     = tk.Entry(hitFrame)
        velocityErrorEntry = tk.Entry(hitFrame)
        targetSizeEntry.insert(0,"2")
        caliberMOAEntry.insert(0,"0")
        windErrorEntry.insert(0,".75")
        velocityErrorEntry.insert(0,".2")

        # Variables for output display
        hitrateVariable    = StringVar()

   
        # 7 rows
        targetTypeRow = debugStartRow+1
        targetRow    = targetTypeRow+1
        caliberRow   = targetRow+1
        windEntryRow = caliberRow+1
        velRow       = windEntryRow+1
        hitRateRow   = velRow+1
        goButtonRow = hitRateRow+1

        targetLabelString = "Target Height (MOA): "

        targetTypeRowLabel  = tk.Label(hitFrame, text="Target Type: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=targetTypeRow, column=0)
        

        
        targetLabel  = tk.Label(hitFrame, text=targetLabelString,
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=targetRow, column=0)

        targetSizeEntry.grid(
            row=targetRow, column=1,columnspan=entryspan)

        def updateTargetSize(selected):
            # Update the targetSizeEntry default value based on the selected target type
            target_type = getattr(HitAnalysis.TARGETSHAPE, selected)
            default_size = HitAnalysis.getDefaultTargetSize(target_type)
            targetSizeEntry.delete(0, END)
            targetSizeEntry.insert(0, str(default_size))

        targetShapeMenu = OptionMenu(hitFrame, targetShapeStr, *targetOptions, command=updateTargetSize)
        targetShapeMenu.grid(sticky='w',row=targetTypeRow, column=1)

        caliberLabel = tk.Label(hitFrame, text="Caliber (MOA): ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=caliberRow, column=0)

        caliberMOAEntry.grid(
            row=caliberRow, column=1,columnspan=entryspan)
                                
        windLabel  = tk.Label(hitFrame, text="Wind Err (MOA): ",
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
                                         float(targetSizeEntry.get()),
                                         float(caliberMOAEntry.get()),
                                         float(windErrorEntry.get()),
                                         float(velocityErrorEntry.get()),
                                         hitrateVariable,
                                         getattr(HitAnalysis.TARGETSHAPE, targetShapeStr.get()),
                                         float(accuracyEntry.get())),
                                        bg=buttonColor, fg='white').grid(
                                            row=goButtonRow, column=0, columnspan=3)
        
        hitFrame.grid()
    else:
        showHitModeNext = True
        hitFrame.grid_remove()

def displaySimpleHitrate():
    """Display the simple hit rate calculator interface.
    
    Provides basic hit probability calculation with shooter type selection
    and real-world wind modeling.
    """
    global showDebugModeNext
    global showHitModeNext
    
    showDebugModeNext = True
    
    if showHitModeNext:
        velocityErrorScale = .1
        showHitModeNext = False
        debugFrame.grid_remove()
        debugStartRow  = buttonRow+1
        
        infoLabel = tk.Label(hitFrame, text="Simple Hit Analysis Zone", anchor="w",
                             bg=themeColor,fg='plum1',font=("TkFixedFont 14 bold")).grid(
                                 row=debugStartRow, columnspan=4)

        # This interface should allow you to input the size of the target,
        # your wind reading error, and your velocity error.

        targetOptions = HitAnalysis.getTargetTypes()
        targetShapeStr = StringVar(hitFrame)
        targetShapeStr.set(HitAnalysis.TARGETSHAPE.name)  # Set default value

        # 5 Input fields
        targetSizeEntry    = tk.Entry(hitFrame)
        caliberMOAEntry    = tk.Entry(hitFrame)
        windErrorEntry     = tk.Entry(hitFrame)
        velocityErrorEntry = tk.Entry(hitFrame)
        targetSizeEntry.insert(0,"12")
        caliberMOAEntry.insert(0,"0.308")
        windErrorEntry.insert(0,"4")
        velocityErrorEntry.insert(0,"2")
        distanceEntry = tk.Entry(hitFrame)
        distanceEntry.insert(0,"100")

        # Variables for output display
        hitrateVariable    = StringVar()

   
        # 7 rows
        targetTypeRow = debugStartRow+1
        targetRow    = targetTypeRow+1
        caliberRow   = targetRow+1
        windEntryRow = caliberRow+1
        realWindRow = windEntryRow+1
        velRow       = realWindRow+1

        distanceRow = velRow+1
        shooterTypeRow = distanceRow+1
        hitRateRow   = shooterTypeRow+1
        goButtonRow = hitRateRow+1

        targetLabelString = "Target Height (Inches): "

        targetTypeRowLabel  = tk.Label(hitFrame, text="Target Type: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=targetTypeRow, column=0)
        

        
        targetLabel  = tk.Label(hitFrame, text=targetLabelString,
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=targetRow, column=0)

        targetSizeEntry.grid(
            row=targetRow, column=1,columnspan=entryspan)

        def updateTargetSize(selected):
            # Update the targetSizeEntry default value based on the selected target type
            target_type = getattr(HitAnalysis.TARGETSHAPE, selected)
            default_size = HitAnalysis.getDefaultTargetSize(target_type)
            targetSizeEntry.delete(0, END)
            targetSizeEntry.insert(0, str(default_size))

        targetShapeMenu = OptionMenu(hitFrame, targetShapeStr, *targetOptions, command=updateTargetSize)
        targetShapeMenu.grid(sticky='w',row=targetTypeRow, column=1)

        caliberLabel = tk.Label(hitFrame, text="Caliber (inches): ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=caliberRow, column=0)

        caliberMOAEntry.grid(
            row=caliberRow, column=1,columnspan=entryspan)
                                
        windLabel  = tk.Label(hitFrame, text="Wind Handling (90deg 10mph, MOA): ",
                             anchor="w",bg=themeColor,fg='white').grid(
                                 sticky='w',row=windEntryRow, column=0)
                                
        windErrorEntry.grid(
            row=windEntryRow, column=1,columnspan=entryspan)

        realWindLabel = tk.Label(hitFrame, text="Real Wind (mph): ",
                         anchor="w", bg=themeColor, fg='white')
        realWindLabel.grid(sticky='w', row=realWindRow, column=0)

        realWindEntry = tk.Entry(hitFrame)
        realWindEntry.insert(0, "5")
        realWindEntry.grid(row=realWindRow, column=1,columnspan=entryspan)
        
        
        hitrateLabel  = tk.Label(hitFrame, text="Hitrate: ",
                              anchor="w", bg=themeColor,fg='white').grid(
                                  sticky='w',row=hitRateRow, column=0)
                               
        hitrateResLabel = tk.Label(hitFrame, textvariable=hitrateVariable,
                                anchor="w", bg=themeColor,fg='white').grid(
                                    sticky='w',row=hitRateRow, column=1)
        
        distanceLabel = tk.Label(hitFrame, text="Distance (yards): ",
                                 anchor="w", bg=themeColor, fg='white')
        distanceLabel.grid(sticky='w', row=distanceRow, column=0)

        distanceEntry.grid(row=distanceRow, column=1, columnspan=entryspan)             

        shooterTypeVar = StringVar(hitFrame)
        
        shooterTypeVar.set(HitAnalysis.ShooterType.AVERAGE_HUNTER.value)  # Default value

        dropdown_options = [stype.value for stype in HitAnalysis.ShooterType]
        shooterTypeMenu = OptionMenu(hitFrame, shooterTypeVar, *dropdown_options)
        shooterTypeMenu.grid(row=shooterTypeRow, column=0, columnspan=3, sticky='ew')

        def grabAndCalculate():
            windMetric=10
            distanceEntryValue = int(distanceEntry.get())
            distanceEntryUnitfied = distanceEntryValue / 100.0 * 1.047
            targetSize = float(targetSizeEntry.get())/(distanceEntryUnitfied)
            caliberMOA = float(caliberMOAEntry.get())/(distanceEntryUnitfied)
            targetShapeValue    = getattr(HitAnalysis.TARGETSHAPE, targetShapeStr.get())
            shooterTypeValue = next(st for st in HitAnalysis.ShooterType if st.value == shooterTypeVar.get())
            shiftSwitch = HitAnalysis.getGenerateShiftParameters(shooterTypeValue)
            nominalWindErr = float(windErrorEntry.get())
            realWind = float(realWindEntry.get())
            shift = shiftSwitch[0] * (realWind/windMetric * nominalWindErr)
            wind = shiftSwitch[1] * (realWind/windMetric * nominalWindErr)/2
            velocityError = velocityErrorScale * wind


            hitAnalysisGuiFn(
                                         targetSize,
                                         caliberMOA,
                                         wind,
                                         velocityError,
                                         hitrateVariable,
                                         targetShapeValue,
                                         float(accuracyEntry.get()),
                                         shift)
        # 1 additional button
        hitrateLaunchButton = tk.Button(hitFrame, text="Hit Rate",
                                        command= grabAndCalculate,
                                        bg=buttonColor, fg='white').grid(
                                            row=goButtonRow, column=0, columnspan=3)
        
        hitFrame.grid()
    else:
        showHitModeNext = True
        hitFrame.grid_remove()

def hitAnalysisGuiFn(
    target_size,
    caliber,
    wind_err,
    velocity_err,
    hit_rate_variable,
    target_shape,
    accuracy,
    shift=0.0
):
    """Run hit analysis and display results in the UI.
    
    Args:
        target_size: Target size in MOA or inches.
        caliber: Bullet diameter in inches.
        wind_err: Wind reading error in MOA.
        velocity_err: Velocity/elevation error in MOA.
        hit_rate_variable: StringVar to display hit rate.
        target_shape: Target shape enum value.
        accuracy: Rifle precision in MOA.
        shift: Horizontal shift in MOA (default 0).
    """       
        
    if accuracy and accuracy > 0.01:
        hit_rate = HitAnalysis.hitAnalysis(accuracy, target_size, wind_err, velocity_err, 1, caliber, target_shape, shift)
        hit_rate_variable.set("%s%%" % int(hit_rate))

def displayUsage():
    """Display the help/usage documentation window."""
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
    """Display the about/credits window."""
    popup = Toplevel(top)

    popup.geometry("785x400")
    popup.title("About")
    labelOver = ttk.Label(popup, text=PyShootHelp.getAboutText())
    labelOver.grid(column=0,row=0, padx=(10,10));

def displayMathModelSelection():
    """Display the math model selection dialog."""
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
   
def displayHitrate():
    """Display hit rate calculator (simple or advanced based on settings)."""
    if showAngularHitAnalysis:
        displayAdvHitrate()
    else:
        displaySimpleHitrate()

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
totalTestSlider = tk.Scale(top, from_=1, to=maxTests, orient=HORIZONTAL, bg=themeColor,fg='white', length=(minx/2 + 10))
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
settingsMenu.add_command(label="Toggle Analysis Inputs", command=setupAngularHitAnalysis)

menubar.add_cascade(label="Expand Functions", menu=functionsMenu)
menubar.add_cascade(label="Help", menu=helpMenu)
menubar.add_cascade(label="Settings", menu=settingsMenu)

top.config(menu=menubar)
top.iconbitmap('PyShootGui.ico')
top.title("PyShoot")
top.mainloop()
