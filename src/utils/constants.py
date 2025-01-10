"""
Game constants and configuration values for D&D Command Line Adventure.
This module contains all the static game data and configuration values used throughout the game.
"""

# Game Settings
MAX_PLAYERS = 6
MIN_PLAYERS = 1
SAVE_FILE_NAME = "game_save.json"

# Character Creation
ABILITY_SCORES = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

# Character Races with their features
RACES = {
    'Dwarf': {
        'ability_bonuses': {'Constitution': 2},
        'speed': 25,
        'traits': ['Darkvision', 'Dwarven Resilience', 'Stonecunning'],
        'languages': ['Common', 'Dwarvish']
    },
    'Elf': {
        'ability_bonuses': {'Dexterity': 2},
        'speed': 30,
        'traits': ['Darkvision', 'Keen Senses', 'Fey Ancestry', 'Trance'],
        'languages': ['Common', 'Elvish']
    },
    'Halfling': {
        'ability_bonuses': {'Dexterity': 2},
        'speed': 25,
        'traits': ['Lucky', 'Brave', 'Halfling Nimbleness'],
        'languages': ['Common', 'Halfling']
    },
    'Human': {
        'ability_bonuses': {'Strength': 1, 'Dexterity': 1, 'Constitution': 1,
                          'Intelligence': 1, 'Wisdom': 1, 'Charisma': 1},
        'speed': 30,
        'traits': ['Versatile'],
        'languages': ['Common', 'Choice of one']
    }
}

# Difficulty Classes for skill checks
DIFFICULTY_CLASSES = {
    "Very Easy": 5,
    "Easy": 10,
    "Medium": 15,
    "Hard": 20,
    "Very Hard": 25,
    "Nearly Impossible": 30
}

# Combat System
COMBAT_ROUNDS = {
    'ACTION_TYPES': ['attack', 'cast', 'dash', 'disengage', 'dodge', 'help', 'hide', 'ready'],
    'BONUS_ACTIONS': ['offhand_attack', 'cunning_action', 'rage'],
    'REACTIONS': ['opportunity_attack', 'shield_spell', 'uncanny_dodge']
}

COMBAT_STATES = {
    'not_in_combat': 'Exploration mode',
    'in_combat': 'Combat mode',
    'surprised': 'Surprised',
    'ready': 'Ready for combat'
}

# Status Conditions
CONDITIONS = {
    'Blinded': {
        'effects': ['disadvantage on attacks', 'attackers have advantage'],
        'duration': 'varies'
    },
    'Charmed': {
        'effects': ['cannot attack charmer', 'charmer has advantage on social checks'],
        'duration': 'varies'
    },
    'Deafened': {
        'effects': ['cannot hear', 'fails checks requiring hearing'],
        'duration': 'varies'
    },
    'Frightened': {
        'effects': ['disadvantage while source in sight', 'cannot move closer'],
        'duration': 'varies'
    },
    'Grappled': {
        'effects': ['speed 0', 'condition ends if grappler incapacitated'],
        'duration': 'until escaped'
    },
    'Incapacitated': {
        'effects': ['cannot take actions or reactions'],
        'duration': 'varies'
    },
    'Invisible': {
        'effects': ['cannot be seen', 'advantage on attacks', 'attacks against have disadvantage'],
        'duration': 'varies'
    },
    'Paralyzed': {
        'effects': ['cannot move or speak', 'auto fail Str and Dex saves', 'attacks have advantage'],
        'duration': 'varies'
    },
    'Petrified': {
        'effects': ['transformed to stone', 'immune to damage', 'auto fail Str and Dex saves'],
        'duration': 'varies'
    },
    'Poisoned': {
        'effects': ['disadvantage on attacks and ability checks'],
        'duration': 'varies'
    },
    'Prone': {
        'effects': ['can only crawl', 'disadvantage on attacks', 'melee attacks have advantage'],
        'duration': 'until standing'
    },
    'Restrained': {
        'effects': ['speed 0', 'attacks have disadvantage', 'attacks against have advantage'],
        'duration': 'varies'
    },
    'Stunned': {
        'effects': ['incapacitated', 'auto fail Str and Dex saves', 'attacks have advantage'],
        'duration': 'varies'
    },
    'Unconscious': {
        'effects': ['incapacitated', 'drop everything', 'auto fail Str and Dex saves'],
        'duration': 'varies'
    }
}

# Time and Round Management
ROUND_LENGTH = 6  # seconds
TURNS_PER_ROUND = 1
ROUNDS_PER_MINUTE = 10
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24

