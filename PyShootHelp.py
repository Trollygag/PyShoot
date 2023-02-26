#!/usr/bin/env python3

def getOverviewText():
    text="\
##############################################################################################\n\n\
PyShoot is a shot modeling, hit rate analysis tool using a tuned normal distribution.\n\n\
The purpose is to allow a user build intuition for what could be possible group-to-group given\n\
a constant set of parameters. PyShoot produces organic looking groups the way your won rifle\n\
would and helps illustrate the extremes that are possible, probability of them happening, and\n\
how they might affect your chances of hitting a target over time.\
\n\n\
########################################## FEATURES ##########################################\
\n\nIn the current shooting culture, there is a trend of folks using small samples to draw big\n\
conclusions, that in reality, are not supported by probability and statistics.\n\n\
Pyshoot includes a number of features to combat this, such as:\n\n\
♦ Simulated targets, of which up to 20 can be generated at a time and illustrating\n\t\
correct target vs group vs bullet dimensions.\n\n\
♦ Monte-carlo hit rate simulator that simulates shooting against a target of your chosen size,\n\t\
your rifle's wind error handling performance, and your ammo's velocity spread, to\n\t\
give you a hit probability with center-of-target point of aim.\n\n\
♦ Up to 10,000 group sample analysis mode to show extremes of results with fast,\n\
\tnon-graphical computation\n\n\
##############################################################################################"
    return text

def getMainText():
    text="\
##############################################################################################\n\n\
\
##############################################################################################"
    return text

def getHitrateText():
    text="This is my hitrate text\n\
and there are lots of parts to it that\n\
I need to write"
    return text

def getDebugText():
    text="This is my debug text\n\
and there are lots of parts to it that\n\
I need to write"
    return text
    
def getAboutText():
    text="\
##############################################################################################\n\n\
v2023.02.25 - Developed by Trollygag.\n\n\
PyShoot is a shot modeling, hit rate analysis tool using\n\
a tuned normal distribution.\
\n\nFor more information, see:\n\
♦ reddit.com/u/Trollygag\n\
♦ github.com/Trollygag\n\n\
##############################################################################################\n\n\
Next features list:\n\n\
♦ Investigate alternate model distributions to account for more extreme variances\n\n\
♦ Add IPSC silhouette target, diamond target, and square.\
\n\n\
##############################################################################################"
    return text
