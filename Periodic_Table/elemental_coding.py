import pygame
import sys
import math
import os

# Supress ALSA warnings by redirecting stderr to null
sys.stderr = open(os.devnull, 'w')

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Periodic Combinator - Periodic Table")

# Define colors
BACKGROUND = (44, 44, 47)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
ELEMENT_FONT_COLOR = (82, 87, 93)

# Pastel colors for element groups
ALKALI_METALS = (255, 204, 204)
ALKALINE_EARTH_METALS = (255, 229, 204)
TRANSITION_METALS = (255, 255, 204)
POST_TRANSITION_METALS = (229, 255, 204)
METALLOIDS = (204, 255, 204)
NONMETALS = (204, 255, 229)
HALOGENS = (204, 229, 255)
NOBLE_GASES = (229, 204, 255)
LANTHANIDES = (255, 204, 229)
ACTINIDES = (255, 229, 204)

# Set up fonts
# Default font for general text, size 29
font = pygame.font.Font(None, 29)
# Larger font for headings or emphasized text
large_font = pygame.font.Font(None, 36)
# Bold font for emphasis, size 33
bold_font = pygame.font.Font(None, 33)
bold_font.set_bold(True) # Set this font to bold

element_font = pygame.font.Font(None, 28)
# Font for popups, size 46
popup_font = pygame.font.Font(None, 46)

# Element cell size
CELL_SIZE = 53          # Size of each element cell in pixels
GRID_PADDING = 4        # Padding between cells in pixels
TABLE_OFFSET_X = 80     # Horizontal offset for the entire periodic table

