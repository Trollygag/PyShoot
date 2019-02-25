#!/usr/bin/env python3

import argparse
import getopt
import math
import random
import sys
from decimal import Decimal

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull


def pyshoot():
    # Application bounds
    lowerCal=0.17
    upperCal=0.5
    minShots=3
    maxShots=100000

    # Default Application variables
    accuracy=1.0 #MOA
    shotcount=3
    # inches. This simply controls how big the dots are
    caliber=0.308

    # TODO: Need better math for this. Should it scale based on number of shots?
    # Should it be fixed scale? Should it be 3 standard deviations as an integer?
    #scale=int(math.log(shotcount,2)+3) # MOA
    scale=8 # MOA

    # Heat value is dispersion added per shot as the barrel heats up.
    # In practice, barrels are often allowed to cool between strings and
    # the POI shift is more noticeable than dispersion.
    # Even small values fot his, like 0.01 MOA dispersion increase per shot, can become big
    # with large sample sizes. 
    heat=0.00

    # Override from command line
    def printUsage() :
        print("PyShoot.py")
        print("\t-h (help)")
        print("\t-a <accuracy in MOA>")
        print("\t-n <number of shots in the group>")
        print("\t-c <caliber in inches>")
        print("\t-x <heat dispersion per shot>")
        print("\t-s <scale in MOA (min 2)>")
        
        
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ha:n:c:x:s:")
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            sys.exit()
        elif opt == '-a':
            laccuracy = float(arg)
            if laccuracy > 0:
                accuracy = laccuracy
        elif opt == '-n':
            lshotcount = int(arg)
            if lshotcount >= minShots and lshotcount <= maxShots:
                shotcount = lshotcount
            else:
                print("Number of shots is out of range[",minShots,",",maxShots,"], defaulting to: ", shotcount)
        elif opt == '-x':
            lheat = float(arg)
            if lheat >= 0:
                heat=lheat
            else:
                print("Heat given is out of range, [0,∞]")
        elif opt == '-s':
            lscale = int(arg)
            if lscale >=2:
                scale=lscale
            else:
                print("Scale given is out of range, [2,∞]")
        elif opt == '-c':
            lcaliber=float(arg)
            if lcaliber >= lowerCal and lcaliber <= upperCal:
                caliber=lcaliber
            else:
                print("Caliber is out of range [",lowerCal,",",upperCal,"], defaulting to: ", caliber)





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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=Decimal, default=Decimal('1.0'), help='accuracy in MOA')
    parser.add_argument('-n', type=int, default=3, choices=range(3, 100000) help='number of shots in the group')
    parser.add_argument('-c', type=Decimal, default=Decimal('.308'), help='caliber in inches')
    parser.add_argument('-x', type=Decimal, default=Decimal('0'), help='heat dispersion per shot')
    parser.add_argument('-s', type=int, default=8, choices=range(2, 100), help='scale in MOA (min 2)')

    parser.parse_args()


if __name__ == '__main__':
    main()
