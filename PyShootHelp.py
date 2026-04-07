#!/usr/bin/env python3

def getOverviewText():
    text = "\
##############################################################################################\n\n\
PyShoot - Shot Modeling and Hit Rate Analysis Tool\n\n\
PyShoot is a ballistic simulation tool using statistically tuned, realistic distributions\n\
to model rifle shot groups and predict hit probabilities on targets.\n\n\
PURPOSE:\n\
The goal is to help shooters build accurate intuition about what group sizes are achievable\n\
given consistent parameters, and to understand the probability of extreme outliers. PyShoot\n\
generates realistic-looking groups the way your actual rifle would produce them, helping you\n\
understand the extremes that are possible, how often they occur, and how they affect your\n\
hit probability on targets over time.\n\n\
MOTIVATION:\n\
In modern shooting culture, many shooters draw broad conclusions from very small sample sizes\n\
without proper statistical support. PyShoot provides tools to combat this by generating large\n\
sample sets and analyzing them statistically.\n\n\
########################################## FEATURES ##########################################\n\n\
PyShoot includes the following key features:\n\n\
♦ Shot Group Simulation - Generate up to 20 simulated groups at a time with accurate\n\t\
representations of target size, group dispersion, and individual bullet diameters.\n\n\
♦ Monte Carlo Hit Rate Simulator - Simulate shooting against targets of any size while\n\t\
accounting for wind reading errors, velocity variation, precision capability, and\n\t\
other real-world factors. Provides hit probability statistics with center-of-aim\n\t\
point of impact.\n\n\
♦ Batch Analysis Mode - Analyze up to 10,000 shot groups at once with high-speed,\n\t\
non-graphical computation to identify extreme outliers and statistical extremes.\n\n\
##############################################################################################"
    return text

def getMainText():
    text = "\
##############################################################################################\n\n\
MAIN SHOT GROUP SIMULATOR\n\n\
The main function generates N shot groups at a specified precision (accuracy) level.\n\n\
VISUALIZATION:\n\
The generated charts display the correct bullet diameter alongside a 1 MOA bullseye at 100\n\
yards as reference, in rotating colors for each shot. If the Extreme Spread (ES) exceeds\n\
the default chart size, the display automatically scales to fit. The chart shows the bounding\n\
circle for the ES and draws a line connecting the two most extreme shots in gold.\n\n\
At the top of each chart is a readout showing the dispersion as Extreme Spread (ES) measured\n\
in Minute of Angle (MOA), center-to-center.\n\n\
FIELD DESCRIPTIONS:\n\n\
♦ Precision (MOA) - Represents rifle accuracy normalized to 5-shot Extreme Spread, measured\n\t\
in Minute of Angle. To use other group sizes (3-shot, 10-shot, etc.), use the Debug\n\t\
Analysis function. For example, if you measured a 0.75 MOA 3-shot average, enter 3\n\t\
shots in the main window, adjust precision until the calculated MOA matches your\n\t\
measured value. This calibrates the model to your rifle.\n\n\
♦ Shots - The number of shots per group to simulate. This is theoretically unlimited,\n\t\
but be aware that very large group sizes (thousands of shots) combined with multiple\n\t\
trials can be computationally intensive and slow to render graphically.\n\n\
♦ Heat (MOA/Shot) - Accounts for barrel heat causing increased shot dispersion as the\n\t\
barrel heats up. Defaults to a small value; set to 0 to ignore barrel heat effects.\n\t\
At large sample scales (hundreds to thousands of shots), this parameter can have\n\t\
dramatic effects, sometimes increasing group sizes by orders of magnitude.\n\n\
♦ Caliber (inches) - The bullet diameter in inches. For metric calibers, convert to\n\t\
inches. This helps visualize group quality in terms of bullet diameters. For example,\n\t\
a 0.25 MOA group with .308 (7.62mm) bullets will show bullets almost overlapping at\n\t\
100 yards, as the ES is smaller than one bullet diameter.\n\n\
♦ Number Trials - The number of shot groups to generate simultaneously, up to 20.\n\n\
##############################################################################################"
    return text