TIME_PERIODS = {
    'Dawn': {'start': 6, 'end': 8},
    'Morning': {'start': 8, 'end': 12},
    'Afternoon': {'start': 12, 'end': 17},
    'Evening': {'start': 17, 'end': 20},
    'Night': {'start': 20, 'end': 6}
}

REST_PERIODS = {
    'Short Rest': {
        'duration': 1,  # hours
        'healing': 'Hit Dice',
        'ability_refresh': ['Some class features']
    },
    'Long Rest': {
        'duration': 8,  # hours
        'healing': 'Full HP',
        'ability_refresh': ['All class features', 'Half total Hit Dice']
    }
}

# Equipment - Weapons
WEAPONS = {
    'Simple Melee': {
        'Club': {'damage': '1d4', 'type': 'bludgeoning', 'properties': ['light']},
        'Dagger': {'damage': '1d4', 'type': 'piercing', 'properties': ['finesse', 'light', 'thrown']},
        'Greatclub': {'damage': '1d8', 'type': 'bludgeoning', 'properties': ['two-handed']},
        'Handaxe': {'damage': '1d6', 'type': 'slashing', 'properties': ['light', 'thrown']},
        'Javelin': {'damage': '1d6', 'type': 'piercing', 'properties': ['thrown']},
        'Light Hammer': {'damage': '1d4', 'type': 'bludgeoning', 'properties': ['light', 'thrown']},
        'Mace': {'damage': '1d6', 'type': 'bludgeoning', 'properties': []},
        'Quarterstaff': {'damage': '1d6', 'type': 'bludgeoning', 'properties': ['versatile']},
        'Sickle': {'damage': '1d4', 'type': 'slashing', 'properties': ['light']},
        'Spear': {'damage': '1d6', 'type': 'piercing', 'properties': ['thrown', 'versatile']}
    },
    'Simple Ranged': {
        'Light Crossbow': {'damage': '1d8', 'type': 'piercing', 'properties': ['ammunition', 'loading', 'two-handed']},
        'Dart': {'damage': '1d4', 'type': 'piercing', 'properties': ['finesse', 'thrown']},
        'Shortbow': {'damage': '1d6', 'type': 'piercing', 'properties': ['ammunition', 'two-handed']},
        'Sling': {'damage': '1d4', 'type': 'bludgeoning', 'properties': ['ammunition']}
    },
    'Martial Melee': {
        'Battleaxe': {'damage': '1d8', 'type': 'slashing', 'properties': ['versatile']},
        'Flail': {'damage': '1d8', 'type': 'bludgeoning', 'properties': []},
        'Glaive': {'damage': '1d10', 'type': 'slashing', 'properties': ['heavy', 'reach', 'two-handed']},
        'Greataxe': {'damage': '1d12', 'type': 'slashing', 'properties': ['heavy', 'two-handed']},
        'Greatsword': {'damage': '2d6', 'type': 'slashing', 'properties': ['heavy', 'two-handed']},
        'Longsword': {'damage': '1d8', 'type': 'slashing', 'properties': ['versatile']},
        'Rapier': {'damage': '1d8', 'type': 'piercing', 'properties': ['finesse']},
        'Scimitar': {'damage': '1d6', 'type': 'slashing', 'properties': ['finesse', 'light']}
    },
    'Martial Ranged': {
        'Heavy Crossbow': {'damage': '1d10', 'type': 'piercing', 'properties': ['ammunition', 'heavy', 'loading', 'two-handed']},
        'Longbow': {'damage': '1d8', 'type': 'piercing', 'properties': ['ammunition', 'heavy', 'two-handed']}
    }
}

# Equipment - Armor
ARMOR = {
    'Light': {
        'Padded': {'AC': 11, 'type': 'light', 'stealth': 'disadvantage'},
        'Leather': {'AC': 11, 'type': 'light'},
        'Studded Leather': {'AC': 12, 'type': 'light'}
    },
    'Medium': {
        'Hide': {'AC': 12, 'type': 'medium'},
        'Chain Shirt': {'AC': 13, 'type': 'medium'},
        'Scale Mail': {'AC': 14, 'type': 'medium', 'stealth': 'disadvantage'},
        'Breastplate': {'AC': 14, 'type': 'medium'},
        'Half Plate': {'AC': 15, 'type': 'medium', 'stealth': 'disadvantage'}
    },
    'Heavy': {
        'Ring Mail': {'AC': 14, 'type': 'heavy', 'stealth': 'disadvantage'},
        'Chain Mail': {'AC': 16, 'type': 'heavy', 'stealth': 'disadvantage', 'strength': 13},
        'Splint': {'AC': 17, 'type': 'heavy', 'stealth': 'disadvantage', 'strength': 15},
        'Plate': {'AC': 18, 'type': 'heavy', 'stealth': 'disadvantage', 'strength': 15}
    }
}

