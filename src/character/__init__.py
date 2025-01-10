"""
Character creation and management system for D&D
"""
from .stats import generate_class_stats, calculate_hit_points, optimize_stats
from .classes import (
    CLASS_DESCRIPTIONS,
    CLASS_HIT_DICE,
    CLASS_SETUPS,
    CLASS_STARTING_EQUIPMENT,
    CLASS_FEATURES,
    CLASS_PRIMARY_ABILITIES,
    SPELLCASTING_ABILITIES,
    CharacterClass,
    SIMPLE_WEAPONS,
    MARTIAL_WEAPONS
)
from .proficiencies import (
    get_class_proficiencies,
    get_skill_ability,
    calculate_skill_bonus
)

__all__ = [
    # Stats
    'generate_class_stats',
    'calculate_hit_points',
    'optimize_stats',

    # Classes
    'CLASS_DESCRIPTIONS',
    'CLASS_HIT_DICE',
    'CLASS_SETUPS',
    'CLASS_STARTING_EQUIPMENT',
    'CLASS_FEATURES',
    'CLASS_PRIMARY_ABILITIES',
    'SPELLCASTING_ABILITIES',
    'CharacterClass',
    'SIMPLE_WEAPONS',
    'MARTIAL_WEAPONS',

    # Proficiencies
    'get_class_proficiencies',
    'get_skill_ability',
    'calculate_skill_bonus'
]