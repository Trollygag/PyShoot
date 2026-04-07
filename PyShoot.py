#!/usr/bin/env python3

import argparse
import math
import random
import functools

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from datetime import datetime
import PyShootMathModel


# Application bounds
LOWER_CAL = 0.17
UPPER_CAL = 0.5
MIN_SHOTS = 3
MAX_SHOTS = 100000

# Default Application variables
ACCURACY = 1.0 #MOA

SHOT_COUNT = 5
# inches. This simply controls how big the dots are
CALIBER = 0.308

# TODO: Need better math for this. Should it scale based on number of shots?
# Should it be fixed scale? Should it be 3 standard deviations as an integer?
#scale=int(math.log(shotcount,2)+3) # MOA
SCALE = 8 # MOA

# Heat value is dispersion added per shot as the barrel heats up.
# In practice, barrels are often allowed to cool between strings and
# the POI shift is more noticeable than dispersion.
# Even small values fot his, like 0.01 MOA dispersion increase per shot, can become big
# with large sample sizes. 
HEAT = 0.00

# Litz measured a heat affect of 0.0067 in MALRS2
HEAT_LITZ = 0.0067

# This stores the max ES and the coordinates from the points carrying them.
class ESParameters:
    """Container for Extreme Spread (ES) parameters and endpoint coordinates."""
    def __init__(self, es, exp1, exp2, eyp1, eyp2):
        self.es = es      # Extreme Spread distance
        self.exp1 = exp1  # First endpoint X coordinate
        self.exp2 = exp2  # Second endpoint X coordinate
        self.eyp1 = eyp1  # First endpoint Y coordinate
        self.eyp2 = eyp2  # Second endpoint Y coordinate     

# Small profiler to help take measurements
def printProfilerTime(timeStr):
    """Print current time with a descriptive message."""
    now = datetime.now()
    formatted_time = now.strftime("%H:%M:%S.%f")
    print("%s time: %s" % (timeStr, formatted_time))
    
# Calculate max polygon diameter using brute force method.
# TODO: Consider implementing rotating calipers algorithm for better performance.
def calculateES(hull):
    """Calculate the Extreme Spread (ES) of a convex hull."""
    max_length = 0
    exp1 = 0
    exp2 = 0
    eyp1 = 0
    eyp2 = 0
    
    for idx in range(len(hull.vertices)):
        for idx2 in range(idx + 1, len(hull.vertices)):
            xp1 = hull.points[hull.vertices[idx], 0]
            xp2 = hull.points[hull.vertices[idx2], 0]
            yp1 = hull.points[hull.vertices[idx], 1]
            yp2 = hull.points[hull.vertices[idx2], 1]
            xdiff = abs(xp2 - xp1)
            ydiff = abs(yp2 - yp1)
            distance = math.hypot(xdiff, ydiff)
            if distance > max_length:
                max_length = distance
                exp1 = xp1
                exp2 = xp2
                eyp1 = yp1
                eyp2 = yp2

    return ESParameters(max_length, exp1, exp2, eyp1, eyp2)

def drawTarget(hitsList, hull, esParams, scale, caliber):
    """Draw a target chart with shot placement and dispersion visualization."""
    # You can add or remove colors. More colors makes individual shots easier to spot
    colors = ['r', 'g', 'b', 'orange', 'gold', 'purple', 'darkcyan', 'sienna']
    color_count = len(colors)

    # This function draws the bullet holes as circles
    def drawHits(ax):
        for shot in range(len(hitsList)):
            circle = plt.Circle(hitsList[shot], caliber / 2, color=colors[shot % color_count])
            ax.add_artist(circle)
        return ax
       
    fig, ax = plt.subplots()  # Note: must use plt.subplots, not plt.subplot

    # Draw target bullseye (outer and center circles)
    ax.add_artist(plt.Circle((scale / 2, scale / 2), 0.5, fill=False, linewidth=8))
    ax.add_artist(plt.Circle((scale / 2, scale / 2), 0.125, color='black'))

    # Draw grid (square grid for reference)
    for i in range(int(scale)):
        plt.plot((0, scale), (i, i), linewidth=0.5, color='black')
        plt.plot((i, i), (0, scale), linewidth=0.5, color='black')

    # Draw hit distribution
    ax = drawHits(ax)

    # Draw convex hull outline
    for simplex in hull.simplices:
        plt.plot(hull.points[simplex, 0], hull.points[simplex, 1], 'k-', color='dimgray')

    # Draw line between the extreme spread endpoints
    line_width = max(1, int(caliber * 5 + 1))
    plt.plot((esParams.exp1, esParams.exp2), (esParams.eyp1, esParams.eyp2),
             color='gold', linewidth=line_width)

    # Set chart dimensions
    plt.ylim(0, scale)
    plt.xlim(0, scale)
    plt.gca().set_aspect('equal', adjustable='box')

    # Set title with the MOA calculation of extreme spread
    title_str = "Dispersion: %.2f MOA C-C" % esParams.es
    plt.title(title_str)