def getHitrateText():
    text = "\
##############################################################################################\n\n\
MONTE CARLO HIT RATE ANALYZER\n\n\
The hit rate analysis tool uses Monte Carlo simulation to predict your probability of hitting\n\
a target given your rifle's precision, environmental factors, and shooting errors.\n\n\
METHODOLOGY:\n\
This tool requires input of factors that you must determine separately using ballistic\n\
software. Use tools like Applied Ballistics, Strelok, ShootersCalculator, or 4DOF to\n\
estimate your wind reading errors and elevation variance in Minute of Angle (MOA). The\n\
simulation uses these error sources combined with your rifle's precision to calculate hit\n\
probability. Precision input is pulled directly from the main PyShoot GUI.\n\n\
The simulation runs 10,000 shots internally, though only 100 are rendered on the chart for\n\
performance and clarity.\n\n\
CHART DISPLAY:\n\
• Green dots represent hits on the target\n\
• Red dots represent misses\n\
• The target is displayed at the specified size in Minute of Angle (MOA)\n\n\
TARGET SIZE DETERMINATION:\n\
To find your target size in MOA, either:\n\t\
1) Measure it using your scope's reticle (if you have MOA or mil markings)\n\t\
2) Use a known reference object and calculate back to MOA at your specific distance\n\n\
CALIBER AND EDGE STRIKES:\n\
The caliber input (in MOA) accounts for edge strikes—hits where the bullet partially\n\
strikes the target. Calculate this by converting your bullet diameter to MOA at your\n\
shooting distance. The chart scales to show bullet size but doesn't display bullets smaller\n\
than 0.05 MOA for clarity. Edge strikes are counted as hits if at least 15% of the bullet\n\
contacts the target.\n\n\
ACCURACY ASSUMPTIONS:\n\
The hit-rate calculation assumes you are centering your point of aim on the target. This\n\
represents the best-case scenario. In reality, factors like cold-bore shots or inexperienced\n\
shooters may shift impacts away from center, reducing actual hit probability.\n\n\
##############################################################################################"
    return text

def getDebugText():
    text = "\
##############################################################################################\n\n\
BATCH ANALYSIS AND DEBUG MODE\n\n\
The debug function enables validation of your model, reverse-engineering of parameters, and\n\
identification of extreme outliers across large sample sets.\n\n\
FEATURES:\n\
This mode runs high-speed batch analysis without graphical output (which would be slow with\n\
large samples—10,000 samples of 10 shots each takes approximately 8 seconds on modern\n\
hardware). Instead, it provides statistical summaries:\n\n\
♦ Minimum MOA - The smallest group size observed in the batch\n\t\
♦ Maximum MOA - The largest group size observed (the worst-case scenario)\n\t\
♦ Average MOA - The mean group size across all samples\n\n\
VALIDATION:\n\
Since measurements are normalized to 5-shot Extreme Spread, the calculated average MOA\n\
should closely match your input Precision value when running multiple samples (5 shots each)\n\
with zero heat soak. Any discrepancies indicate model calibration issues.\n\n\
SLIDER CONTROL:\n\
The slider bar controls the number of samples but has relatively coarse increments. To fine-tune\n\
the sample count by ±1, click in the gray area on either side of the slider button.\n\n\
USE CASES:\n\
• Validate that your precision input accurately represents your rifle\n\t\
• Understand the realistic extremes you might encounter\n\t\
• Analyze how heat soak affects dispersion over large shot volumes\n\t\
• Work backward from measured group sizes to find the precision value that matches\n\n\
##############################################################################################"
    return text
    
def getAboutText():
    text = "\
##############################################################################################\n\n\
PyShoot v2023.02.26\n\
Developed by Trollygag\n\n\
PyShoot is a comprehensive shot modeling and hit rate analysis tool using statistically\n\
realistic distributions to help shooters understand group formation, variability, and hit\n\
probability.\n\n\
For more information:\n\
♦ Reddit: reddit.com/u/Trollygag\n\
♦ GitHub: github.com/Trollygag\n\n\
##############################################################################################\n\n\
PLANNED FEATURES\n\n\
Future versions will include:\n\n\
♦ Alternative distribution models - Investigation of alternate statistical distributions\n\t\
to better model extreme variance outliers and unusual shot behaviors.\n\n\
♦ Environmental simulation - Expanded wind and environmental modeling capabilities.\n\n\
♦ Advanced analytics - More granular control over heat soak and environmental factors.\n\n\
##############################################################################################"
    return text

