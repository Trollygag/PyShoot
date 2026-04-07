#!/usr/bin/env python3

import argparse
import math
import random
import functools
import os
import enum
import PyShoot
import PyShootMathModel
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class ShooterType(enum.Enum):
    """Represents different shooter skill levels and experience."""
    AVERAGE_HUNTER = "Average Hunter (Cold Bore)"
    EXPERT_HUNTER = "Expert LR Hunter (Cold Bore)"
    AVERAGE_COMPETITOR = "Average Competitor (Cold Bore)"
    WORLD_CLASS_SHOOTER = "World Class Shooter (Cold Bore)"
    EXPERT_SHOOTER = "Expert Shooter (Followup Shots)"
    WORLD_CLASS_SHOOTER_FU = "World Class Shooter (Followup Shots)"

class ShapesEnum(enum.Enum):
    """Represents different target shapes available for hit analysis."""
    CIRCLE = "Circle"
    SQUARE = "Square"
    DIAMOND = "Diamond"
    IPSC = "IPSC"
    HOG = "Hog"
    DEER = "Deer"
    ELK = "Elk"

HOG_MOA=7
DEER_MOA=9
ELK_MOA=15

SAMPLES=10000
DOWNSELECT=50
MIN_SHOTSIZE=0.02
MAX_SHOTSIZE=0.50
SCALE=8
TARGETSHAPE=ShapesEnum.CIRCLE

# vs overall height
IPSC_SCALE_X=0.6
IPSC_SCALE_BODY=0.8
IPSC_SCALE_HEAD=0.2

def getDefaultTargetSize(selected):
    """Return the default target size in MOA for the given shape."""
    if selected == ShapesEnum.CIRCLE:
        return 12
    elif selected == ShapesEnum.SQUARE:
        return 12
    elif selected == ShapesEnum.DIAMOND:
        return 12
    elif selected == ShapesEnum.IPSC:
        return 70
    elif selected == ShapesEnum.HOG:
        return HOG_MOA
    elif selected == ShapesEnum.DEER:
        return DEER_MOA
    elif selected == ShapesEnum.ELK:
        return ELK_MOA
    else:
        return 12
    
def getGenerateShiftParameters(shooterType):
    """Return shift parameters (shift_scale, wind_scale) for the given shooter type."""
    if shooterType == ShooterType.AVERAGE_HUNTER:
        return 1, 1
    elif shooterType == ShooterType.EXPERT_HUNTER:
        return 0.5, 0.5
    elif shooterType == ShooterType.AVERAGE_COMPETITOR:
        return 0.25, 0.25
    elif shooterType == ShooterType.WORLD_CLASS_SHOOTER:
        return 0.1, 0.1
    elif shooterType == ShooterType.EXPERT_SHOOTER:
        return 0, 0.1
    elif shooterType == ShooterType.WORLD_CLASS_SHOOTER_FU:
        return 0, 0.025
    else:
        raise ValueError("Invalid Shooter Type provided.")

def getTargetTypes():
    """Return list of available target shape names."""
    return [shape.name for shape in ShapesEnum]

def calculateShots(accuracy, windResistance, windError, vSD):
    shotsList = PyShootMathModel.generateGroup(accuracy, SAMPLES, 0, 0)
    return correctShots(shotsList, windResistance, windError, vSD)    

def correctShots(shots_list, wind_resistance, wind_error, v_sd):
    """Apply wind and velocity corrections to shot positions."""
    avg_x = 0
    avg_y = 0
    for shot in range(len(shots_list)):
        x_mod = np.random.normal(0, wind_error, 1)
        y_mod = np.random.normal(0, v_sd, 1)
        shots_list[shot][0] = shots_list[shot][0] + x_mod
        shots_list[shot][1] = shots_list[shot][1] + y_mod
        avg_x = avg_x + shots_list[shot][0]
        avg_y = avg_y + shots_list[shot][1]

    avg_x = avg_x / len(shots_list)
    avg_y = avg_y / len(shots_list)
    print("avg X: %.4f, avg Y: %.4f" % (avg_x, avg_y))
    return shots_list
            

def calcRadius(shot):
    """Calculate distance from center for a shot."""
    return math.sqrt(shot[0] ** 2 + shot[1] ** 2)

def getCircleTargetSize(target_size, caliber):
    """Get effective circle radius accounting for caliber."""
    return (target_size / 2.0) + (0.85 * caliber)

def calculateCircleHit(shot, target_size, caliber):
    """Check if shot hits circular target."""
    return calcRadius(shot) <= getCircleTargetSize(target_size, caliber)