# Equipment Weight and Capacity
EQUIPMENT_WEIGHTS = {
    'coins': {
        'copper': 0.02,
        'silver': 0.02,
        'electrum': 0.02,
        'gold': 0.02,
        'platinum': 0.02
    },
    'basic_items': {
        'torch': 1,
        'rations': 2,
        'waterskin': 5,
        'rope': 10,
        'bedroll': 7
    }
}

CARRYING_CAPACITY = {
    'base_multiplier': 15,  # times Strength score
    'size_multipliers': {
        'Tiny': 0.5,
        'Small': 1,
        'Medium': 1,
        'Large': 2,
        'Huge': 4,
        'Gargantuan': 8
    },
    'push_drag_lift_multiplier': 2  # times normal carrying capacity
}

# Magic System - Spells
SPELLS = {
    'Wizard': {
        'cantrips': ['Fire Bolt', 'Mage Hand', 'Prestidigitation', 'Ray of Frost'],
        '1st': ['Magic Missile', 'Shield', 'Mage Armor', 'Sleep'],
        '2nd': ['Invisibility', 'Scorching Ray', 'Misty Step', 'Web']
    },
    'Cleric': {
        'cantrips': ['Sacred Flame', 'Spare the Dying', 'Thaumaturgy'],
        '1st': ['Cure Wounds', 'Healing Word', 'Bless', 'Shield of Faith'],
        '2nd': ['Lesser Restoration', 'Spiritual Weapon', 'Hold Person']
    },
    'Druid': {
        'cantrips': ['Druidcraft', 'Produce Flame', 'Shillelagh'],
        '1st': ['Entangle', 'Goodberry', 'Healing Word', 'Faerie Fire'],
        '2nd': ['Moonbeam', 'Heat Metal', 'Pass without Trace']
    }
}

# Starting Equipment by Class
CLASS_EQUIPMENT = {
    'Barbarian': {
        'weapons': ['Greataxe', 'Two Handaxes'],
        'armor': None,
        'other': ['Explorer\'s Pack', '4 Javelins']
    },
    'Bard': {
        'weapons': ['Rapier', 'Dagger'],
        'armor': 'Leather',
        'other': ['Diplomat\'s Pack', 'Musical Instrument']
    },
    'Cleric': {
        'weapons': ['Mace', 'Light Crossbow'],
        'armor': 'Scale Mail',
        'other': ['Priest\'s Pack', 'Shield', 'Holy Symbol']
    }
}

# Experience and Progression
XP_LEVELS = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000
}

# Experience and Progression
XP_LEVELS = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000
}

CHALLENGE_RATINGS = {
    0: {'xp': 10, 'proficiency': 2},
    0.125: {'xp': 25, 'proficiency': 2},
    0.25: {'xp': 50, 'proficiency': 2},
    0.5: {'xp': 100, 'proficiency': 2},
    1: {'xp': 200, 'proficiency': 2},
    2: {'xp': 450, 'proficiency': 2},
    3: {'xp': 700, 'proficiency': 2},
    4: {'xp': 1100, 'proficiency': 2},
    5: {'xp': 1800, 'proficiency': 3},
    6: {'xp': 2300, 'proficiency': 3},
    7: {'xp': 2900, 'proficiency': 3},
    8: {'xp': 3900, 'proficiency': 3},
    9: {'xp': 5000, 'proficiency': 4},
    10: {'xp': 5900, 'proficiency': 4}
}

# Environment and Weather
ENVIRONMENTS = {
    'Dungeon': {
        'features': ['corridors', 'rooms', 'traps', 'treasures'],
        'hazards': ['cave-ins', 'pit traps', 'poison gas'],
        'encounters': ['monsters', 'undead', 'cultists']
    },
    'Forest': {
        'features': ['trees', 'clearings', 'streams'],
        'hazards': ['quicksand', 'poisonous plants', 'falling trees'],
        'encounters': ['beasts', 'fey', 'bandits']
    },
    'Mountain': {
        'features': ['peaks', 'caves', 'cliffs'],
        'hazards': ['avalanches', 'thin air', 'falling'],
        'encounters': ['dragons', 'giants', 'griffons']
    },
    'Urban': {
        'features': ['buildings', 'streets', 'sewers'],
        'hazards': ['crowds', 'guards', 'thieves'],
        'encounters': ['criminals', 'nobles', 'cultists']
    },
    'Coastal': {
        'features': ['beaches', 'cliffs', 'caves'],
        'hazards': ['tides', 'storms', 'whirlpools'],
        'encounters': ['pirates', 'merfolk', 'sea monsters']
    },
    'Desert': {
        'features': ['dunes', 'oases', 'ruins'],
        'hazards': ['sandstorms', 'heat', 'dehydration'],
        'encounters': ['nomads', 'monstrous beasts', 'elementals']
    },
    'Underground': {
        'features': ['caverns', 'tunnels', 'underground rivers'],
        'hazards': ['cave-ins', 'toxic gases', 'getting lost'],
        'encounters': ['drow', 'aberrations', 'dwarves']
    }
}

