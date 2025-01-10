"""
Character proficiency management
"""
from typing import Dict, List, Set

# Default skill list
SKILLS = {
    "acrobatics": "dexterity",
    "animal_handling": "wisdom",
    "arcana": "intelligence",
    "athletics": "strength",
    "deception": "charisma",
    "history": "intelligence",
    "insight": "wisdom",
    "intimidation": "charisma",
    "investigation": "intelligence",
    "medicine": "wisdom",
    "nature": "intelligence",
    "perception": "wisdom",
    "performance": "charisma",
    "persuasion": "charisma",
    "religion": "intelligence",
    "sleight_of_hand": "dexterity",
    "stealth": "dexterity",
    "survival": "wisdom"
}

# Class skill proficiencies
CLASS_SKILLS = {
    'barbarian': {
        'num_choices': 2,
        'options': ['animal_handling', 'athletics', 'intimidation', 'nature', 'perception', 'survival']
    },
    'bard': {
        'num_choices': 3,
        'options': list(SKILLS.keys())  # Bards can choose any skill
    },
    'cleric': {
        'num_choices': 2,
        'options': ['history', 'insight', 'medicine', 'persuasion', 'religion']
    },
    'druid': {
        'num_choices': 2,
        'options': ['arcana', 'animal_handling', 'insight', 'medicine', 'nature', 'perception', 'religion', 'survival']
    },
    'fighter': {
        'num_choices': 2,
        'options': ['acrobatics', 'animal_handling', 'athletics', 'history', 'insight', 'intimidation', 'perception', 'survival']
    },
    'monk': {
        'num_choices': 2,
        'options': ['acrobatics', 'athletics', 'history', 'insight', 'religion', 'stealth']
    },
    'paladin': {
        'num_choices': 2,
        'options': ['athletics', 'insight', 'intimidation', 'medicine', 'persuasion', 'religion']
    },
    'ranger': {
        'num_choices': 3,
        'options': ['animal_handling', 'athletics', 'insight', 'investigation', 'nature', 'perception', 'stealth', 'survival']
    },
    'rogue': {
        'num_choices': 4,
        'options': ['acrobatics', 'athletics', 'deception', 'insight', 'intimidation', 'investigation', 'perception',
                    'performance', 'persuasion', 'sleight_of_hand', 'stealth']
    },
    'sorcerer': {
        'num_choices': 2,
        'options': ['arcana', 'deception', 'insight', 'intimidation', 'persuasion', 'religion']
    },
    'warlock': {
        'num_choices': 2,
        'options': ['arcana', 'deception', 'history', 'intimidation', 'investigation', 'nature', 'religion']
    },
    'wizard': {
        'num_choices': 2,
        'options': ['arcana', 'history', 'insight', 'investigation', 'medicine', 'religion']
    }
}

# Saving throw proficiencies by class
CLASS_SAVES = {
    'barbarian': ['strength', 'constitution'],
    'bard': ['dexterity', 'charisma'],
    'cleric': ['wisdom', 'charisma'],
    'druid': ['intelligence', 'wisdom'],
    'fighter': ['strength', 'constitution'],
    'monk': ['strength', 'dexterity'],
    'paladin': ['wisdom', 'charisma'],
    'ranger': ['strength', 'dexterity'],
    'rogue': ['dexterity', 'intelligence'],
    'sorcerer': ['constitution', 'charisma'],
    'warlock': ['wisdom', 'charisma'],
    'wizard': ['intelligence', 'wisdom']
}

def get_class_proficiencies(char_class: str) -> Dict[str, Dict[str, bool]]:
    """
    Get default proficiencies for a character class

    Args:
        char_class (str): Character class name

    Returns:
        Dict containing skill and saving throw proficiencies
    """
    char_class = char_class.lower()

    # Initialize all skills as not proficient
    skills = {skill: False for skill in SKILLS.keys()}
    saves = {save: False for save in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']}

    # Set saving throw proficiencies
    if char_class in CLASS_SAVES:
        for save in CLASS_SAVES[char_class]:
            saves[save] = True

    # Get random skill proficiencies based on class options
    if char_class in CLASS_SKILLS:
        import random
        class_skills = CLASS_SKILLS[char_class]
        num_choices = class_skills['num_choices']
        options = class_skills['options']

        # Select random skills from options
        chosen_skills = random.sample(options, min(num_choices, len(options)))
        for skill in chosen_skills:
            skills[skill] = True

    return {
        'skills': skills,
        'saves': saves
    }

def get_skill_ability(skill: str) -> str:
    """Get the ability score associated with a skill"""
    return SKILLS.get(skill.lower(), 'dexterity')

def calculate_skill_bonus(skill: str, ability_modifier: int, proficient: bool, prof_bonus: int) -> int:
    """Calculate total bonus for a skill check"""
    return ability_modifier + (prof_bonus if proficient else 0)