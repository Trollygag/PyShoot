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
♦ Monte Carlo hit rate simulator that simulates shooting against a target of your chosen size,\n\t\
your rifle's wind error handling performance, and your ammo's velocity spread, to\n\t\
give you a hit probability with center-of-target point of aim.\n\n\
♦ Up to 10,000 group sample analysis mode to show extremes of results with fast,\n\
\tnon-graphical computation\n\n\
##############################################################################################"
    return text

def getMainText():
    text="\
##############################################################################################\n\n\
The main screen function generates a number of N shot groups at some precision value.\n\n\
The generated charts plot the correct bullet diameter against a 1 MOA bullseye @ 100 yds,\n\
in multicolor rotation. If the MOA exceeds the default char size, the chart will scale to fit.\n\n\
The chart renders the bounding circle for the ES, and the link between the two most extreme\n\
shots with a gold line.\n\n\
At the top of the chart is a readout illustrating the dispersion as ES measured in MOA,\n\
center-to-center\n\n\
Field descriptions:\n\n\
♦ Precision - Normalized against 5 shot ES, given in MOA. If you want other MOA measures,\n\t\
like from 3 shot groups or 10 shot groups, use the debug function to figure out what\n\t\
those group sizes correlate to when starting from 5 shot. I.e., if you measured\n\t\
.75 MOA 3-shot average, then plug in 3 shots into the main window, bump up the\n\t\
debug slider a bit, and run it with different Precision values until the Calc\n\t\
MOA matches your measured 3-shot MOA.\n\n\
♦ Shots - Number of shots in each group sampled. This number is unbounded, but be aware\n\t\
that giving it tens of thousands of shots and multiple trials to run each, while it\n\t\
will compute the results quickly, rendering the graphs can take a while and be\n\t\
resource intensive.\n\n\
♦ Heat - A parameter to tune for the barrel heat soaking increasing dispersion.\n\t\
Defaults to a small value, but set to 0 if you want to ignore it. At big samples -\n\t\
hundreds to thousands of shots scale, this heat value can be kinda wonky -\n\t\
increasing group sizes by hundreds of times when normally it would be a\n\t\
small factor.\n\n\
♦ Caliber - The bullet diameter in inches. For metric bullets, convert to inches. This is\n\t\
helpful for building intuition of what a particular small group looks like in terms\n\t\
of width of the group in bullet diameters. I.e., a .25 MOA group with .308 bullets\n\t\
@ 100yds will have all bullets stacked on themselves with no gaps between them\n\t\
because the MOAmeasure of the ES is smaller than the width of the bullet in MOA.\n\n\
♦ Number Trials - Number of graphs you want to generate in one shot, up to 20.\n\n\
##############################################################################################"
    return text

def getHitrateText():
    text="\
##############################################################################################\n\n\
The hitrate analysis tool provides a Monte Carlo simulation of what would happen over time\n\
given what you know about your wind reading vs your ballistic performance, your elevation\n\
variance, and the angular target size.\n\n\
This tool does not provide you with the means of determining these factors - instead you can\n\
input your assumptions about head/cross winds, your wind reading ability, ballistic\n\
coefficient, speed, temperature, ammo velocity/SDs into a ballistic calculator (AB, Strelok\n\
shooterscalc, 4DOF, and others) to get a feel for what your min/max might be. Divide that\n\
by 2 to get the magnitude from center, in MOA, and input those error sources into the hitrate\n\
analysis tool. Precision is fed from the main pyshoot GUI.\n\n\
The internal default is modeling 10,000 shots, though only 100 shots are rendered onto\n\
the chart for illustration purposes and as a performance compromise.\n\n\
Hits are green, missses are red.\n\n\
The target is given as a shape of some MOA height. To determine the target size\n\
from real life, you will either need to measure it with your optic (mil or MOA), or have a\n\
known reference size to then back convert to MOA given your distance.\n\n\
The hit-rate readout assumes you are centering your POIs at the target. A cold bore shot or\n\
an inexperienced shooter may not account for this and may aim off target altogether, reducing\n\
effectiveness. In that sense, the hit percent could be interpreted s the best case scenario.\n\n\
The caliber readout in MOA allows you to account for edge-strikes on target. You will need\n\
to calculate this by taking your fired caliber and dividing by distance to get its MOA at\n\
the target and to stay same units as the target you shoot at. The chart drawing will scale\n\
somewhat to account for this, but will not draw bullet circles below 0.05 MOA.\n\
Edge strikes are counted if at least 15% of the bullet hits the edge.\n\n\
##############################################################################################"
    return text

def getDebugText():
    text="\
##############################################################################################\n\n\
The debug function is a way to validate your math, work backwards from what you have, and\n\
find out the most extreme extremes you might encounter in some given number of samples.\n\n\
There is no graphical chart (for performance reasons, 10,000 samples of 10 shots each is a\n\
8 second operation on my machine), but the lowest and highest encountered MOA  measurements\n\
are given, as well as the average MOA encountered. Since this is normalized against 5 shot,\n\
it should be that the calculated MOA at many samples, 5 shots per sample, and 0 heat soak\n\
matches the expected MOA from the top Precision box.\n\n\
The slider bar controls the number of samples but is a bit coarse. If you are trying to hit a\n\
specific number, you can click in the grey areas on either side of the slider to +/- by 1.\n\n\
##############################################################################################"
    return text
    
def getAboutText():
    text="\
##############################################################################################\n\n\
v2023.02.26 - Developed by Trollygag.\n\n\
PyShoot is a shot modeling, hit rate analysis tool using\n\
a tuned normal distribution.\
\n\nFor more information, see:\n\
♦ reddit.com/u/Trollygag\n\
♦ github.com/Trollygag\n\n\
##############################################################################################\n\n\
Next features list:\n\n\
♦ Investigate alternate model distributions to account for more extreme variances\n\n\
\n\n\
##############################################################################################"
    return text
