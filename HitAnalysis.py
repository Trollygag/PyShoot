#!/usr/bin/env python3

import argparse
import math
import random
import functools
import PyShoot

import matplotlib.pyplot as plt
import numpy as np
import math

SAMPLES=10000
DOWNSELECT=50
SHOTSIZE=0.05
SCALE=8

def calculateShots(accuracy, windResistance, windError, vSD):
    
    shotsList = PyShoot.generateGroup(accuracy, SAMPLES, 0, 0)
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

def drawShots(hitsList, missesList, targetSize):
    # This function just draws dots
    def drawHits(ax) :
        for shot in range(0,len(hitsList)):
            if shot % DOWNSELECT == 0:
##            print(hitsList[shot])
                circle = plt.Circle((hitsList[shot][0]+(SCALE/2), hitsList[shot][1]+(SCALE/2)), SHOTSIZE, color='g')
                ax.add_artist(circle)
        for shot in range(0,len(missesList)):
            if shot % DOWNSELECT == 0:
                circle = plt.Circle((missesList[shot][0]+(SCALE/2), missesList[shot][1]+(SCALE/2)), SHOTSIZE, color='r')
                ax.add_artist(circle)
        return ax
       
   # Setup
    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

    # Draw target dot
    ax.add_artist(plt.Circle((SCALE/2, SCALE/2), targetSize/2,  color="grey"))
    
    # Draw hit distribution
    ax = drawHits(ax)

    # Set dimensions
    plt.ylim(0,SCALE)
    plt.xlim(0,SCALE)
    plt.gca().set_aspect('equal', adjustable='box')

    # Set title with the MOA calculation of polygon distance
    titleStr="Hits diagram"
    plt.title(titleStr)

    # Draw
    plt.show()
    
def hitAnalysis(accuracy=1, targetSize=2, windErrorReading=2, velocitySD=15, windResistance=6.5):
    
    shots   = calculateShots(accuracy, windResistance, windErrorReading, velocitySD)
    hits    = calculateHits(shots, targetSize)
    misses  = calculateMisses(shots, targetSize)
    hitRate = calculateHitsRatio(hits, shots)*100
    print("ratio: %s%%, hits: %s, misses: %s" % (hitRate, len(hits), len(misses)))
    drawShots(hits, misses, targetSize)

    return hitRate
    
def main():
    hitAnalysis()

if __name__ == '__main__':
    main()
