# Needed imports
import matplotlib.pyplot as plt
import math
from scipy.spatial import ConvexHull
import numpy as np
import random

# Application variables
accuracy=1.5 #MOA
shotcount=3


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

# inches. This simply controls how big the dots are
caliber=0.308 

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
ax.add_artist(plt.Circle((scale/2, scale/2), 0.125, color='darkorange'))

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
    plt.plot(hull.points[simplex,0], hull.points[simplex,1], 'k-')

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
plt.plot((exp1, exp2), (eyp1,eyp2),color='gold', linewidth=5)

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