def getQuickStartText():
    text = "\
##############################################################################################\n\n\
QUICK START GUIDE\n\n\
Follow these steps to get started with PyShoot:\n\n\
STEP 1: MEASURE YOUR RIFLE'S PRECISION\n\
• Fire 5-shot groups at 100 yards at a known distance\n\
• Measure the Extreme Spread (ES) - the distance between the farthest two bullet holes\n\
• Convert this measurement to Minute of Angle (MOA): MOA = (Distance in inches / 100) / 1.047\n\
• This value is your Precision parameter\n\n\
STEP 2: DETERMINE YOUR BULLET SPECIFICATIONS\n\
• Know your bullet's diameter in inches (or convert from metric: mm ÷ 25.4 = inches)\n\
• Find your barrel's heat soak characteristics (typically 0.01-0.05 MOA per shot for hunting rifles)\n\t\
Start with 0 if unsure, then adjust based on results\n\n\
STEP 3: RUN BASIC SIMULATION\n\
• Enter your Precision value in the 'Precision (MOA)' field\n\
• Set 'Shots' to match your typical group size (e.g., 5 for 5-shot groups)\n\
• Set 'Caliber' to your bullet diameter in inches\n\
• Leave Heat at default or set to 0 for initial testing\n\
• Set 'Number Trials' to 1-3 to see a few examples\n\
• Click 'Pyshoot' to generate simulated groups\n\n\
STEP 4: ANALYZE HIT PROBABILITY\n\
• Go to Expand Functions → HitRate Calculator\n\
• Enter your target size (in MOA or inches, depending on the calculator you choose)\n\
• Set realistic wind and elevation error estimates (from ballistic software)\n\
• Click 'Hit Rate' to see your predicted hit probability\n\n\
STEP 5: VALIDATE YOUR MODEL\n\
• Go to Expand Functions → Debug Analytics\n\
• Run with high sample counts (8000-10000) and 5 shots per sample\n\
• The average MOA should closely match your input Precision\n\
• If it doesn't, adjust your Precision input and try again\n\n\
TIPS FOR BEST RESULTS\n\
♦ Use your actual measured group sizes; don't guess\n\
♦ Start simple: get the basic simulation working before adding complexity\n\
♦ Use the Debug mode to validate that your model matches reality\n\
♦ Remember: garbage in = garbage out. Accurate input = accurate predictions\n\n\
##############################################################################################"
    return text

def getGlossaryText():
    text = "\
##############################################################################################\n\n\
TECHNICAL GLOSSARY\n\n\
BALLISTICS TERMS:\n\
♦ MOA (Minute of Angle) - An angular measurement equal to 1/60th of a degree. At 100 yards,\n\t\
1 MOA ≈ 1.047 inches. Used to measure precision and wind/elevation corrections.\n\n\
♦ ES (Extreme Spread) - The distance between the two farthest bullet holes in a group,\n\t\
measured center-to-center or hole-to-hole depending on standard.\n\n\
♦ Group Size - The overall measurement of shot dispersion, typically expressed as ES in MOA.\n\t\
Smaller values indicate better precision.\n\n\
♦ Caliber - The diameter of the bullet in inches or millimeters. Common examples: .308 (7.62mm),\n\t\
.223 (5.56mm), .30-06 (7.62×63mm).\n\n\
♦ Heat Soak - The phenomenon where repeated shots cause barrel temperature to increase,\n\t\
leading to reduced accuracy. Measured as MOA increase per shot.\n\n\
STATISTICAL TERMS:\n\
♦ Monte Carlo Simulation - A statistical technique using repeated random sampling to estimate\n\t\
probable outcomes. PyShoot uses this to predict hit probabilities.\n\n\
♦ Distribution - A mathematical model describing how shots scatter. PyShoot uses tuned\n\t\
distributions that model real-world rifle behavior.\n\n\
♦ Sample Size - The number of groups or shots analyzed. Larger samples provide more reliable\n\t\
statistical conclusions.\n\n\
♦ Outlier - A result far from the typical range, representing extreme but possible outcomes.\n\n\
SHOOTING TERMS:\n\
♦ POI (Point of Impact) - Where bullets actually strike the target.\n\n\
♦ POA (Point of Aim) - Where the shooter aims on the target.\n\n\
♦ Wind Reading Error - The shooter's or ballistic calculator's estimate uncertainty of wind speed\n\t\
and direction, expressed in MOA deviation at the target.\n\n\
♦ Elevation Error - Uncertainty in altitude/angle correction, typically from velocity variation\n\t\
or environmental factors, expressed in MOA.\n\n\
♦ Hit Rate/Hit Probability - The percentage of shots expected to hit the target given all\n\t\
specified error sources and target size.\n\n\
##############################################################################################"
    return text

