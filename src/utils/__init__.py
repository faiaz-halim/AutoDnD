"""
Utility functions and game constants
"""
from .dice import DiceRoller
from .text_formatter import TextFormatter
from .constants import (
    # Game Settings
    MAX_PLAYERS,
    MIN_PLAYERS,
    SAVE_FILE_NAME,
    ABILITY_SCORES,

    # Character Creation
    RACES,

    # Game Mechanics
    DIFFICULTY_CLASSES,
    COMBAT_ROUNDS,
    COMBAT_STATES,
    CONDITIONS,

    # Time Management
    ROUND_LENGTH,
    TURNS_PER_ROUND,
    ROUNDS_PER_MINUTE,
    MINUTES_PER_HOUR,
    HOURS_PER_DAY,
    TIME_PERIODS,
    REST_PERIODS,

    # Equipment
    WEAPONS,
    ARMOR,
    EQUIPMENT_WEIGHTS,
    CARRYING_CAPACITY,

    # Magic System
    SPELLS,

    # Character Classes
    CLASS_EQUIPMENT,

    # Progression
    XP_LEVELS,
    CHALLENGE_RATINGS,

    # Environment
    ENVIRONMENTS,
    WEATHER_CONDITIONS,

    # Game Economy
    CURRENCY,
    ITEM_PRICES,

    # Travel and Exploration
    TRAVEL_PACE,
    ENCOUNTER_DISTANCES
)

__all__ = [
    # Utility Classes
    'DiceRoller',
    'TextFormatter',

    # Game Settings
    'MAX_PLAYERS',
    'MIN_PLAYERS',
    'SAVE_FILE_NAME',
    'ABILITY_SCORES',
    'RACES',

    # Game Mechanics
    'DIFFICULTY_CLASSES',
    'COMBAT_ROUNDS',
    'COMBAT_STATES',
    'CONDITIONS',

    # Time Management
    'ROUND_LENGTH',
    'TURNS_PER_ROUND',
    'ROUNDS_PER_MINUTE',
    'MINUTES_PER_HOUR',
    'HOURS_PER_DAY',
    'TIME_PERIODS',
    'REST_PERIODS',

    # Equipment
    'WEAPONS',
    'ARMOR',
    'EQUIPMENT_WEIGHTS',
    'CARRYING_CAPACITY',

    # Magic
    'SPELLS',

    # Classes
    'CLASS_EQUIPMENT',

    # Progression
    'XP_LEVELS',
    'CHALLENGE_RATINGS',

    # Environment
    'ENVIRONMENTS',
    'WEATHER_CONDITIONS',

    # Economy
    'CURRENCY',
    'ITEM_PRICES',

    # Travel
    'TRAVEL_PACE',
    'ENCOUNTER_DISTANCES'
]