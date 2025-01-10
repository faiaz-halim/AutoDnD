"""
Game settings and configuration
"""

# Game settings
MAX_PLAYERS = 6
MIN_PLAYERS = 1
SAVE_FILE_NAME = "game_save.json"

# D&D specific settings
CHARACTER_CLASSES = [
    "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
    "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer",
    "Warlock", "Wizard"
]

ABILITY_SCORES = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

# Dice settings
DICE_TYPES = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]

# Game difficulty settings
DIFFICULTY_CLASSES = {
    "Very Easy": 5,
    "Easy": 10,
    "Medium": 15,
    "Hard": 20,
    "Very Hard": 25,
    "Nearly Impossible": 30
}

# Combat settings
DEFAULT_INITIATIVE_DICE = "1d20"
DEFAULT_HP_DICE = {
    "Barbarian": "1d12",
    "Fighter": "1d10",
    "Paladin": "1d10",
    "Ranger": "1d10",
    "Bard": "1d8",
    "Cleric": "1d8",
    "Druid": "1d8",
    "Monk": "1d8",
    "Rogue": "1d8",
    "Warlock": "1d8",
    "Wizard": "1d6",
    "Sorcerer": "1d6"
}