def calculateSquareHit(shot, target_size, caliber):
    """Check if shot hits square target."""
    return calculateRectangleHit(shot, target_size, target_size, caliber)

def calculateRectangleHit(shot, target_size_x, target_size_y, caliber):
    """Check if shot hits rectangular target with given dimensions."""
    target_max_x = (target_size_x / 2.0) + (0.85 * caliber)
    target_max_y = (target_size_y / 2.0) + (0.85 * caliber)
    shot_x = abs(shot[0])
    shot_y = abs(shot[1])
    return (shot_x <= target_max_x) and (shot_y <= target_max_y)

def calculateDiamondHit(shot, target_size, caliber):
    """Check if shot hits diamond-shaped target."""
    # Magnitude X/Y from center, dealing with one corner due to symmetry
    target_max_axis = (target_size / 2.0) + calculateAngleHeight(0.85 * caliber)
    shot_x = abs(shot[0])
    shot_y = abs(shot[1])
    # Line equation: y = -x + targetMaxAxis
    return shot_y <= ((-1 * shot_x) + target_max_axis)

def calculateIPSCHit(shot, target_size, caliber):
    """Check if shot hits IPSC target (body + head)."""
    shifted_shot = [shot[0], shot[1] - ((target_size * IPSC_SCALE_BODY / 2) + (target_size * IPSC_SCALE_HEAD / 2))]
    hit_body = calculateRectangleHit(shot, target_size * IPSC_SCALE_X, target_size * IPSC_SCALE_BODY, caliber)
    hit_head = calculateRectangleHit(shifted_shot, target_size * IPSC_SCALE_HEAD, target_size * IPSC_SCALE_HEAD, caliber)
    return hit_body or hit_head

def calculateHitsAndMisses(shots, target_size, caliber, target_shape):
    """Categorize shots into hits and misses based on target shape."""
    hits_list = []
    misses_list = []

    # Select appropriate hit calculation function based on target shape
    if target_shape == ShapesEnum.CIRCLE:
        calculate_shape_hit = calculateCircleHit
    elif target_shape == ShapesEnum.SQUARE:
        calculate_shape_hit = calculateSquareHit
    elif target_shape == ShapesEnum.DIAMOND:
        calculate_shape_hit = calculateDiamondHit
    elif target_shape == ShapesEnum.IPSC:
        calculate_shape_hit = calculateIPSCHit
    else:
        calculate_shape_hit = calculateCircleHit

    # Categorize each shot
    for shot in shots:
        if calculate_shape_hit(shot, target_size, caliber):
            hits_list.append(shot)
        else:
            misses_list.append(shot)

    return [hits_list, misses_list]

def calculateHitsRatio(hits, shots):
    """Calculate hit rate as a ratio of hits to total shots."""
    return len(hits) / len(shots)

def calculateRotatedUnitCenter(target_size):
    """Calculate distance from center to corner of rotated square."""
    return math.sqrt((target_size / 2.0) ** 2 * 2.0)

def calculateAngleHeight(target_size):
    """Calculate height of diamond when rotated 45 degrees."""
    return 2.0 * math.sqrt((target_size / 2.0) ** 2 / 2.0)

