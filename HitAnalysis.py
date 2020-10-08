#!/usr/bin/env python3

import argparse
import math
import random
import functools

import matplotlib.pyplot as plt
import numpy as np
import math

SAMPLES=10000
DOWNSELECT=50
SHOTSIZE=0.05
def calculateShots(windResistance, windError, vSD):
    shotsList = []
    stdDev=(windError/10) * windResistance;
    sdY=vSD/10*0.38
    print ("Calculating error from stdDev: %s"% stdDev)
    for shots in range(SAMPLES):
        shotsList.append((np.random.normal(0,stdDev,1),np.random.normal(0,sdY,1)))
    return shotsList    

def calcRadius(shot):
    return math.sqrt(shot[0]**2 + shot[1]**2)

def calculateHits(shots, targetSize):
    hitsList = []
    for shot in range(len(shots)):
        if(calcRadius(shots[shot]) <= (targetSize/2.0)):
            hitsList.append(shots[shot])
    return hitsList

def calculateMisses(shots, targetSize):
    missList = []
    for shot in range(len(shots)):
        if(calcRadius(shots[shot]) > (targetSize/2.0)):
            missList.append(shots[shot])
    return missList

def calculateHitsRatio(hits, shots):
    return len(hits)/len(shots)

def drawShots(hitsList, shotsList, targetSize):
    scale=targetSize*5
    # This function just draws dots
    def drawHits(ax) :
        for shot in range(0,len(hitsList)):
            if shot % DOWNSELECT == 0:
##            print(hitsList[shot])
                circle = plt.Circle((hitsList[shot][0]+(scale/2), hitsList[shot][1]+(scale/2)), SHOTSIZE, color='g')
                ax.add_artist(circle)
        for shot in range(0,len(shotsList)):
            if shot % DOWNSELECT == 0:
                circle = plt.Circle((shotsList[shot][0]+(scale/2), shotsList[shot][1]+(scale/2)), SHOTSIZE, color='r')
                ax.add_artist(circle)
        return ax
       
   # Setup
    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

    # Draw target dot
    ax.add_artist(plt.Circle((scale/2, scale/2), targetSize/2,  color="grey"))
    # Draw hit distribution
    ax = drawHits(ax)

    # Set dimensions
    plt.ylim(0,scale)
    plt.xlim(0,scale)
    plt.gca().set_aspect('equal', adjustable='box')

    # Set title with the MOA calculation of polygon distance
    titleStr="Hits diagram"
    plt.title(titleStr)

    # Draw
    plt.show()
    
def hitAnalysis(targetSize, windErrorReading, velocitySD, windResistance):
    shots = calculateShots(windResistance, windErrorReading, velocitySD)
    hits = calculateHits(shots, targetSize)
    misses = calculateMisses(shots, targetSize)
    drawShots(hits, misses, targetSize)
    print("ratio: %s%%, shots: %s, hits: %s" % (calculateHitsRatio(hits,shots)*100, len(shots), len(hits)))
    
def hitAnalysis():
    targetSize=2
    windError=2
    SD=15
    shots = calculateShots(6.5, windError,10)
    hits = calculateHits(shots, targetSize)
    misses = calculateMisses(shots, targetSize)
    drawShots(hits, misses, targetSize)
    print("ratio: %s%%, shots: %s, hits: %s" % (calculateHitsRatio(hits,shots)*100, len(shots), len(hits)))

    
def main():
    hitAnalysis()

if __name__ == '__main__':
    main()
