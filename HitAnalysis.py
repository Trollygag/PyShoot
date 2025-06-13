#!/usr/bin/env python3

import argparse
import math
import random
import functools
import PyShoot
import PyShootMathModel

import matplotlib.pyplot as plt
import numpy as np
import math
import enum
import os

class ShapesEnum(enum.Enum):
    CIRCLE="Circle"
    SQUARE="Square"
    DIAMOND="Diamond"
    IPSC="IPSC"
    HOG="Hog"
    DEER="Deer"
    ELK="Elk"

HOG_MOA=7
DEER_MOA=9
ELK_MOA=15

SAMPLES=10000
DOWNSELECT=50
MIN_SHOTSIZE=0.1
MAX_SHOTSIZE=0.50
SCALE=8
TARGETSHAPE=ShapesEnum.CIRCLE

# vs overall height
IPSC_SCALE_X=0.6
IPSC_SCALE_BODY=0.8
IPSC_SCALE_HEAD=0.2

def getTargetTypes():
    return [shape.name for shape in ShapesEnum]

def calculateShots(accuracy, windResistance, windError, vSD):
    shotsList = PyShootMathModel.generateGroup(accuracy, SAMPLES, 0, 0)
    return correctShots(shotsList, windResistance, windError, vSD)    

def correctShots(shotsList, windResistance, windError, vSD):
    #(windError/10) * windResistance;
    #sdY    = vSD/10*0.38
    avgX = 0
    avgY = 0
    for shots in range(len(shotsList)):
        xMod = np.random.normal(0, windError, 1);
        yMod = np.random.normal(0, vSD, 1);
        shotsList[shots][0] = shotsList[shots][0] + xMod;
        shotsList[shots][1] = shotsList[shots][1] + yMod;
        avgX = avgX + shotsList[shots][0]
        avgY = avgY + shotsList[shots][1]

    avgX = avgX / len(shotsList)
    avgY = avgY / len(shotsList)
    print("avg X %s, avg Y %s" % (avgX, avgY))
    return shotsList
            

def calcRadius(shot):
    # For each shot, calculate the magnitude of X/Y components
    return math.sqrt(shot[0]**2 + shot[1]**2)

def getCircleTargetSize(targetSize, caliber):
    return ((targetSize/2.0)+(.85*caliber))

def calculateCircleHit(shot, targetSize, caliber):
    return calcRadius(shot) <= getCircleTargetSize(targetSize, caliber)

def calculateSquareHit(shot, targetSize, caliber):
    return calculateRectangleHit(shot,targetSize,targetSize,caliber)

def calculateRectangleHit(shot, targetSizeX, targetSizeY, caliber):
    targetMaxXAxis = (targetSizeX/2.0) + (.85*caliber)
    targetMaxYAxis = (targetSizeY/2.0) + (.85*caliber)
    shotX = abs(shot[0])
    shotY = abs(shot[1])
    return (shotX<= targetMaxXAxis) and (shotY<=targetMaxYAxis)

def calculateDiamondHit(shot, targetSize, caliber):
    # Just needs magnitude X/Y from center, only dealing with one corner since there is symmetry
    targetMaxAxis = (targetSize/2.0) + calculateAngleHeight(.85*caliber)
    shotX = abs(shot[0])
    shotY = abs(shot[1])

    # y=mx+b, in this case
    # y=x+targetMaxAxis
    # starts the same as a square, but also restrict it to below the slope
    return (shotY <= ((-1*shotX)+targetMaxAxis))

def calculateIPSCHit(shot, targetSize, caliber):
    shiftedShot = []
    shiftedShot.append(shot[0])
    shiftedShot.append(shot[1] - ((targetSize*IPSC_SCALE_BODY / 2) + (targetSize*IPSC_SCALE_HEAD / 2)))
    hitBody = calculateRectangleHit(shot, targetSize*IPSC_SCALE_X, targetSize*IPSC_SCALE_BODY, caliber)
    hitHead = calculateRectangleHit(shiftedShot, targetSize*IPSC_SCALE_HEAD, targetSize*IPSC_SCALE_HEAD, caliber)
    
    return hitBody or hitHead

def calculateHitsAndMisses(shots, targetSize, caliber, targetShape):
    hitsandmiss = []
    hitsList = []
    missesList = []
    # hits at index 0, misses at index 1
    hitsandmiss.append(hitsList)
    hitsandmiss.append(missesList)

    
    if(targetShape == ShapesEnum.CIRCLE):
        calculateShapeHit = calculateCircleHit
    elif(targetShape == ShapesEnum.SQUARE):
        calculateShapeHit = calculateSquareHit
    elif(targetShape == ShapesEnum.DIAMOND):
        calculateShapeHit = calculateDiamondHit
    elif(targetShape == ShapesEnum.IPSC):
        calculateShapeHit = calculateIPSCHit
    else:
        calculateShapeHit = calculateCircleHit
    
   
    for shot in range(len(shots)):
        if(calculateShapeHit(shots[shot], targetSize, caliber)):
            hitsandmiss[0].append(shots[shot])
        else:
            hitsandmiss[1].append(shots[shot])

    return hitsandmiss

def calculateHitsRatio(hits, shots):
    return len(hits)/len(shots)

def calculateRotatedUnitCenter(targetSize):
    return math.sqrt((targetSize/2.0)**2.0 * 2.0)