def getTroubleshootingText():
    text = "\
##############################################################################################\n\n\
TROUBLESHOOTING GUIDE\n\n\
ISSUE: Generated groups don't look realistic\n\
SOLUTION:\n\
• Verify your Precision input is correct by checking your rifle's actual group sizes\n\
• Run Debug Analytics with high sample counts to see average MOA\n\
• If calculated average MOA ≠ input Precision, adjust your input value\n\
• Ensure zero Heat value when validating basic precision\n\n\
ISSUE: Hit rate seems too high or too low\n\
SOLUTION:\n\
• Verify target size is entered correctly and in the right units (MOA vs inches)\n\
• Check that wind and elevation error values are realistic (not too small)\n\
• Ensure Precision matches your rifle's actual accuracy\n\
• Remember: hit rate assumes perfect centering; real results may be lower\n\n\
ISSUE: Debug Analytics taking too long\n\
SOLUTION:\n\
• Reduce the sample count using the slider (start with 1000-2000)\n\
• Use fewer shots per group if possible\n\
• Try disabling any background programs to free up CPU resources\n\
• Note: 10,000 samples × 10 shots typically takes ~8 seconds\n\n\
ISSUE: Graphs not rendering or rendering slowly\n\
SOLUTION:\n\
• Reduce the number of trials to generate (max 20 can be slow)\n\
• Reduce the number of shots per group\n\
• Run in Debug mode instead (no graphics, much faster)\n\
• Close other applications to free up system memory\n\n\
ISSUE: Heat soak parameter causing extreme group sizes\n\
SOLUTION:\n\
• Start with Heat value of 0.01-0.02 for hunting rifles\n\
• Remember: at high shot counts (1000+), heat soak effects multiply\n\
• Set to 0 if you want to ignore barrel heating effects entirely\n\
• Match heat soak value to your actual rifle testing results\n\n\
ISSUE: Caliber input not affecting results visibly\n\
SOLUTION:\n\
• Caliber only affects visualization (bullet circle size) and edge-strike calculations\n\
• It does NOT affect the group dispersion itself\n\
• Use caliber to understand how many bullet diameters wide your group is\n\n\
ISSUE: \"Invalid accuracy\" error in hit rate calculation\n\
SOLUTION:\n\
• Ensure Precision (MOA) value is greater than 0.01\n\
• Enter a positive number in the Precision field on the main screen\n\
• Reset fields using default values if needed\n\n\
##############################################################################################"
    return text

def getAdvancedTipsText():
    text = "\
##############################################################################################\n\n\
ADVANCED USAGE TIPS\n\n\
PARAMETER TUNING:\n\n\
Calibrating Precision to Non-Standard Group Sizes:\n\
• PyShoot normalizes to 5-shot groups. For other sizes:\n\
• Measure your 3-shot groups, convert to MOA, enter \"3\" in Shots field\n\
• Adjust Precision in small increments (0.01 MOA) until Debug shows correct average\n\
• This calibrated value is your rifle's true precision at that specific group size\n\n\
Heat Soak Modeling:\n\
• Measure precision at two different shot counts (e.g., shots 1-5 and 50-55)\n\
• Calculate: Heat = (MOA_difference) / (number of shots between measurements)\n\
• Enter this derived value in the Heat field for realistic long-range simulation\n\
• At extreme shot counts (1000+), heat soak becomes dominant; enable for realistic data\n\n\
ADVANCED HIT RATE ANALYSIS:\n\n\
Wind Reading Error Estimation:\n\
• For unknown wind characteristics, run multiple ballistic calculations with different\n\t\
wind speed estimates (±5 mph on actual wind)\n\
• Compare resulting impact points; divide range by 2 to get ±MOA error\n\
• This conservative estimate accounts for shooter reading ability + ballistic uncertainty\n\n\
Velocity Variation Analysis:\n\
• Use ammunition chronograph data or manufacturer specs\n\
• Standard deviation × 0.25 = approximate MOA at 100 yards (varies by caliber/distance)\n\
• Compare against your ballistic software's velocity sensitivity calculation\n\n\
Edge Strike Calculations:\n\
• Bullet MOA = (bullet diameter in inches / distance in yards) / 1.047\n\
• Example: .308 at 200 yards = (0.308 / 200) / 1.047 = 0.00147 MOA\n\
• Enter this value as your Caliber parameter for realistic hit probability with near-misses\n\n\
TARGET SIZE CONVERSION:\n\
• Measure target height in inches at your shooting distance\n\
• Target MOA = (height in inches / distance in yards) / 1.047\n\
• Example: 12-inch target at 300 yards = (12 / 300) / 1.047 = 0.0382 MOA\n\n\
BATCH ANALYSIS STRATEGIES:\n\n\
Finding Statistical Extremes:\n\
• Run Debug Analytics at 10,000 samples to identify worst-case scenarios\n\
• Use this data to establish realistic expectations for rare events\n\
• Useful for understanding \"once in 10,000 shots\" type outliers\n\n\
Reverse Engineering:\n\
• Measure actual group sizes from your rifle across many shot counts\n\
• Use Debug mode to find Precision and Heat values that match your data\n\
• This creates a validated model specific to your rifle\n\n\
Sensitivity Analysis:\n\
• Run simulations with slightly different parameters (±0.05 MOA precision)\n\
• Observe how sensitive hit rates are to precision changes\n\
• Identify which factors have the most impact on your results\n\n\
PERFORMANCE OPTIMIZATION:\n\n\
Multi-Trial Analysis:\n\
• Running 20 trials at once is slower than running 1 trial 20 times\n\
• But 20 trials shows group-to-group variation better than 1 trial repeated\n\
• Choose based on your needs: speed vs. visual insight\n\n\
Math Model Selection:\n\
• Different distributions affect extreme outlier frequency\n\
• Experiment via Settings → Select Math Model to see differences\n\
• Use the distribution that best matches your actual rifle data\n\n\
##############################################################################################"
    return text