def show():
    plt.show()

def pyshootlite(accuracy, number, heat, caliber):
    """Generate and display a single group with automatic scaling."""
    # Determine scale based on accuracy
    if accuracy > 3:
        scale = round(accuracy * 3)
    else:
        scale = 8
    
    # Validate inputs
    validateAccuracy(accuracy)
    validateNumShots(number)
    validateHeat(heat)
    validateCaliber(caliber)
    
    pyshoot(accuracy, number, heat, scale, caliber)

def pyshootCalculate(accuracy, number):
    """Calculate Extreme Spread without graphical output."""
    # Determine scale based on accuracy
    if accuracy > 3:
        scale = round(accuracy * 3)
    else:
        scale = 8
    
    # Validate inputs
    validateAccuracy(accuracy)
    validateNumShots(number)
    
    # Generate group and calculate ES
    hits_list = PyShootMathModel.generateGroup(accuracy, number, HEAT, scale)
    # Calculate convex hull (polygon that captures the outside of the hits)
    hull = ConvexHull(hits_list)
    es_params = calculateES(hull)
    return es_params.es
            
def pyshoot(accuracy, number, heat, scale, caliber):
    """Generate a single shot group and display the results."""
    printProfilerTime("Start Pyshoot Generation/Calc")
    
    # Generate shot group
    hits_list = PyShootMathModel.generateGroup(accuracy, number, heat, scale)
    
    # Calculate convex hull (polygon that captures the outside of the hits)
    hull = ConvexHull(hits_list)
    es_params = calculateES(hull)
    
    printProfilerTime("End Pyshoot Generation/Calc")
    drawTarget(hits_list, hull, es_params, scale, caliber)

def check_int_range(val, min_val=None, max_val=None):
    """Input validation function for integers."""
    exc = argparse.ArgumentTypeError('%s is an invalid value' % val)
    try:
        ival = int(val)
    except ValueError:
        raise exc

    if min_val is not None and ival < min_val:
        raise exc
    if max_val is not None and ival > max_val:
        raise exc
    return ival


def check_float_range(val, min_val=None, max_val=None):
    """Input validation function for floats."""
    exc = argparse.ArgumentTypeError('%s is an invalid value' % val)
    try:
        fval = float(val)
    except ValueError:
        raise exc

    if min_val is not None and fval < min_val:
        raise exc
    if max_val is not None and fval > max_val:
        raise exc
    return fval

def validateHeat(heat):
    """Validate heat soak parameter (must be >= 0)."""
    return check_float_range(heat, min_val=0)

def validateAccuracy(accuracy):
    """Validate accuracy/precision parameter (must be > 0)."""
    return check_float_range(accuracy, min_val=0.001)

def validateNumShots(number):
    """Validate number of shots (must be between MIN_SHOTS and MAX_SHOTS)."""
    return check_int_range(number, min_val=MIN_SHOTS, max_val=MAX_SHOTS)

def validateCaliber(caliber):
    """Validate caliber diameter (must be between LOWER_CAL and UPPER_CAL)."""
    return check_float_range(caliber, min_val=LOWER_CAL, max_val=UPPER_CAL)

def main():
    """Main function for PyShoot."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--accuracy',
        type=functools.partial(validateAccuracy),
        default=ACCURACY,
        help='accuracy in MOA (default: %s min: %s)' % (ACCURACY, 0.1))
    parser.add_argument(
        '-n',
        '--number',
        type=functools.partial(validateNumShots),
        default=SHOT_COUNT,
        help='number of shots in the group (default: %s min: %s max: %s)' % (SHOT_COUNT, MIN_SHOTS, MAX_SHOTS))
    parser.add_argument(
        '-c',
        '--caliber',
        type=functools.partial(check_float_range, min_val=LOWER_CAL - .001, max_val=UPPER_CAL + .001),
        default=CALIBER,
        help='caliber in inches (min: %s max: %s)' % (LOWER_CAL, UPPER_CAL))
    parser.add_argument(
        '-x',
        '--heat',
        type=functools.partial(check_float_range, min_val=-.001),
        default=HEAT,
        help='heat dispersion per shot (default: %s min: %s)' % (HEAT, 0))
    parser.add_argument(
        '-s',
        '--scale',
        type=functools.partial(check_int_range, min_val=1, max_val=101),
        default=SCALE,
        help='scale in MOA (default: %s min: %s max: %s)' % (SCALE, 2, 100))

    args = parser.parse_args()

    pyshoot(args.accuracy, args.number, args.heat, args.scale, args.caliber)
    show()

if __name__ == '__main__':
    main()