def drawShots(hits_list, target_size, caliber, target_shape):
    """Draw visualization of hit and miss positions on target."""
    # Determine display scale
    if target_size > SCALE / 2:
        display_scale = target_size * 2
    else:
        display_scale = SCALE

    # Clamp caliber to valid display range
    caliber = max(caliber, MIN_SHOTSIZE)
    caliber = min(caliber, MAX_SHOTSIZE)
    color_list = ['g', 'r']  # Green for hits, red for misses

    # Function to draw bullet holes
    def drawHits(ax):
        for shot_idx in range(2):
            for shot in range(len(hits_list[shot_idx])):
                if shot % DOWNSELECT == 0:
                    circle = plt.Circle(
                        (hits_list[shot_idx][shot][0] + (display_scale / 2),
                         hits_list[shot_idx][shot][1] + (display_scale / 2)),
                        caliber / 2,
                        color=color_list[shot_idx]
                    )
                    ax.add_artist(circle)
        return ax

    # Setup plot
    fig, ax = plt.subplots()  # Must use plt.subplots, not plt.subplot

    # Draw target shape
    if target_shape == ShapesEnum.CIRCLE:
        ax.add_artist(plt.Circle((display_scale / 2, display_scale / 2), target_size / 2, color="grey"))
    elif target_shape == ShapesEnum.SQUARE:
        ax.add_artist(
            plt.Rectangle(
                (display_scale / 2 - (target_size / 2), display_scale / 2 - (target_size / 2)),
                target_size, target_size, color="grey"
            )
        )
    elif target_shape == ShapesEnum.DIAMOND:
        angled_height = calculateAngleHeight(target_size)
        translated_factor = calculateRotatedUnitCenter(angled_height)
        rectangle = plt.Rectangle(
            (display_scale / 2, display_scale / 2 - translated_factor),
            angled_height, angled_height,
            color="grey", angle=45
        )
        ax.add_artist(rectangle)
    elif target_shape == ShapesEnum.IPSC:
        # Draw scaled body and head
        target_y = target_size * IPSC_SCALE_BODY
        target_x = target_size * IPSC_SCALE_X
        target_head = target_size * IPSC_SCALE_HEAD
        rectangle = plt.Rectangle(
            (display_scale / 2 - (target_x / 2), display_scale / 2 - (target_y / 2)),
            target_x, target_y, color="grey"
        )
        rectangle_head = plt.Rectangle(
            (display_scale / 2 - (target_head / 2), display_scale / 2 + target_y / 2),
            target_head, target_head, color="grey"
        )
        ax.add_artist(rectangle)
        ax.add_artist(rectangle_head)
    elif target_shape in (ShapesEnum.HOG, ShapesEnum.DEER, ShapesEnum.ELK):
        display_scale *= 3
        # Plot animal silhouette image
        vital_scale = 1.0
        if target_shape == ShapesEnum.HOG:
            img_path = os.path.join(os.path.dirname(__file__), "hog_silhouette.png")
            vital_scale = 2.81
        elif target_shape == ShapesEnum.DEER:
            img_path = os.path.join(os.path.dirname(__file__), "deer_silhouette.png")
            vital_scale = 3.36
        elif target_shape == ShapesEnum.ELK:
            img_path = os.path.join(os.path.dirname(__file__), "elk_silhouette.png")
            vital_scale = 3.36

        target_scale = target_size * vital_scale
        display_scale = target_scale * 2

        if os.path.exists(img_path):
            img = mpimg.imread(img_path)
            # Calculate image extent to center and scale
            img_height, img_width = img.shape[0], img.shape[1]
            aspect = img_width / img_height
            img_display_height = target_size * vital_scale
            img_display_width = img_display_height * aspect
            extent = [
                display_scale / 2 - img_display_width,
                display_scale / 2 + img_display_width,
                display_scale / 2 - img_display_height,
                display_scale / 2 + img_display_height
            ]
            ax.imshow(img, extent=extent, zorder=0)
        else:
            # Fallback: draw rectangle placeholder
            ax.add_artist(
                plt.Rectangle(
                    (display_scale / 2 - (target_size / 2), display_scale / 2 - (target_size / 2)),
                    target_size, target_size, color="grey"
                )
            )

    # Draw hit distribution
    ax = drawHits(ax)

    # Set chart dimensions
    plt.ylim(0, display_scale)
    plt.xlim(0, display_scale)
    plt.gca().set_aspect('equal', adjustable='box')

    # Set title
    plt.title("Hit Distribution Diagram")
    plt.show(block=False)
    
def shiftShots(shots, shift):
    """Apply horizontal shift to all shots."""
    if shift == 0:
        return shots
    shifted_shots = []
    for shot in shots:
        shifted_shot = [shot[0] + shift, shot[1]]
        shifted_shots.append(shifted_shot)
    return shifted_shots

def hitAnalysis(
    accuracy=1,
    target_size=2,
    wind_error_reading=2,
    velocity_sd=15,
    wind_resistance=6.5,
    caliber=0.05,
    target_shape=TARGETSHAPE,
    shift=0
):
    """Perform hit analysis simulation and return hit rate percentage."""
    shots = calculateShots(accuracy, wind_resistance, wind_error_reading, velocity_sd)
    shots = shiftShots(shots, shift)
    hits = calculateHitsAndMisses(shots, target_size, caliber, target_shape)
    hit_rate = calculateHitsRatio(hits[0], shots) * 100
    print("Hit rate: %.2f%%, Hits: %d, Misses: %d" % (hit_rate, len(hits[0]), len(hits[1])))
    drawShots(hits, target_size, caliber, target_shape)
    return hit_rate
    
def main():
    hitAnalysis()

if __name__ == '__main__':
    main()