def calculateAngleHeight(targetSize):
    return 2.0 * math.sqrt((targetSize/2.0)**2.0 / 2.0)

def drawShots(hitsList, targetSize, caliber, targetShape):

    if targetSize > SCALE/2:
        LSCALE= targetSize * 2
    else:
        LSCALE = SCALE
    

    caliber = max(caliber,MIN_SHOTSIZE)
    caliber = min(caliber,MAX_SHOTSIZE)
    colorList = ['g','r']
    # This function just draws dots
    def drawHits(ax) :
        for shotIdx in range(0,2):
            for shot in range(0,len(hitsList[shotIdx])):
                if shot % DOWNSELECT == 0:
                    circle = plt.Circle((hitsList[shotIdx][shot][0]+(LSCALE/2), hitsList[shotIdx][shot][1]+(LSCALE/2)), caliber/2, color=colorList[shotIdx])
                    ax.add_artist(circle)
        return ax
       
   # Setup
    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

    # Draw target dot
    if(targetShape == ShapesEnum.CIRCLE):
        ax.add_artist(plt.Circle((LSCALE/2, LSCALE/2), targetSize/2,  color="grey"))
    elif(targetShape == ShapesEnum.SQUARE):
        ax.add_artist(plt.Rectangle((LSCALE/2 - (targetSize / 2), LSCALE/2 - (targetSize / 2)), targetSize, targetSize, color="grey"))
    elif(targetShape == ShapesEnum.DIAMOND):
        angledHeight = calculateAngleHeight(targetSize)
        translatedfactor = calculateRotatedUnitCenter(angledHeight)
        rectangle = plt.Rectangle(((LSCALE/2), (LSCALE/2 - translatedfactor)), angledHeight, angledHeight, color="grey", angle=45)
        ax.add_artist(rectangle)
    elif(targetShape == ShapesEnum.IPSC):
        # draw scaled body and head from the height
        targetY=targetSize*IPSC_SCALE_BODY
        targetX=targetSize*IPSC_SCALE_X
        targetHead=targetSize*IPSC_SCALE_HEAD
        rectangle = plt.Rectangle((LSCALE/2 - (targetX / 2), LSCALE/2 - (targetY / 2)), targetX, targetY, color="grey")
        rectangleHead = plt.Rectangle((LSCALE/2 - (targetHead / 2), (LSCALE/2 + targetY/2)), targetHead, targetHead, color="grey")
        ax.add_artist(rectangle)
        ax.add_artist(rectangleHead)
    elif(targetShape == ShapesEnum.HOG or targetShape == ShapesEnum.DEER or targetShape == ShapesEnum.ELK):

        LSCALE*=3
        # Example: Plot a hog silhouette image centered on the target
        import matplotlib.image as mpimg

        vitalScale = 1.0
        # Path to the hog image (should be a transparent PNG for best results)
        if targetShape == ShapesEnum.HOG:
            img_path = os.path.join(os.path.dirname(__file__), "hog_silhouette.png")
            #vitalScale = HOG_MOA
            vitalScale = 2.81
        elif targetShape == ShapesEnum.DEER:
            img_path = os.path.join(os.path.dirname(__file__), "deer_silhouette.png")
            #vitalScale = DEER_MOA
            vitalScale = 3.36
        elif targetShape == ShapesEnum.ELK:
            img_path = os.path.join(os.path.dirname(__file__), "elk_silhouette.png")
            #vitalScale = ELK_MOA
            vitalScale = 3.36
            
        
        if os.path.exists(img_path):
            img = mpimg.imread(img_path)
            # Calculate image extent to center and scale it to targetSize
            img_height, img_width = img.shape[0], img.shape[1]
            aspect = img_width / img_height
            # Scale image so its height matches targetSize
            img_display_height = targetSize* vitalScale
            img_display_width = img_display_height * aspect
            extent = [
                LSCALE/2 - img_display_width,
                LSCALE/2 + img_display_width,
                LSCALE/2 - img_display_height,
                LSCALE/2 + img_display_height
            ]
            ax.imshow(img, extent=extent, zorder=0)
        else:
            # Fallback: draw a rectangle as a placeholder
            ax.add_artist(plt.Rectangle((LSCALE/2 - (targetSize / 2), LSCALE/2 - (targetSize / 2)), targetSize, targetSize, color="grey"))
    
    # Draw hit distribution
    ax = drawHits(ax)

    # Set dimensions
    plt.ylim(0,LSCALE)
    plt.xlim(0,LSCALE)
    plt.gca().set_aspect('equal', adjustable='box')

    # Set title with the MOA calculation of polygon distance
    titleStr="Hits diagram"
    plt.title(titleStr)

    # Draw
    plt.show(block=False)
    
def hitAnalysis(accuracy=1, targetSize=2, windErrorReading=2, velocitySD=15, windResistance=6.5, caliber=0.05, targetShape=TARGETSHAPE):

    shots   = calculateShots(accuracy, windResistance, windErrorReading, velocitySD)
    hits    = calculateHitsAndMisses(shots, targetSize, caliber, targetShape)
    hitRate = calculateHitsRatio(hits[0], shots)*100
    print("ratio: %s%%, hits: %s, misses: %s" % (hitRate, len(hits[0]), len(hits[1])))
    drawShots(hits, targetSize, caliber, targetShape)

    return hitRate
    
def main():
    hitAnalysis()

if __name__ == '__main__':
    main()