WEATHER_CONDITIONS = {
    'Clear': {
        'visibility': 'excellent',
        'movement': 'normal',
        'effects': []
    },
    'Cloudy': {
        'visibility': 'good',
        'movement': 'normal',
        'effects': []
    },
    'Rain': {
        'visibility': 'limited',
        'movement': 'difficult',
        'effects': ['disadvantage on perception checks using sight']
    },
    'Storm': {
        'visibility': 'poor',
        'movement': 'very difficult',
        'effects': ['disadvantage on perception checks', 'disadvantage on ranged attacks']
    },
    'Fog': {
        'visibility': 'very poor',
        'movement': 'normal',
        'effects': ['heavily obscured beyond 60 feet']
    },
    'Snow': {
        'visibility': 'limited',
        'movement': 'difficult',
        'effects': ['cold damage possible', 'difficult terrain']
    },
    'Extreme Heat': {
        'visibility': 'normal',
        'movement': 'normal',
        'effects': ['constitution saves', 'exhaustion possible']
    }
}

# Game Economy
CURRENCY = {
    'exchange_rates': {
        'copper': {'copper': 1, 'silver': 0.1, 'gold': 0.01, 'platinum': 0.001},
        'silver': {'copper': 10, 'silver': 1, 'gold': 0.1, 'platinum': 0.01},
        'gold': {'copper': 100, 'silver': 10, 'gold': 1, 'platinum': 0.1},
        'platinum': {'copper': 1000, 'silver': 100, 'gold': 10, 'platinum': 1}
    },
    'starting_money': {
        'Barbarian': '2d4 x 10 gp',
        'Bard': '5d4 x 10 gp',
        'Cleric': '5d4 x 10 gp',
        'Druid': '2d4 x 10 gp',
        'Fighter': '5d4 x 10 gp',
        'Monk': '5d4 gp',
        'Paladin': '5d4 x 10 gp',
        'Ranger': '5d4 x 10 gp',
        'Rogue': '4d4 x 10 gp',
        'Sorcerer': '3d4 x 10 gp',
        'Warlock': '4d4 x 10 gp',
        'Wizard': '4d4 x 10 gp'
    }
}

ITEM_PRICES = {
    'Adventuring Gear': {
        'Backpack': '2 gp',
        'Bedroll': '1 gp',
        'Candle': '1 cp',
        'Torch': '1 cp',
        'Rations (1 day)': '5 sp',
        'Rope (50 feet)': '1 gp',
        'Waterskin': '2 sp'
    },
    'Tools': {
        'Alchemist\'s supplies': '50 gp',
        'Brewer\'s supplies': '20 gp',
        'Carpenter\'s tools': '8 gp',
        'Cartographer\'s tools': '15 gp',
        'Disguise kit': '25 gp',
        'Forgery kit': '15 gp',
        'Herbalism kit': '5 gp',
        'Navigator\'s tools': '25 gp',
        'Poisoner\'s kit': '50 gp',
        'Thieves\' tools': '25 gp'
    }
}

# Travel and Movement
TRAVEL_PACE = {
    'Fast': {
        'minute': 400,  # feet per minute
        'hour': 4,     # miles per hour
        'day': 30,     # miles per day
        'effect': '-5 penalty to passive Wisdom (Perception) scores'
    },
    'Normal': {
        'minute': 300,
        'hour': 3,
        'day': 24,
        'effect': None
    },
    'Slow': {
        'minute': 200,
        'hour': 2,
        'day': 18,
        'effect': 'Able to use stealth'
    }
}

ENCOUNTER_DISTANCES = {
    'Desert': {'min': 300, 'max': 600},  # feet
    'Forest': {'min': 100, 'max': 300},
    'Grassland': {'min': 200, 'max': 400},
    'Mountain': {'min': 200, 'max': 500},
    'Urban': {'min': 50, 'max': 150},
    'Underground': {'min': 30, 'max': 100}
}