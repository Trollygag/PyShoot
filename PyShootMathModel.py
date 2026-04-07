"""PyShoot Math Model - Statistical distributions for shot group generation.

This module provides multiple statistical distribution models for generating
realistic bullet hole patterns and predicting shot dispersion.
"""
import math
import random
import numpy as np
import enum


class MathModel(enum.Enum):
    """Available statistical distributions for modeling shot groups."""
    NORMAL = 1
    WEIBULL_K1 = 2
    WEIBULL_K1_5 = 3
    WEIBULL_K3 = 4
    RAYLEIGH = 5

# Accuracy corrections for different distributions to normalize output
# These values ensure that different models produce similar average dispersion
NORMAL_ACCURACY_CORRECTION = 3.09
WEIBULL_K1_5_ACCURACY_CORRECTION = 0.42
WEIBULL_K3_ACCURACY_CORRECTION = 0.5
WEIBULL_K1_ACCURACY_CORRECTION = 1.0 / 3.0  # 0.33333...
RAYLEIGH_ACCURACY_CORRECTION = 0.463  # Correction for Rayleigh distribution

# Weibull shape parameters
K1 = 1.0      # Exponential distribution (k=1)
K1_5 = 1.5    # Between exponential and Rayleigh
K3 = 3.0      # More concentrated distribution
R = 2         # Rayleigh parameter

# Default model for group generation
MATH_MODEL = MathModel.WEIBULL_K1_5

def getMathModelOptions():
    """Return list of available math model names."""
    return [model.name for model in MathModel]

def setMathModel(model):
    """Set the global math model for shot group generation.
    
    Args:
        model: A MathModel enum value representing the distribution to use.
        
    Raises:
        ValueError: If the provided model is not a valid MathModel enum.
    """
    global MATH_MODEL
    if isinstance(model, MathModel):
        MATH_MODEL = model
        print("Math model set to: %s" % model.name)
    else:
        raise ValueError("Invalid MathModel provided. Use MathModel enum.")

def generateGroup(accuracy, shot_count, heat, scale):
    """Generate a shot group using the current math model.
    
    Args:
        accuracy: Precision in MOA (Minute of Angle).
        shot_count: Number of shots to generate.
        heat: Dispersion increase per shot (MOA/shot).
        scale: Canvas scale for centering shots.
        
    Returns:
        List of [x, y] coordinates representing bullet holes.
    """
    if MATH_MODEL == MathModel.NORMAL:
        return generateNormalGroup(accuracy, shot_count, heat, scale)
    elif MATH_MODEL == MathModel.WEIBULL_K1:
        return generateWeibullGroup(accuracy, shot_count, heat, scale, K1, WEIBULL_K1_ACCURACY_CORRECTION)
    elif MATH_MODEL == MathModel.WEIBULL_K1_5:
        return generateWeibullGroup(accuracy, shot_count, heat, scale, K1_5, WEIBULL_K1_5_ACCURACY_CORRECTION)
    elif MATH_MODEL == MathModel.WEIBULL_K3:
        return generateWeibullGroup(accuracy, shot_count, heat, scale, K3, WEIBULL_K3_ACCURACY_CORRECTION)
    elif MATH_MODEL == MathModel.RAYLEIGH:
        return generateWeibullGroup(accuracy, shot_count, heat, scale, R, RAYLEIGH_ACCURACY_CORRECTION)
    else:
        # Fallback to default
        return generateWeibullGroup(accuracy, shot_count, heat, scale, K1_5, WEIBULL_K1_5_ACCURACY_CORRECTION)
    
def generateNormalGroup(accuracy, shot_count, heat, scale):
    """Generate shot group using normal (Gaussian) distribution.
    
    Args:
        accuracy: Precision in MOA.
        shot_count: Number of shots.
        heat: Dispersion increase per shot.
        scale: Canvas scale for centering.
        
    Returns:
        List of [x, y] coordinates for bullet holes.
    """
    hits_list = []
    rng = np.random.default_rng()
    for shot in range(shot_count):
        # Standard deviation increases with heat
        sigma = (accuracy + (heat * shot)) / NORMAL_ACCURACY_CORRECTION
        hits_list.append(rng.normal(scale / 2, sigma, 2))
    return hits_list

def generateWeibullGroup(accuracy, shot_count, heat, scale, k, weibull_accuracy_correction):
    """Generate shot group using Weibull (or Rayleigh) distribution.
    
    This uses a radial distance approach with angle randomization to model
    realistic 2D shot dispersion patterns.
    
    Args:
        accuracy: Precision in MOA.
        shot_count: Number of shots.
        heat: Dispersion increase per shot.
        scale: Canvas scale for centering.
        k: Weibull shape parameter (determines distribution characteristics).
        weibull_accuracy_correction: Scaling factor to normalize output.
        
    Returns:
        List of [x, y] coordinates for bullet holes.
    """
    hits_list = []
    rng = np.random.default_rng()
    for shot in range(shot_count):
        # Random direction in radians (0 to 2π)
        direction = rng.uniform(0, 2 * math.pi)
        x_mod = math.cos(direction)
        y_mod = math.sin(direction)
        
        # Radial distance from Weibull distribution
        offset = rng.weibull(k, 1)
        
        # Adjust for heat and accuracy, then offset from center
        current_accuracy = accuracy + (heat * shot)
        dispersion = weibull_accuracy_correction * current_accuracy * offset[0]
        x_position = dispersion * x_mod + scale / 2
        y_position = dispersion * y_mod + scale / 2
        hits_list.append(np.array([x_position, y_position]))
    return hits_list