# Define elements
ELEMENTS = {
    # Hydrogen and Helium
    'H': {'name': 'Hydrogen', 'color': NONMETALS, 'atomic_number': 1, 'mass': 1.008, 'electron_config': '1s1', 'shells': [1]},
    'He': {'name': 'Helium', 'color': NOBLE_GASES, 'atomic_number': 2, 'mass': 4.0026, 'electron_config': '1s2', 'shells': [2]},

    # Alkali Metals
    'Li': {'name': 'Lithium', 'color': ALKALI_METALS, 'atomic_number': 3, 'mass': 6.94, 'electron_config': '1s2 2s1', 'shells': [2, 1]},
    'Na': {'name': 'Sodium', 'color': ALKALI_METALS, 'atomic_number': 11, 'mass': 22.990, 'electron_config': '[Ne] 3s1', 'shells': [2, 8, 1]},
    'K': {'name': 'Potassium', 'color': ALKALI_METALS, 'atomic_number': 19, 'mass': 39.098, 'electron_config': '[Ar] 4s1', 'shells': [2, 8, 8, 1]},
    'Rb': {'name': 'Rubidium', 'color': ALKALI_METALS, 'atomic_number': 37, 'mass': 85.468, 'electron_config': '[Kr] 5s1', 'shells': [2, 8, 18, 8, 1]},
    'Cs': {'name': 'Cesium', 'color': ALKALI_METALS, 'atomic_number': 55, 'mass': 132.905, 'electron_config': '[Xe] 6s1', 'shells': [2, 8, 18, 18, 8, 1]},
    'Fr': {'name': 'Francium', 'color': ALKALI_METALS, 'atomic_number': 87, 'mass': 223, 'electron_config': '[Rn] 7s1', 'shells': [2, 8, 18, 32, 18, 8, 1]},

    # Alkaline Earth Metals
    'Be': {'name': 'Beryllium', 'color': ALKALINE_EARTH_METALS, 'atomic_number': 4, 'mass': 9.0122, 'electron_config': '1s2 2s2', 'shells': [2, 2]},
    'Mg': {'name': 'Magnesium', 'color': ALKALINE_EARTH_METALS, 'atomic_number': 12, 'mass': 24.305, 'electron_config': '[Ne] 3s2', 'shells': [2, 8, 2]},
    'Ca': {'name': 'Calcium', 'color': ALKALINE_EARTH_METALS, 'atomic_number': 20, 'mass': 40.078, 'electron_config': '[Ar] 4s2', 'shells': [2, 8, 8, 2]},
    'Sr': {'name': 'Strontium', 'color': ALKALINE_EARTH_METALS, 'atomic_number': 38, 'mass': 87.62, 'electron_config': '[Kr] 5s2', 'shells': [2, 8, 18, 8, 2]},
    'Ba': {'name': 'Barium', 'color': ALKALINE_EARTH_METALS, 'atomic_number': 56, 'mass': 137.327, 'electron_config': '[Xe] 6s2', 'shells': [2, 8, 18, 18, 8, 2]},
    'Ra': {'name': 'Radium', 'color': ALKALINE_EARTH_METALS, 'atomic_number': 88, 'mass': 226, 'electron_config': '[Rn] 7s2', 'shells': [2, 8, 18, 32, 18, 8, 2]},

    # Transition Metals
    'Sc': {'name': 'Scandium', 'color': TRANSITION_METALS, 'atomic_number': 21, 'mass': 44.955, 'electron_config': '[Ar] 3d1 4s2', 'shells': [2, 8, 9, 2]},
    'Ti': {'name': 'Titanium', 'color': TRANSITION_METALS, 'atomic_number': 22, 'mass': 47.867, 'electron_config': '[Ar] 3d2 4s2', 'shells': [2, 8, 10, 2]},
    'V': {'name': 'Vanadium', 'color': TRANSITION_METALS, 'atomic_number': 23, 'mass': 50.942, 'electron_config': '[Ar] 3d3 4s2', 'shells': [2, 8, 11, 2]},
    'Cr': {'name': 'Chromium', 'color': TRANSITION_METALS, 'atomic_number': 24, 'mass': 51.996, 'electron_config': '[Ar] 3d5 4s1', 'shells': [2, 8, 13, 1]},
    'Mn': {'name': 'Manganese', 'color': TRANSITION_METALS, 'atomic_number': 25, 'mass': 54.938, 'electron_config': '[Ar] 3d5 4s2', 'shells': [2, 8, 13, 2]},
    'Fe': {'name': 'Iron', 'color': TRANSITION_METALS, 'atomic_number': 26, 'mass': 55.845, 'electron_config': '[Ar] 3d6 4s2', 'shells': [2, 8, 14, 2]},
    'Co': {'name': 'Cobalt', 'color': TRANSITION_METALS, 'atomic_number': 27, 'mass': 58.933, 'electron_config': '[Ar] 3d7 4s2', 'shells': [2, 8, 15, 2]},
    'Ni': {'name': 'Nickel', 'color': TRANSITION_METALS, 'atomic_number': 28, 'mass': 58.693, 'electron_config': '[Ar] 3d8 4s2', 'shells': [2, 8, 16, 2]},
    'Cu': {'name': 'Copper', 'color': TRANSITION_METALS, 'atomic_number': 29, 'mass': 63.546, 'electron_config': '[Ar] 3d10 4s1', 'shells': [2, 8, 18, 1]},
    'Zn': {'name': 'Zinc', 'color': TRANSITION_METALS, 'atomic_number': 30, 'mass': 65.38, 'electron_config': '[Ar] 3d10 4s2', 'shells': [2, 8, 18, 2]},
    # More transition metals...
    'Ag': {'name': 'Silver', 'color': TRANSITION_METALS, 'atomic_number': 47, 'mass': 107.868, 'electron_config': '[Kr] 4d10 5s1', 'shells': [2, 8, 18, 18, 1]},
    'Au': {'name': 'Gold', 'color': TRANSITION_METALS, 'atomic_number': 79, 'mass': 196.967, 'electron_config': '[Xe] 4f14 5d10 6s1', 'shells': [2, 8, 18, 32, 18, 1]},

    # Post-Transition Metals
    'Al': {'name': 'Aluminum', 'color': POST_TRANSITION_METALS, 'atomic_number': 13, 'mass': 26.982, 'electron_config': '[Ne] 3s2 3p1', 'shells': [2, 8, 3]},
    'Ga': {'name': 'Gallium', 'color': POST_TRANSITION_METALS, 'atomic_number': 31, 'mass': 69.723, 'electron_config': '[Ar] 3d10 4s2 4p1', 'shells': [2, 8, 18, 3]},
    'In': {'name': 'Indium', 'color': POST_TRANSITION_METALS, 'atomic_number': 49, 'mass': 114.818, 'electron_config': '[Kr] 4d10 5s2 5p1', 'shells': [2, 8, 18, 18, 3]},
    'Sn': {'name': 'Tin', 'color': POST_TRANSITION_METALS, 'atomic_number': 50, 'mass': 118.710, 'electron_config': '[Kr] 4d10 5s2 5p2', 'shells': [2, 8, 18, 18, 4]},
    'Pb': {'name': 'Lead', 'color': POST_TRANSITION_METALS, 'atomic_number': 82, 'mass': 207.2, 'electron_config': '[Xe] 4f14 5d10 6s2 6p2', 'shells': [2, 8, 18, 32, 18, 4]},

    # Metalloids
    'B': {'name': 'Boron', 'color': METALLOIDS, 'atomic_number': 5, 'mass': 10.81, 'electron_config': '1s2 2s2 2p1', 'shells': [2, 3]},
    'Si': {'name': 'Silicon', 'color': METALLOIDS, 'atomic_number': 14, 'mass': 28.085, 'electron_config': '[Ne] 3s2 3p2', 'shells': [2, 8, 4]},
    'Ge': {'name': 'Germanium', 'color': METALLOIDS, 'atomic_number': 32, 'mass': 72.63, 'electron_config': '[Ar] 3d10 4s2 4p2', 'shells': [2, 8, 18, 4]},
    'As': {'name': 'Arsenic', 'color': METALLOIDS, 'atomic_number': 33, 'mass': 74.922, 'electron_config': '[Ar] 3d10 4s2 4p3', 'shells': [2, 8, 18, 5]},
    'Sb': {'name': 'Antimony', 'color': METALLOIDS, 'atomic_number': 51, 'mass': 121.760, 'electron_config': '[Kr] 4d10 5s2 5p3', 'shells': [2, 8, 18, 18, 5]},
    'Te': {'name': 'Tellurium', 'color': METALLOIDS, 'atomic_number': 52, 'mass': 127.60, 'electron_config': '[Kr] 4d10 5s2 5p4', 'shells': [2, 8, 18, 18, 6]},

    # Nonmetals
    'C': {'name': 'Carbon', 'color': NONMETALS, 'atomic_number': 6, 'mass': 12.011, 'electron_config': '1s2 2s2 2p2', 'shells': [2, 4]},
    'N': {'name': 'Nitrogen', 'color': NONMETALS, 'atomic_number': 7, 'mass': 14.007, 'electron_config': '1s2 2s2 2p3', 'shells': [2, 5]},
    'O': {'name': 'Oxygen', 'color': NONMETALS, 'atomic_number': 8, 'mass': 15.999, 'electron_config': '1s2 2s2 2p4', 'shells': [2, 6]},
    'P': {'name': 'Phosphorus', 'color': NONMETALS, 'atomic_number': 15, 'mass': 30.974, 'electron_config': '[Ne] 3s2 3p3', 'shells': [2, 8, 5]},
    'S': {'name': 'Sulfur', 'color': NONMETALS, 'atomic_number': 16, 'mass': 32.06, 'electron_config': '[Ne] 3s2 3p4', 'shells': [2, 8, 6]},
    'Se': {'name': 'Selenium', 'color': NONMETALS, 'atomic_number': 34, 'mass': 78.96, 'electron_config': '[Ar] 3d10 4s2 4p4', 'shells': [2, 8, 18, 6]},

    # Halogens
    'F': {'name': 'Fluorine', 'color': HALOGENS, 'atomic_number': 9, 'mass': 18.998, 'electron_config': '1s2 2s2 2p5', 'shells': [2, 7]},
    'Cl': {'name': 'Chlorine', 'color': HALOGENS, 'atomic_number': 17, 'mass': 35.45, 'electron_config': '[Ne] 3s2 3p5', 'shells': [2, 8, 7]},
    'Br': {'name': 'Bromine', 'color': HALOGENS, 'atomic_number': 35, 'mass': 79.904, 'electron_config': '[Ar] 3d10 4s2 4p5', 'shells': [2, 8, 18, 7]},
    'I': {'name': 'Iodine', 'color': HALOGENS, 'atomic_number': 53, 'mass': 126.90, 'electron_config': '[Kr] 4d10 5s2 5p5', 'shells': [2, 8, 18, 18, 7]},
    'At': {'name': 'Astatine', 'color': HALOGENS, 'atomic_number': 85, 'mass': 210, 'electron_config': '[Xe] 4f14 5d10 6s2 6p5', 'shells': [2, 8, 18, 32, 18, 7]},

    # Noble Gases
    'Ne': {'name': 'Neon', 'color': NOBLE_GASES, 'atomic_number': 10, 'mass': 20.180, 'electron_config': '1s2 2s2 2p6', 'shells': [2, 8]},
    'Ar': {'name': 'Argon', 'color': NOBLE_GASES, 'atomic_number': 18, 'mass': 39.948, 'electron_config': '[Ne] 3s2 3p6', 'shells': [2, 8, 8]},
    'Kr': {'name': 'Krypton', 'color': NOBLE_GASES, 'atomic_number': 36, 'mass': 83.798, 'electron_config': '[Ar] 3d10 4s2 4p6', 'shells': [2, 8, 18, 8]},
    'Xe': {'name': 'Xenon', 'color': NOBLE_GASES, 'atomic_number': 54, 'mass': 131.293, 'electron_config': '[Kr] 4d10 5s2 5p6', 'shells': [2, 8, 18, 18, 8]},
    'Rn': {'name': 'Radon', 'color': NOBLE_GASES, 'atomic_number': 86, 'mass': 222, 'electron_config': '[Xe] 4f14 5d10 6s2 6p6', 'shells': [2, 8, 18, 32, 18, 8]},

    # Lanthanides
    'La': {'name': 'Lanthanum', 'color': LANTHANIDES, 'atomic_number': 57, 'mass': 138.905, 'electron_config': '[Xe] 5d1 6s2', 'shells': [2, 8, 18, 18, 9, 2]},
    'Ce': {'name': 'Cerium', 'color': LANTHANIDES, 'atomic_number': 58, 'mass': 140.116, 'electron_config': '[Xe] 4f1 5d1 6s2', 'shells': [2, 8, 18, 19, 9, 2]},
    'Pr': {'name': 'Praseodymium', 'color': LANTHANIDES, 'atomic_number': 59, 'mass': 140.907, 'electron_config': '[Xe] 4f3 6s2', 'shells': [2, 8, 18, 21, 8, 2]},
    'Nd': {'name': 'Neodymium', 'color': LANTHANIDES, 'atomic_number': 60, 'mass': 144.242, 'electron_config': '[Xe] 4f4 6s2', 'shells': [2, 8, 18, 22, 8, 2]},
    'Pm': {'name': 'Promethium', 'color': LANTHANIDES, 'atomic_number': 61, 'mass': 145, 'electron_config': '[Xe] 4f5 6s2', 'shells': [2, 8, 18, 23, 8, 2]},
    'Sm': {'name': 'Samarium', 'color': LANTHANIDES, 'atomic_number': 62, 'mass': 150.36, 'electron_config': '[Xe] 4f6 6s2', 'shells': [2, 8, 18, 24, 8, 2]},
    'Eu': {'name': 'Europium', 'color': LANTHANIDES, 'atomic_number': 63, 'mass': 151.964, 'electron_config': '[Xe] 4f7 6s2', 'shells': [2, 8, 18, 25, 8, 2]},
    'Gd': {'name': 'Gadolinium', 'color': LANTHANIDES, 'atomic_number': 64, 'mass': 157.25, 'electron_config': '[Xe] 4f7 5d1 6s2', 'shells': [2, 8, 18, 25, 9, 2]},
    'Tb': {'name': 'Terbium', 'color': LANTHANIDES, 'atomic_number': 65, 'mass': 158.925, 'electron_config': '[Xe] 4f9 6s2', 'shells': [2, 8, 18, 27, 8, 2]},
    'Dy': {'name': 'Dysprosium', 'color': LANTHANIDES, 'atomic_number': 66, 'mass': 162.500, 'electron_config': '[Xe] 4f10 6s2', 'shells': [2, 8, 18, 28, 8, 2]},
    'Ho': {'name': 'Holmium', 'color': LANTHANIDES, 'atomic_number': 67, 'mass': 164.930, 'electron_config': '[Xe] 4f11 6s2', 'shells': [2, 8, 18, 29, 8, 2]},
    'Er': {'name': 'Erbium', 'color': LANTHANIDES, 'atomic_number': 68, 'mass': 167.259, 'electron_config': '[Xe] 4f12 6s2', 'shells': [2, 8, 18, 30, 8, 2]},
    'Tm': {'name': 'Thulium', 'color': LANTHANIDES, 'atomic_number': 69, 'mass': 168.934, 'electron_config': '[Xe] 4f13 6s2', 'shells': [2, 8, 18, 31, 8, 2]},
    'Yb': {'name': 'Ytterbium', 'color': LANTHANIDES, 'atomic_number': 70, 'mass': 173.04, 'electron_config': '[Xe] 4f14 6s2', 'shells': [2, 8, 18, 32, 8, 2]},
    'Lu': {'name': 'Lutetium', 'color': LANTHANIDES, 'atomic_number': 71, 'mass': 174.966, 'electron_config': '[Xe] 4f14 5d1 6s2', 'shells': [2, 8, 18, 32, 9, 2]},

    # Actinides
    'Th': {'name': 'Thorium', 'color': ACTINIDES, 'atomic_number': 90, 'mass': 232.038, 'electron_config': '[Rn] 6d2 7s2', 'shells': [2, 8, 18, 32, 18, 10, 2]},
    'Pa': {'name': 'Protactinium', 'color': ACTINIDES, 'atomic_number': 91, 'mass': 231.035, 'electron_config': '[Rn] 5f2 6d1 7s2', 'shells': [2, 8, 18, 32, 20, 9, 2]},
    'U': {'name': 'Uranium', 'color': ACTINIDES, 'atomic_number': 92, 'mass': 238.029, 'electron_config': '[Rn] 5f3 6d1 7s2', 'shells': [2, 8, 18, 32, 21, 9, 2]},
    'Np': {'name': 'Neptunium', 'color': ACTINIDES, 'atomic_number': 93, 'mass': 237, 'electron_config': '[Rn] 5f4 6d1 7s2', 'shells': [2, 8, 18, 32, 22, 9, 2]},
    'Pu': {'name': 'Plutonium', 'color': ACTINIDES, 'atomic_number': 94, 'mass': 244, 'electron_config': '[Rn] 5f6 7s2', 'shells': [2, 8, 18, 32, 24, 8, 2]},
    'Am': {'name': 'Americium', 'color': ACTINIDES, 'atomic_number': 95, 'mass': 243, 'electron_config': '[Rn] 5f7 7s2', 'shells': [2, 8, 18, 32, 25, 8, 2]},
    'Cm': {'name': 'Curium', 'color': ACTINIDES, 'atomic_number': 96, 'mass': 247, 'electron_config': '[Rn] 5f7 6d1 7s2', 'shells': [2, 8, 18, 32, 25, 9, 2]},
    'Bk': {'name': 'Berkelium', 'color': ACTINIDES, 'atomic_number': 97, 'mass': 247, 'electron_config': '[Rn] 5f9 7s2', 'shells': [2, 8, 18, 32, 27, 8, 2]},
    'Cf': {'name': 'Californium', 'color': ACTINIDES, 'atomic_number': 98, 'mass': 251, 'electron_config': '[Rn] 5f10 7s2', 'shells': [2, 8, 18, 32, 28, 8, 2]},
    'Es': {'name': 'Einsteinium', 'color': ACTINIDES, 'atomic_number': 99, 'mass': 252, 'electron_config': '[Rn] 5f11 7s2', 'shells': [2, 8, 18, 32, 29, 8, 2]},
    'Fm': {'name': 'Fermium', 'color': ACTINIDES, 'atomic_number': 100, 'mass': 257, 'electron_config': '[Rn] 5f12 7s2', 'shells': [2, 8, 18, 32, 30, 8, 2]},
    'Md': {'name': 'Mendelevium', 'color': ACTINIDES, 'atomic_number': 101, 'mass': 258, 'electron_config': '[Rn] 5f13 7s2', 'shells': [2, 8, 18, 32, 31, 8, 2]},
    'No': {'name': 'Nobelium', 'color': ACTINIDES, 'atomic_number': 102, 'mass': 259, 'electron_config': '[Rn] 5f14 7s2', 'shells': [2, 8, 18, 32, 32, 8, 2]},
    'Lr': {'name': 'Lawrencium', 'color': ACTINIDES, 'atomic_number': 103, 'mass': 262, 'electron_config': '[Rn] 5f14 7s2 7p1', 'shells': [2, 8, 18, 32, 32, 8, 3]},
}


