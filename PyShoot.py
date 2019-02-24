# Exception Handler
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)

import sys
sys.excepthook = show_exception_and_exit

# Needed imports
import matplotlib.pyplot as plt
import math
from scipy.spatial import ConvexHull
import numpy as np
import random

# Application variables
accuracy=1.5 #MOA
shotcount=3
#scale=int(math.log(shotcount,2)+3) # MOA
scale=8 # MOA

heat=0.00
caliber=0.308 # inches
colors=['r','g','b']
hitsList = []

def addHits(ax) :
    
    for shot in range(shotcount):
        point = np.random.normal(scale/2, ((accuracy/2)+(heat)*shot),2)
        hitsList.append(point)
        circle = plt.Circle(point, caliber/2, color=colors[shot%3])
        ax.add_artist(circle)
    return ax
   
# Main
# Setup
fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

# Draw target dot
ax.add_artist(plt.Circle((scale/2, scale/2), 0.5, fill=False, linewidth=8))
ax.add_artist(plt.Circle((scale/2, scale/2), 0.125, color='darkorange'))

# Draw grid (square)
for i in range(int(scale)):
    plt.plot((0,scale), (i,i), linewidth=0.5,color='black')
    plt.plot((i,i), (0,scale), linewidth=0.5,color='black')

ax = addHits(ax)

hull=ConvexHull(hitsList)

distances=[]
# Draw connectors
for simplex in hull.simplices:
    print(simplex)
    plt.plot(hull.points[simplex,0], hull.points[simplex,1], 'k-')

# Brute force line length
maxLength = 0
exp1 = 0
exp2 = 0
eyp1 = 0
eyp2 = 0
print("Total Simplices: ", len(hull.vertices))
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

plt.plot((exp1, exp2), (eyp1,eyp2),color='gold', linewidth=5)

plt.ylim(0,scale)
plt.xlim(0,scale)
titleStr="Dispersion: "+format(maxLength, '.2f')+" MOA C-C"
plt.title(titleStr)
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
