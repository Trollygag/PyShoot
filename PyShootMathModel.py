import math
import random
import numpy as np
import enum


class MathModel(enum.Enum):
    NORMAL = 1
    WEIBULL_K1 = 2
    WEIBULL_K1_5 = 3
    WEIBULL_K3 = 4

# This is a correction to accuracy so that the normal distribution produces the mean
NORMAL_ACCURACY_CORRECTION=3.09
WEIBULL_K1_5_ACCURACY_CORRECTION=0.42
WEIBULL_K3_ACCURACY_CORRECTION = 0.5
WEIBULL_K1_ACCURACY_CORRECTION = .33333333
K1 = 1.0 # Weibull shape parameter
K1_5=1.5 # Weibull shape parameter
K3=3.0 # Weibull shape parameter

MATH_MODEL = MathModel.WEIBULL_K1_5
# This is the math model used for generating groups.

def getMathModelOptions():
    return [model.name for model in MathModel]

def setMathModel(model):
    global MATH_MODEL
    if isinstance(model, MathModel):
        MATH_MODEL = model
        print("Math model set to: " + model.name)
    else:
        raise ValueError("Invalid MathModel provided. Use MathModel enum.")

# This function just generates groups
def generateGroup(accuracy, shotcount, heat, scale):
    if MATH_MODEL == MathModel.NORMAL:
        return generateNormalGroup(accuracy, shotcount, heat, scale)
    elif MATH_MODEL == MathModel.WEIBULL_K1:
        return generateWeibullGroup(accuracy, shotcount, heat, scale, K1, WEIBULL_K1_ACCURACY_CORRECTION)
    elif MATH_MODEL == MathModel.WEIBULL_K1_5:
        return generateWeibullGroup(accuracy, shotcount, heat, scale, K1_5, WEIBULL_K1_5_ACCURACY_CORRECTION)
    elif MATH_MODEL == MathModel.WEIBULL_K3:
        return generateWeibullGroup(accuracy, shotcount, heat, scale, K3, WEIBULL_K3_ACCURACY_CORRECTION)
    
# This function just generates groups
def generateNormalGroup(accuracy, shotcount, heat, scale):
    #print("Group Generation with params: " + format(accuracy, '.2f') + " MOA, " + format(shotcount) + " shots, heat: " + format(heat) + ", scale: " + format(scale))
    hitsList = []
    rng = np.random.default_rng()
    for shot in range(shotcount):
        hitsList.append(rng.normal(scale/2, ((accuracy+(heat*shot))/NORMAL_ACCURACY_CORRECTION),2))
    return hitsList

# This function just generates groups
def generateWeibullGroup(accuracy, shotcount, heat, scale, K, WEIBULL_ACCURACY_CORRECTION):
    #print("Group Generation with params: " + format(accuracy, '.2f') + " MOA, " + format(shotcount) + " shots, heat: " + format(heat) + ", scale: " + format(scale) + ", K: " + format(K) + ", WEIBULL_ACCURACY_CORRECTION: " + format(WEIBULL_ACCURACY_CORRECTION))
    hitsList = []
    rng = np.random.default_rng()
    for shot in range(shotcount):
        direction = rng.uniform(0, 2*math.pi)
        xmod = math.cos(direction)
        ymod = math.sin(direction)  
        offset = rng.weibull(K,1)

        hitsList.append(np.array([WEIBULL_ACCURACY_CORRECTION*(accuracy+(heat*shot))*xmod*offset[0], WEIBULL_ACCURACY_CORRECTION*(accuracy+(heat*shot))*ymod*offset[0]])+np.array([scale/2,scale/2]))
    return hitsList