# Define compounds
COMPOUNDS = {
    'H2O': {'elements': ['H', 'H', 'O'], 'name': 'Water', 'uses': 'Essential for life, solvent', 'properties': 'Colorless, odorless liquid'},
    'CO2': {'elements': ['C', 'O', 'O'], 'name': 'Carbon Dioxide', 'uses': 'Carbonated drinks, plant photosynthesis', 'properties': 'Colorless gas, soluble in water'},
    'NaCl': {'elements': ['Na', 'Cl'], 'name': 'Sodium Chloride', 'uses': 'Table salt, food preservative', 'properties': 'White crystalline solid, soluble in water'},
    'CH4': {'elements': ['C', 'H', 'H', 'H', 'H'], 'name': 'Methane', 'uses': 'Natural gas, fuel', 'properties': 'Colorless, odorless gas'},
    'NH3': {'elements': ['N', 'H', 'H', 'H'], 'name': 'Ammonia', 'uses': 'Fertilizer, cleaner', 'properties': 'Colorless gas with a strong odor'},
    'C6H12O6': {'elements': ['C', 'H', 'O', 'C', 'H', 'O', 'C', 'H', 'O', 'C', 'H', 'O', 'C', 'H', 'O'], 'name': 'Glucose', 'uses': 'Energy source in cells', 'properties': 'White crystalline solid, soluble in water'},
    'H2SO4': {'elements': ['H', 'H', 'S', 'O', 'O', 'O', 'O'], 'name': 'Sulfuric Acid', 'uses': 'Manufacturing, battery acid', 'properties': 'Colorless, oily liquid, very corrosive'},
    'C2H5OH': {'elements': ['C', 'H', 'H', 'H', 'H', 'H', 'C', 'H', 'O', 'H'], 'name': 'Ethanol', 'uses': 'Alcoholic beverages, solvent, fuel', 'properties': 'Colorless, volatile liquid with a distinctive odor'},
    'CaCO3': {'elements': ['Ca', 'C', 'O', 'O', 'O'], 'name': 'Calcium Carbonate', 'uses': 'Antacid, construction', 'properties': 'White, insoluble solid'},
    'NaOH': {'elements': ['Na', 'O', 'H'], 'name': 'Sodium Hydroxide', 'uses': 'Soap making, drain cleaner', 'properties': 'White solid, very corrosive'},
    'HCl': {'elements': ['H', 'Cl'], 'name': 'Hydrochloric Acid', 'uses': 'Stomach acid, industrial applications', 'properties': 'Colorless to light yellow liquid, highly corrosive'},
    'KNO3': {'elements': ['K', 'N', 'O', 'O', 'O'], 'name': 'Potassium Nitrate', 'uses': 'Fertilizer, food preservation', 'properties': 'White crystalline solid, soluble in water'},
    'NaHCO3': {'elements': ['Na', 'H', 'C', 'O', 'O', 'O'], 'name': 'Sodium Bicarbonate', 'uses': 'Baking soda, antacid', 'properties': 'White crystalline solid, soluble in water'},
    'H2O2': {'elements': ['H', 'H', 'O', 'O'], 'name': 'Hydrogen Peroxide', 'uses': 'Disinfectant, bleaching agent', 'properties': 'Colorless liquid, unstable'},
    'CaSO4': {'elements': ['Ca', 'S', 'O', 'O', 'O', 'O'], 'name': 'Calcium Sulfate', 'uses': 'Plaster, construction', 'properties': 'White crystalline solid, slightly soluble in water'},
    'HNO3': {'elements': ['H', 'N', 'O', 'O', 'O'], 'name': 'Nitric Acid', 'uses': 'Fertilizer production, explosives', 'properties': 'Colorless to yellowish liquid, highly corrosive'},
    'C12H22O11': {'elements': ['C', 'H', 'O'], 'name': 'Sucrose', 'uses': 'Table sugar, food sweetener', 'properties': 'White crystalline solid, soluble in water'},
    'CH3OH': {'elements': ['C', 'H', 'H', 'H', 'O', 'H'], 'name': 'Methanol', 'uses': 'Solvent, antifreeze, fuel', 'properties': 'Colorless, volatile liquid, poisonous'},
    'C2H4': {'elements': ['C', 'H', 'H', 'C', 'H', 'H'], 'name': 'Ethylene', 'uses': 'Plastic production, ripening agent', 'properties': 'Colorless gas, sweet odor'},
    'C3H8': {'elements': ['C', 'H', 'H', 'H', 'C', 'H', 'H', 'H', 'C', 'H', 'H', 'H'], 'name': 'Propane', 'uses': 'Fuel, heating', 'properties': 'Colorless, odorless gas'},
    'C4H10': {'elements': ['C', 'H', 'H', 'H', 'C', 'H', 'H', 'H', 'C', 'H', 'H', 'H', 'C', 'H', 'H', 'H'], 'name': 'Butane', 'uses': 'Fuel, lighter fluid', 'properties': 'Colorless, odorless gas'},
    'C2H2': {'elements': ['C', 'H', 'C', 'H'], 'name': 'Acetylene', 'uses': 'Welding, chemical synthesis', 'properties': 'Colorless gas, sweet odor'},
    'C6H6': {'elements': ['C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H'], 'name': 'Benzene', 'uses': 'Solvent, precursor in chemical synthesis', 'properties': 'Colorless liquid, sweet odor, carcinogenic'},
    'C3H6O': {'elements': ['C', 'H', 'H', 'H', 'C', 'H', 'H', 'O', 'C', 'H', 'H', 'H'], 'name': 'Acetone', 'uses': 'Solvent, nail polish remover', 'properties': 'Colorless liquid, sweet odor'},
    'C7H8': {'elements': ['C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H'], 'name': 'Toluene', 'uses': 'Solvent, paint thinner', 'properties': 'Colorless liquid, sweet odor'},
    'H2S': {'elements': ['H', 'H', 'S'], 'name': 'Hydrogen Sulfide', 'uses': 'Chemical precursor, produced by bacteria', 'properties': 'Colorless gas, rotten egg smell, toxic'},
    'HBr': {'elements': ['H', 'Br'], 'name': 'Hydrobromic Acid', 'uses': 'Chemical synthesis, catalyst', 'properties': 'Colorless to pale yellow liquid, highly corrosive'},
    'HI': {'elements': ['H', 'I'], 'name': 'Hydroiodic Acid', 'uses': 'Chemical synthesis, catalyst', 'properties': 'Colorless liquid, highly corrosive'},
    'HF': {'elements': ['H', 'F'], 'name': 'Hydrofluoric Acid', 'uses': 'Glass etching, chemical synthesis', 'properties': 'Colorless liquid, highly corrosive'},
    'SO2': {'elements': ['S', 'O', 'O'], 'name': 'Sulfur Dioxide', 'uses': 'Preservative, bleaching agent', 'properties': 'Colorless gas, pungent odor'},
    'SO3': {'elements': ['S', 'O', 'O', 'O'], 'name': 'Sulfur Trioxide', 'uses': 'Sulfuric acid production', 'properties': 'Colorless liquid, very corrosive'},
    'NO2': {'elements': ['N', 'O', 'O'], 'name': 'Nitrogen Dioxide', 'uses': 'Pollutant, used in chemical synthesis', 'properties': 'Brown gas, pungent odor'},
    'N2O': {'elements': ['N', 'N', 'O'], 'name': 'Nitrous Oxide', 'uses': 'Anesthetic, fuel oxidizer', 'properties': 'Colorless gas, slightly sweet odor'},
    'N2H4': {'elements': ['N', 'N', 'H', 'H', 'H', 'H'], 'name': 'Hydrazine', 'uses': 'Rocket propellant, chemical synthesis', 'properties': 'Colorless liquid, toxic'},
    'H2CO3': {'elements': ['H', 'H', 'C', 'O', 'O', 'O'], 'name': 'Carbonic Acid', 'uses': 'Soda production, buffer', 'properties': 'Weak acid, found in carbonated beverages'},
    'H3PO4': {'elements': ['H', 'H', 'H', 'P', 'O', 'O', 'O', 'O'], 'name': 'Phosphoric Acid', 'uses': 'Fertilizers, food additive', 'properties': 'Colorless liquid, mildly acidic'},
    'Na2CO3': {'elements': ['Na', 'Na', 'C', 'O', 'O', 'O'], 'name': 'Sodium Carbonate', 'uses': 'Glass making, water softening', 'properties': 'White crystalline solid, soluble in water'},
    'K2CO3': {'elements': ['K', 'K', 'C', 'O', 'O', 'O'], 'name': 'Potassium Carbonate', 'uses': 'Soap making, glass production', 'properties': 'White crystalline solid, soluble in water'},
    'CaCl2': {'elements': ['Ca', 'Cl', 'Cl'], 'name': 'Calcium Chloride', 'uses': 'De-icing, food additive', 'properties': 'White crystalline solid, soluble in water'},
    'NaClO': {'elements': ['Na', 'Cl', 'O'], 'name': 'Sodium Hypochlorite', 'uses': 'Bleach, disinfectant', 'properties': 'Colorless to pale green liquid, strong oxidizer'},
    'CaClO2': {'elements': ['Ca', 'Cl', 'O', 'O'], 'name': 'Calcium Hypochlorite', 'uses': 'Water treatment, bleaching agent', 'properties': 'White crystalline solid, strong oxidizer'},
    'MgSO4': {'elements': ['Mg', 'S', 'O', 'O', 'O', 'O'], 'name': 'Magnesium Sulfate', 'uses': 'Laxative, Epsom salts', 'properties': 'White crystalline solid, soluble in water'},
    'ZnSO4': {'elements': ['Zn', 'S', 'O', 'O', 'O', 'O'], 'name': 'Zinc Sulfate', 'uses': 'Dietary supplement, industrial applications', 'properties': 'White crystalline solid, soluble in water'},
    'CuSO4': {'elements': ['Cu', 'S', 'O', 'O', 'O', 'O'], 'name': 'Copper Sulfate', 'uses': 'Fungicide, algicide', 'properties': 'Blue crystalline solid, soluble in water'},
    'FeSO4': {'elements': ['Fe', 'S', 'O', 'O', 'O', 'O'], 'name': 'Iron(II) Sulfate', 'uses': 'Dietary supplement, industrial applications', 'properties': 'Green crystalline solid, soluble in water'},
    'H2C2O4': {'elements': ['H', 'H', 'C', 'C', 'O', 'O', 'O', 'O'], 'name': 'Oxalic Acid', 'uses': 'Cleaning agent, bleaching agent', 'properties': 'Colorless crystalline solid, soluble in water'},
    'Na2SO4': {'elements': ['Na', 'Na', 'S', 'O', 'O', 'O', 'O'], 'name': 'Sodium Sulfate', 'uses': 'Detergent manufacturing, paper production', 'properties': 'White crystalline solid, soluble in water'},
    'Na2S2O3': {'elements': ['Na', 'Na', 'S', 'S', 'O', 'O', 'O'], 'name': 'Sodium Thiosulfate', 'uses': 'Photographic fixer, dechlorination', 'properties': 'White crystalline solid, soluble in water'},
    'PbSO4': {'elements': ['Pb', 'S', 'O', 'O', 'O', 'O'], 'name': 'Lead(II) Sulfate', 'uses': 'Battery production', 'properties': 'White crystalline solid, slightly soluble in water'},
    'BaSO4': {'elements': ['Ba', 'S', 'O', 'O', 'O', 'O'], 'name': 'Barium Sulfate', 'uses': 'Radiocontrast agent, pigment', 'properties': 'White crystalline solid, insoluble in water'},
    'KOH': {'elements': ['K', 'O', 'H'], 'name': 'Potassium Hydroxide', 'uses': 'Soap making, electrolyte in batteries', 'properties': 'White solid, very corrosive'},
    'Mg(OH)2': {'elements': ['Mg', 'O', 'H', 'O', 'H'], 'name': 'Magnesium Hydroxide', 'uses': 'Antacid, laxative', 'properties': 'White solid, insoluble in water'},
    'Al(OH)3': {'elements': ['Al', 'O', 'H', 'O', 'H', 'O', 'H'], 'name': 'Aluminum Hydroxide', 'uses': 'Antacid, fire retardant', 'properties': 'White solid, insoluble in water'},
    'Fe(OH)3': {'elements': ['Fe', 'O', 'H', 'O', 'H', 'O', 'H'], 'name': 'Iron(III) Hydroxide', 'uses': 'Pigment, water purification', 'properties': 'Brown solid, insoluble in water'},
    'Cu(OH)2': {'elements': ['Cu', 'O', 'H', 'O', 'H'], 'name': 'Copper(II) Hydroxide', 'uses': 'Fungicide, pigment', 'properties': 'Blue solid, insoluble in water'},
    'NaNO3': {'elements': ['Na', 'N', 'O', 'O', 'O'], 'name': 'Sodium Nitrate', 'uses': 'Fertilizer, food preservative', 'properties': 'White crystalline solid, soluble in water'},
    'KNO3': {'elements': ['K', 'N', 'O', 'O', 'O'], 'name': 'Potassium Nitrate', 'uses': 'Fertilizer, food preservation', 'properties': 'White crystalline solid, soluble in water'},
    'AgNO3': {'elements': ['Ag', 'N', 'O', 'O', 'O'], 'name': 'Silver Nitrate', 'uses': 'Antiseptic, photographic film', 'properties': 'Colorless crystalline solid, soluble in water'},
    'NH4NO3': {'elements': ['N', 'H', 'H', 'H', 'H', 'N', 'O', 'O', 'O'], 'name': 'Ammonium Nitrate', 'uses': 'Fertilizer, explosive', 'properties': 'White crystalline solid, highly soluble in water'},
    'Ca(NO3)2': {'elements': ['Ca', 'N', 'O', 'O', 'O', 'N', 'O', 'O', 'O'], 'name': 'Calcium Nitrate', 'uses': 'Fertilizer, concrete additive', 'properties': 'White crystalline solid, highly soluble in water'},
    'Mg(NO3)2': {'elements': ['Mg', 'N', 'O', 'O', 'O', 'N', 'O', 'O', 'O'], 'name': 'Magnesium Nitrate', 'uses': 'Fertilizer, dehydrating agent', 'properties': 'White crystalline solid, soluble in water'},
    'Pb(NO3)2': {'elements': ['Pb', 'N', 'O', 'O', 'O', 'N', 'O', 'O', 'O'], 'name': 'Lead(II) Nitrate', 'uses': 'Heat stabilizer, pyrotechnics', 'properties': 'White crystalline solid, soluble in water'},
    'Na3PO4': {'elements': ['Na', 'Na', 'Na', 'P', 'O', 'O', 'O', 'O'], 'name': 'Trisodium Phosphate', 'uses': 'Cleaning agent, food additive', 'properties': 'White crystalline solid, soluble in water'},
    'K3PO4': {'elements': ['K', 'K', 'K', 'P', 'O', 'O', 'O', 'O'], 'name': 'Tripotassium Phosphate', 'uses': 'Food additive, water softening', 'properties': 'White crystalline solid, soluble in water'},
    'Ca3(PO4)2': {'elements': ['Ca', 'Ca', 'Ca', 'P', 'O', 'O', 'O', 'O', 'P', 'O', 'O', 'O', 'O'], 'name': 'Calcium Phosphate', 'uses': 'Fertilizer, food additive', 'properties': 'White crystalline solid, insoluble in water'},
    'Mg3(PO4)2': {'elements': ['Mg', 'Mg', 'Mg', 'P', 'O', 'O', 'O', 'O', 'P', 'O', 'O', 'O', 'O'], 'name': 'Magnesium Phosphate', 'uses': 'Fertilizer, food additive', 'properties': 'White crystalline solid, insoluble in water'},
    'AlPO4': {'elements': ['Al', 'P', 'O', 'O', 'O', 'O'], 'name': 'Aluminum Phosphate', 'uses': 'Antacid, dental cement', 'properties': 'White crystalline solid, insoluble in water'},
    'Na3PO4': {'elements': ['Na', 'Na', 'Na', 'P', 'O', 'O', 'O', 'O'], 'name': 'Trisodium Phosphate', 'uses': 'Cleaning agent, food additive', 'properties': 'White crystalline solid, soluble in water'},
    'Na2HPO4': {'elements': ['Na', 'Na', 'H', 'P', 'O', 'O', 'O', 'O'], 'name': 'Disodium Phosphate', 'uses': 'Food additive, buffering agent', 'properties': 'White crystalline solid, soluble in water'},
    'NaH2PO4': {'elements': ['Na', 'H', 'H', 'P', 'O', 'O', 'O', 'O'], 'name': 'Monosodium Phosphate', 'uses': 'Food additive, buffering agent', 'properties': 'White crystalline solid, soluble in water'},
    'K2HPO4': {'elements': ['K', 'K', 'H', 'P', 'O', 'O', 'O', 'O'], 'name': 'Dipotassium Phosphate', 'uses': 'Food additive, buffering agent', 'properties': 'White crystalline solid, soluble in water'},
    'KH2PO4': {'elements': ['K', 'H', 'H', 'P', 'O', 'O', 'O', 'O'], 'name': 'Monopotassium Phosphate', 'uses': 'Food additive, buffering agent', 'properties': 'White crystalline solid, soluble in water'},
    'Na2SiO3': {'elements': ['Na', 'Na', 'Si', 'O', 'O', 'O'], 'name': 'Sodium Silicate', 'uses': 'Adhesive, cement additive', 'properties': 'White crystalline solid, soluble in water'},
    'K2SiO3': {'elements': ['K', 'K', 'Si', 'O', 'O', 'O'], 'name': 'Potassium Silicate', 'uses': 'Adhesive, cement additive', 'properties': 'White crystalline solid, soluble in water'},
    'CaSiO3': {'elements': ['Ca', 'Si', 'O', 'O', 'O'], 'name': 'Calcium Silicate', 'uses': 'Cement additive, insulation material', 'properties': 'White crystalline solid, insoluble in water'},
    'MgSiO3': {'elements': ['Mg', 'Si', 'O', 'O', 'O'], 'name': 'Magnesium Silicate', 'uses': 'Talc, cosmetics', 'properties': 'White crystalline solid, insoluble in water'},
    'Al2SiO5': {'elements': ['Al', 'Al', 'Si', 'O', 'O', 'O', 'O', 'O', 'O'], 'name': 'Aluminum Silicate', 'uses': 'Ceramics, refractory material', 'properties': 'White crystalline solid, insoluble in water'},
    'SiO2': {'elements': ['Si', 'O', 'O'], 'name': 'Silicon Dioxide', 'uses': 'Glass making, abrasives', 'properties': 'White crystalline solid, insoluble in water'},
    'Fe2O3': {'elements': ['Fe', 'Fe', 'O', 'O', 'O'], 'name': 'Iron(III) Oxide', 'uses': 'Pigment, iron production', 'properties': 'Red-brown solid, insoluble in water'},
    'Fe3O4': {'elements': ['Fe', 'Fe', 'Fe', 'O', 'O', 'O', 'O'], 'name': 'Magnetite', 'uses': 'Magnetic storage, iron production', 'properties': 'Black solid, insoluble in water'},
    'Al2O3': {'elements': ['Al', 'Al', 'O', 'O', 'O'], 'name': 'Aluminum Oxide', 'uses': 'Abrasives, refractory material', 'properties': 'White solid, insoluble in water'},
    'CaO': {'elements': ['Ca', 'O'], 'name': 'Calcium Oxide', 'uses': 'Cement, lime', 'properties': 'White solid, soluble in water'},
    'MgO': {'elements': ['Mg', 'O'], 'name': 'Magnesium Oxide', 'uses': 'Refractory material, antacid', 'properties': 'White solid, soluble in water'},
    'CuO': {'elements': ['Cu', 'O'], 'name': 'Copper(II) Oxide', 'uses': 'Pigment, catalyst', 'properties': 'Black solid, insoluble in water'},
    'ZnO': {'elements': ['Zn', 'O'], 'name': 'Zinc Oxide', 'uses': 'Sunscreen, pigment', 'properties': 'White solid, insoluble in water'},
    'PbO': {'elements': ['Pb', 'O'], 'name': 'Lead(II) Oxide', 'uses': 'Battery production, glass making', 'properties': 'Yellow solid, insoluble in water'},
    'HgO': {'elements': ['Hg', 'O'], 'name': 'Mercury(II) Oxide', 'uses': 'Medicinal use, pigment', 'properties': 'Red or yellow solid, insoluble in water'},
    'Ca(OH)2': {'elements': ['Ca', 'O', 'H', 'O', 'H'], 'name': 'Calcium Hydroxide', 'uses': 'Water treatment, plaster', 'properties': 'White solid, slightly soluble in water'},
    'KOH': {'elements': ['K', 'O', 'H'], 'name': 'Potassium Hydroxide', 'uses': 'Soap making, electrolyte in batteries', 'properties': 'White solid, very corrosive'},
    'NaOH': {'elements': ['Na', 'O', 'H'], 'name': 'Sodium Hydroxide', 'uses': 'Soap making, drain cleaner', 'properties': 'White solid, very corrosive'},
    'Mg(OH)2': {'elements': ['Mg', 'O', 'H', 'O', 'H'], 'name': 'Magnesium Hydroxide', 'uses': 'Antacid, laxative', 'properties': 'White solid, insoluble in water'},
    'Al(OH)3': {'elements': ['Al', 'O', 'H', 'O', 'H', 'O', 'H'], 'name': 'Aluminum Hydroxide', 'uses': 'Antacid, fire retardant', 'properties': 'White solid, insoluble in water'},
    'Fe(OH)3': {'elements': ['Fe', 'O', 'H', 'O', 'H', 'O', 'H'], 'name': 'Iron(III) Hydroxide', 'uses': 'Pigment, water purification', 'properties': 'Brown solid, insoluble in water'},
    'Cu(OH)2': {'elements': ['Cu', 'O', 'H', 'O', 'H'], 'name': 'Copper(II) Hydroxide', 'uses': 'Fungicide, pigment', 'properties': 'Blue solid, insoluble in water'},
}



