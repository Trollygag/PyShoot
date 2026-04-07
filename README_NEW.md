# PyShoot - Ballistic Simulation and Hit Rate Analysis

A comprehensive Python application for simulating rifle shot groups and analyzing hit probability. PyShoot uses statistically accurate distributions to model realistic bullet dispersion patterns, helping shooters understand group variability and predict hit rates under various conditions.

## Features

### Shot Group Simulator
- Generate realistic shot groups using multiple statistical distributions
- Simulate up to 20 groups simultaneously
- Account for barrel heat soak effects on accuracy
- Visual representation of shot placement with accurate bullet sizing
- Extreme Spread (ES) calculation and analysis

### Hit Rate Analyzer
- Monte Carlo simulation of shooting against targets
- Support for multiple target shapes (circles, squares, IPSC silhouettes, game animals)
- Account for wind reading errors and velocity variation
- Edge-strike hit detection
- Hit probability visualization

### Debug Analytics
- Batch analysis of 1-10,000 shot groups
- Identify statistical extremes and outliers
- Find minimum, maximum, and average group sizes
- Validate model against real-world rifle data

## Requirements

Python 3.6+ with the following dependencies:
- matplotlib - Plotting and visualization
- scipy - Scientific computing
- numpy - Numerical arrays and operations

### Installation

Using a [virtual environment](https://docs.python.org/3/library/venv.html) is highly recommended:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Or on Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -U -r requirements-to-freeze.txt
```

Alternatively, use [Anaconda](https://www.anaconda.com/distribution/):

```bash
conda create -n pyshoot python=3.9
conda activate pyshoot
conda install --file requirements-to-freeze.txt
```

## Usage

### GUI Application
```bash
python PyShootGui.py
```

The graphical interface provides:
- Main simulator for generating shot groups
- Hit rate calculator with advanced options
- Debug analytics for batch analysis
- Help documentation and glossary
- Settings for math model selection

### Command Line
```bash
python PyShoot.py -a 1.0 -n 5 -c 0.308 -x 0.01 -s 8
```

Options:
- `-a, --accuracy` - Precision in MOA (default: 1.0)
- `-n, --number` - Number of shots per group (default: 5)
- `-c, --caliber` - Bullet diameter in inches (default: 0.308)
- `-x, --heat` - Heat dispersion per shot in MOA (default: 0.0)
- `-s, --scale` - Display scale in MOA (default: 8)

### Hit Analysis
```bash
python HitAnalysis.py
```

## Module Reference

### PyShoot.py
Core shot group generation and visualization.

### PyShootMathModel.py
Statistical distributions for modeling shot patterns:
- Normal distribution
- Weibull K=1.0 (exponential-like)
- Weibull K=1.5 (default, well-balanced)
- Weibull K=3.0 (more concentrated)
- Rayleigh distribution

### HitAnalysis.py
Hit probability calculations and target visualization.

### PyShootGui.py
Tkinter-based graphical user interface.

### PyShootHelp.py
Help text and documentation content.

## Quick Start

1. **Measure your rifle's accuracy**
   - Fire 5-shot groups at 100 yards
   - Measure Extreme Spread (ES) in inches
   - Convert to MOA: MOA = (inches / 100) / 1.047

2. **Run the simulator**
   - Launch `PyShootGui.py`
   - Enter precision, shots, and caliber
   - Click "Pyshoot" to generate groups

3. **Validate your model**
   - Go to Debug Analytics
   - Run with 8000+ samples at 5 shots per sample
   - Average MOA should match your input precision

4. **Analyze hit probability**
   - Go to Hit Rate Calculator
   - Enter target size and error estimates
   - View predicted hit rate

## Mathematical Model

PyShoot models shot dispersion using radial Weibull distributions:
- Random direction (0-2π radians)
- Radial distance from Weibull/Rayleigh/Normal
- Heat soak increases dispersion per shot
- Multiple models available for different shooting scenarios

## Tips for Accuracy

- Use measured group sizes, not estimates
- Account for barrel heating in high-volume shooting
- Validate model against your actual rifle data
- Start with simple scenarios before adding complexity
- Remember: model accuracy depends on input accuracy

## Troubleshooting

**Groups look unrealistic?**
- Verify your precision measurement
- Run debug mode to check average MOA
- Calibrate precision until it matches your rifle

**Hit rate seems wrong?**
- Check target size units (MOA vs inches)
- Ensure wind/elevation errors are realistic
- Verify precision matches your rifle

**Slow rendering?**
- Reduce number of trials
- Reduce shots per group
- Use Debug mode instead (faster, no graphics)

## License

See LICENSE file for details.

## Credits

Developed by Trollygag  
Based on ballistic principles and statistical analysis techniques

## Resources

- [Shooting Reddit Community](https://reddit.com/r/longrange)
- [Applied Ballistics](https://www.appliedballisticsllc.com/)
- [Shooter's Calculator](https://www.snipertools.com/)
