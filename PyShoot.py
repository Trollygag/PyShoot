#!/usr/bin/env python3

import argparse
import math
import random
import functools

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull


# Application bounds
LOWER_CAL = 0.17
UPPER_CAL = 0.5
MIN_SHOTS = 3
MAX_SHOTS = 100000

# Default Application variables
ACCURACY = 1.0 #MOA
SHOT_COUNT = 3
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


def pyshoot(accuracy, shotcount, heat, scale, caliber):
    # You can add or remove colors. More colors makes individual shots easier to spot
    colors=['r','g','b','orange','gold','purple','darkcyan','sienna'] 
    colorsize=len(colors)

    hitsList = []

    # This function might be doing a little too much. If you give it the model, it will
    # pull the application variables for shot count, scale, accuracy, and heat, and turn them
    # into a normal distribution of circles.
    def addHits(ax) :
        
        for shot in range(shotcount):
            point = np.random.normal(scale/2, ((accuracy/2)+(heat)*shot),2)
            hitsList.append(point)
            circle = plt.Circle(point, caliber/2, color=colors[shot%colorsize])
            ax.add_artist(circle)
        return ax
       
    # Main
    # Setup
    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

    # Draw target dot
    ax.add_artist(plt.Circle((scale/2, scale/2), 0.5, fill=False, linewidth=8))
    ax.add_artist(plt.Circle((scale/2, scale/2), 0.125, color='black'))

    # Draw grid (square)
    for i in range(int(scale)):
        plt.plot((0,scale), (i,i), linewidth=0.5,color='black')
        plt.plot((i,i), (0,scale), linewidth=0.5,color='black')

    # Draw hit distribution
    ax = addHits(ax)

    # Calculate convex hull (polygon that captures the outside of the hits)
    hull=ConvexHull(hitsList)

    distances=[]
    # Draw connectors for the convex hull
    for simplex in hull.simplices:
        print(simplex)
        plt.plot(hull.points[simplex,0], hull.points[simplex,1], 'k-', color='dimgray')

    # Calculate max polygon diameter. I don't know how to code a rotating calipers algorithm
    # so for now, I'm just brute forcing this.
    maxLength = 0
    exp1 = 0
    exp2 = 0
    eyp1 = 0
    eyp2 = 0
    print("Total Vertices: ", len(hull.vertices))
    for idx in range(len(hull.vertices)):
        for idx2 in range(idx+1,len(hull.vertices)):
            xp1 = hull.points[hull.vertices[idx],0]
            xp2 = hull.points[hull.vertices[idx2],0]
            yp1 = hull.points[hull.vertices[idx],1]
            yp2 = hull.points[hull.vertices[idx2],1]
            xdiff=math.fabs(xp2-xp1)
            ydiff=math.fabs(yp2-yp1)
            distance = math.hypot(xdiff, ydiff)
            if(distance > maxLength):
                maxLength = distance
                exp1=xp1
                exp2=xp2
                eyp1=yp1
                eyp2=yp2
            print("Evaluating: (", xp1, ",",yp1,") and (", xp2, ",",yp2,") to difference: ", distance)

    print (maxLength)

    # Draw line between the points of the max diameter
    plt.plot((exp1, exp2), (eyp1,eyp2),color='gold', linewidth=int(caliber*5+1))

    # Set dimensions
    plt.ylim(0,scale)
    plt.xlim(0,scale)
    plt.gca().set_aspect('equal', adjustable='box')

    # Set title with the MOA calculation of polygon distance
    titleStr="Dispersion: "+format(maxLength, '.2f')+" MOA C-C"
    plt.title(titleStr)


    # Draw
    plt.show()

    #Done


def check_int_range(val, min_val=None, max_val=None):
    """Input validation function for integers."""
    exc = argparse.ArgumentTypeError('%s is an invalid value' % val)
    try:
        ival = int(val)
    except ValueError:
        raise exc

    if min_val is not None and ival > min_val:
        raise exc
    if max_val is not None and ival < max_val:
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


def main():
    """Main function for PyShoot."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--accuracy',
        type=functools.partial(check_float_range, min_val=0),
        default=ACCURACY,
        help='accuracy in MOA (default: %s min: %s)' % (ACCURACY, 1))
    parser.add_argument(
        '-n',
        '--number',
        type=functools.partial(check_int_range, min_val=MIN_SHOTS - 1, max_val=MAX_SHOTS + 1),
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


if __name__ == '__main__':
    main()