# Define the layout of the periodic table
PERIODIC_TABLE_LAYOUT = [
    ['H', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'He'],
    ['Li', 'Be', '', '', '', '', '', '', '', '', '', '', 'B', 'C', 'N', 'O', 'F', 'Ne'],
    ['Na', 'Mg', '', '', '', '', '', '', '', '', '', '', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar'],
    ['K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'],
    ['Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe'],
    ['Cs', 'Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'],
    ['Fr', 'Ra', 'Ac', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'],
    ['', '', '*', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '#', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '*La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', ''],
    ['', '', '#Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', '']
]

def draw_element(element, x, y, angle=0):
    # If angle is 0 (no rotation)
    if angle == 0:
        # Check if the element exists and is in the ELEMENTS dictionary
        if element and element in ELEMENTS:
            # Create a rectangle for the element
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            # Draw the element's background color
            pygame.draw.rect(screen, ELEMENTS[element]['color'], rect)
            # Draw a black border around the element
            pygame.draw.rect(screen, BLACK, rect, 1)

            # Render the element's symbol
            symbol = element_font.render(element, True, ELEMENT_FONT_COLOR)
            # Center the symbol in the element's rectangle
            symbol_rect = symbol.get_rect(center=\
                                        (x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            # Draw the symbol on the screen
            screen.blit(symbol, symbol_rect)
    
def draw_periodic_table():
    # Iterate through each row in the PERIOD_TABLE_LAYOUT
    for row, elements in enumerate(PERIODIC_TABLE_LAYOUT):
        # Iterate through each element in the row
        for col, element in enumerate(elements):
            # Calculate the x position of the element
            x = col * (CELL_SIZE + GRID_PADDING) + GRID_PADDING + TABLE_OFFSET_X
            # Calculate the y position of the element
            y = row * (CELL_SIZE + GRID_PADDING) + GRID_PADDING
            # Draw the element at the calculated position
            draw_element(element, x, y)

def draw_electron_shells(element, x, y, width, height):
    # Get the electron shell configuration for the element
    shells = ELEMENT[element]['shells']
    # Calculate the center of the drawing area
    center_x, center_y = x + width // 2, y + height // 2
    # Iterate through each shell
    for i, electrons in enumerate(shells):
        # Calculate the radius for this shell
        radius = (i + 1) * (min(width, height)) // (2 * len(shells))
        # Draw the shell circle
        pygame.draw.circle(screen, WHITE, (center_x, center_y), radius, 1)
        # Calculate the angle step between electrons
        angle_step = 360 / electrons
        # Draw each electron in the shell
        for j in range(electrons):
            # Calculate the angle for this electron
            angle = math.radians(j * angle_step)
            # Calculate the x position of the electron
            ex = center_x + int(radius * math.cos(angle))
            # Calculate the y position of the electron
            ey = center_y + int(radius * math.sin(angle))
            # Draw the electron
            pygame.draw.circle(screen, WHITE, (ex, ey), 2)


def create_tooltip(element):
    # Get the information for the given element from the ELEMENTS dictionary
    info = ELEMENTS[element]
    # Create the tooltip text, which is just the name of the element
    tooltip_text = f"{info['name']}"
    # Render the tooltip text as a surface
    # Text color is (44, 44, 47) (#2c2c2f), background is (229, 229, 229)
    tooltip = font.render(tooltip_text, True, (44, 44, 47), (229, 229, 229))
    # Return the rendered tooltip surface
    return tooltip


def draw_tooltip(screen, tooltip, pos):
    # Draw the tooltip on the screen
    # Position is offset by 15 pixels right and down from the cursor position
    screen.blit(tooltip, (pos[0] + 15, pos[1] + 15))


def show_element_info(element):
    # Get the information for the given element from the ELEMENTS dictionary
    info = ELEMENTS[element]
    # Create a list of formatted strings with element information
    lines = [
        f"Name: {info['name']}",
        f"Atomic Number: {info['atomic_number']}",
        f"Mass: {info['mass']}",
        f"Electron Config: {info['electron_config']}"
    ]
    # Return the list of information lines
    return lines


def show_compound_info(compound):
    # Get the information for compound from the COMPOUNDS dictionary
    info = COMPOUNDS[compound]
    # Create a list of formatted strings with compound information
    lines = [
        f"Name: {info['name']}",
        f"Formula: {compound}",
        f"Uses: {info['uses']}",
        f"Properties: {info['properties']}"
    ]
    # Return the list of information lines
    return lines


def check_compound(elements):
    # Sort the input elements to ensure consistent ordering
    elements.sort()
    # Iterate through all known compounds
    for compound, data in COMPOUNDS.items():
        # Compare the sorted input elements with
        # the sorted elements of each compound
        if elements == sorted(data['elements']):
            # If a match is found, return the compound formula and name
            return compound, data['name']
    # If no match is found, return None for both compound and name
    return None, None


def show_popup(message, color):
    # Render the popup message with the specified color
    popup = popup_font.render(message, True, color)
    # Create a rectangle for the popup,
    # Centered horizontally and 260 pixels from the bottom
    popup_rect = popup.get_rect(center=(WIDTH // 2, HEIGHT - 260))
    # Draw the popup on the screen
    screen.blit(popup, popup_rect)
    # Update the display to show the popup
    pygame.display.flip()
    # Wait for 1.5 seconds (1500 milliseconds)
    pygame.time.wait(1500)


def get_element_at_pos(pos):
    # Unpack the x and y coordinates from the input position
    x, y = pos
    # Calculate the column, accounting for the table offset
    col = (x - TABLE_OFFSET_X) // (CELL_SIZE + GRID_PADDING)
    # Calculate the row
    row = y // (CELL_SIZE + GRID_PADDING)
    # Check if the calculated row and column are within the periodic table layout
    if 0 <= row < len(PERIODIC_TABLE_LAYOUT) and 0 <= col < len(PERIODIC_TABLE_LAYOUT[0]):
        # Return the element at the calculated position in the periodic table layout
        return PERIODIC_TABLE_LAYOUT[row][col]
    # Return None if the position is outside the periodic table
    return None

def main():
    # Create a clock object to control the game's frame rate
    clock = pygame.time.Clock()

    # Flag to indicate if an element is being dragged
    dragging = False

    # Store the currently dragged element
    dragged_element = None

    # List to store elements in the merge area
    merge_area = []

    # Define rectangles for various UI elements
    merge_area_rect = pygame.Rect(WIDTH - 200, HEIGHT - 150, 180, 100)
    electron_shell_rect = pygame.Rect(WIDTH - 200, HEIGHT - 260, 180, 100)
    # Electron shell visualization
    merge_button = pygame.Rect(WIDTH - 200, HEIGHT - 40, 180, 30)

    # List to store information about selected elements or compounds
    info_area = []

    # Store the tooltip to be displayed
    tooltip = None

    while True:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game if the window is closed
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if merge_button.collidepoint(event.pos):
                    # Check if a compound can be formed from elements in the merge area
                    compound, name = check_compound(merge_area)
                    if compound:
                        # Show a popup with the created compound
                        show_popup(f"Created {name} ({compound})", WHITE)
                        # Display information about the compound
                        info_area = show_compound_info(compound)
                    else:
                        # Show a popup if no compound can be formed
                        show_popup("No compound formed", RED)
                    # Clear the merge area
                    merge_area = []
                else:
                    # Check if an element was clicked
                    element = get_element_at_pos(event.pos)
                    if element and element in ELEMENTS:
                        # Start dragging the element
                        dragging = True
                        dragged_element = element
                        # Display information about the clicked element
                        info_area = show_element_info(element)
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    if merge_area_rect.collidepoint(event.pos) and dragged_element:
                        # Add the dragged element to the merge area if released there
                        merge_area.append(dragged_element)
                    else:
                        # Show a popup with the element name if released elsewhere
                        show_popup(f"{ELEMENTS[dragged_element]['name']}", WHITE)
                # Reset the dragged element
                dragged_element = None
                
            # Fill the screen with the background color
            screen.fill(BACKGROUND)
            # Draw the periodic table
            draw_periodic_table()

            # Draw the merge area
            pygame.draw.rect(screen, WHITE, merge_area_rect, 2)
            for i, elem in enumerate(merge_area):
                # Draw elements in the merge area
                draw_element(elem, merge_area_rect.x + 10 + i*40,\
                            merge_area_rect.y + 10)
            
            # Draw the electron shell visualization area
            pygame.draw.rect(screen, WHITE, electron_shell_rect, 2)
            if merge_area:
                # Draw electron shells for the last element in the merge area
                draw_electron_shells(merge_area[-1], \
                                    electron_shell_rect.x, electron_shell_rect.y,
                                    electron_shell_rect.width, \
                                    electron_shell_rect.height)
            
            # Draw the merge button
            pygame.draw.rect(screen, WHITE, merge_button)
            merge_text = font.render("Merge", True, BLACK)
            screen.blit(merge_text, (merge_button.x + 70, merge_button.y + 8))

            # Draw information area
            info_rect = pygame.Rect(10, HEIGHT - 150, 300, 140)
            for i, line in enumerate(info_area):
                # Render each line of information as white text
                info_text = font.render(line, True, WHITE)
                # DIsplay the text in the information area
                screen.blit(info_text, (info_rect.x, info_rect.y + i*30))
                
            # Handle tooltips
            mouse_pos = pygame.mouse.get_pos()
            # Get the element at the current mouse position
            hover_element = get_element_at_pos(mouse_pos)
            if hover_element and hover_element in ELEMENTS:
                # Create a tooltip for the hovered element
                tooltip = create_tooltip(hover_element)
            else:
                # Clear the tooltip if not hovering over an element
                tooltip = None
            
            if tooltip:
                # Draw the tooltip if one exists
                draw_tooltip(screen, tooltip, mouse_pos)
                
            # Draw dragged element
            if dragging and dragged_element:
                # Get the current mouse position
                x, y = pygame.mouse.get_pos()
                # Draw the dragged element at the moust position
                draw_element(dragged_element, x - \
                            CELL_SIZE // 2, y - CELL_SIZE // 2)
            
            # Update the display
            pygame.display.flip()
            # Control the frame rate
            clock.tick(60)


if __name__ == "__main__":
    main()

                