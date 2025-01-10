"""
Class definitions and features for D&D characters
"""
from typing import Dict, List, Optional

# Class descriptions
CLASS_DESCRIPTIONS = {
    'Barbarian': 'Fierce warrior who can enter a battle rage, using fury and primal instincts to enhance combat abilities',
    'Bard': 'Magical entertainer who weaves magic through words and music, inspiring allies and confounding enemies',
    'Cleric': 'Divine spellcaster who wields the power of their deity, capable of healing and divine magic',
    'Druid': 'Nature mystic who can shapeshift and command elemental forces, wielding nature\'s magic',
    'Fighter': 'Skilled warrior and weapons master with exceptional combat abilities and tactical expertise',
    'Monk': 'Martial artist who harnesses the power of body and soul, mastering unarmed combat and inner energy',
    'Paladin': 'Holy warrior who channels divine authority into martial prowess, sworn to uphold sacred oaths',
    'Ranger': 'Wilderness survivor skilled in tracking, archery, and natural magic, master of terrain and stealth',
    'Rogue': 'Skilled adventurer specializing in stealth and precision strikes, expert in skills and sneak attacks',
    'Sorcerer': 'Spellcaster with innate magical abilities from their bloodline, wielding raw arcane power',
    'Warlock': 'Wielder of magic granted through a powerful otherworldly patron, mixing magic with cunning',
    'Wizard': 'Scholar of the arcane who learns magic through dedicated study, master of diverse spells'
}

# Hit dice by class
CLASS_HIT_DICE = {
    'barbarian': 12,
    'fighter': 10,
    'paladin': 10,
    'ranger': 10,
    'bard': 8,
    'cleric': 8,
    'druid': 8,
    'monk': 8,
    'rogue': 8,
    'warlock': 8,
    'sorcerer': 6,
    'wizard': 6
}

# Class setups for character creation
CLASS_SETUPS = {
    'barbarian': {
        'saves': ['strength', 'constitution'],
        'skills': ['athletics', 'intimidation', 'survival', 'nature'],
        'primary_stats': ['strength', 'constitution']
    },
    'bard': {
        'saves': ['dexterity', 'charisma'],
        'skills': ['performance', 'persuasion', 'deception', 'insight'],
        'primary_stats': ['charisma', 'dexterity']
    },
    'cleric': {
        'saves': ['wisdom', 'charisma'],
        'skills': ['religion', 'medicine', 'insight', 'persuasion'],
        'primary_stats': ['wisdom', 'constitution']
    },
    'druid': {
        'saves': ['intelligence', 'wisdom'],
        'skills': ['nature', 'animal_handling', 'survival', 'medicine'],
        'primary_stats': ['wisdom', 'constitution']
    },
    'fighter': {
        'saves': ['strength', 'constitution'],
        'skills': ['athletics', 'intimidation', 'acrobatics', 'survival'],
        'primary_stats': ['strength', 'constitution']
    },
    'monk': {
        'saves': ['strength', 'dexterity'],
        'skills': ['acrobatics', 'athletics', 'stealth', 'insight'],
        'primary_stats': ['dexterity', 'wisdom']
    },
    'paladin': {
        'saves': ['wisdom', 'charisma'],
        'skills': ['religion', 'persuasion', 'intimidation', 'medicine'],
        'primary_stats': ['strength', 'charisma']
    },
    'ranger': {
        'saves': ['strength', 'dexterity'],
        'skills': ['nature', 'survival', 'stealth', 'animal_handling'],
        'primary_stats': ['dexterity', 'wisdom']
    },
    'rogue': {
        'saves': ['dexterity', 'intelligence'],
        'skills': ['stealth', 'sleight_of_hand', 'acrobatics', 'deception'],
        'primary_stats': ['dexterity', 'charisma']
    },
    'sorcerer': {
        'saves': ['constitution', 'charisma'],
        'skills': ['arcana', 'deception', 'insight', 'persuasion'],
        'primary_stats': ['charisma', 'constitution']
    },
    'warlock': {
        'saves': ['wisdom', 'charisma'],
        'skills': ['arcana', 'deception', 'intimidation', 'nature'],
        'primary_stats': ['charisma', 'constitution']
    },
    'wizard': {
        'saves': ['intelligence', 'wisdom'],
        'skills': ['arcana', 'history', 'investigation', 'medicine'],
        'primary_stats': ['intelligence', 'constitution']
    }
}

# Update the CLASS_STARTING_EQUIPMENT dictionary to include all classes
CLASS_STARTING_EQUIPMENT = {
    'Barbarian': {
        'weapons': ['Greataxe', 'Two Handaxes'],
        'armor': None,
        'items': ['Explorer\'s Pack', 'Four javelins'],
        'choices': [
            {'type': 'weapon', 'options': ['Greataxe', 'Any martial melee weapon'], 'quantity': 1},
            {'type': 'weapon', 'options': ['Two handaxes', 'Any simple weapon'], 'quantity': 1}
        ]
    },
    'Bard': {
        'weapons': ['Rapier', 'Dagger'],
        'armor': 'Leather',
        'items': ['Diplomat\'s Pack', 'Musical instrument'],
        'choices': [
            {'type': 'weapon', 'options': ['Rapier', 'Longsword', 'Any simple weapon'], 'quantity': 1},
            {'type': 'item', 'options': ['Diplomat\'s pack', 'Entertainer\'s pack'], 'quantity': 1}
        ]
    },
    'Cleric': {
        'weapons': ['Mace', 'Shield'],
        'armor': 'Scale mail',
        'items': ['Priest\'s Pack', 'Holy Symbol'],
        'choices': [
            {'type': 'weapon', 'options': ['Mace', 'Warhammer'], 'quantity': 1},
            {'type': 'armor', 'options': ['Scale mail', 'Leather armor', 'Chain mail'], 'quantity': 1}
        ]
    },
    'Druid': {
        'weapons': ['Scimitar', 'Wooden Shield'],
        'armor': 'Leather',
        'items': ['Explorer\'s Pack', 'Druidic focus'],
        'choices': [
            {'type': 'weapon', 'options': ['Scimitar', 'Any simple melee weapon'], 'quantity': 1},
            {'type': 'item', 'options': ['Wooden shield', 'Any simple weapon'], 'quantity': 1}
        ]
    },
    'Fighter': {
        'weapons': ['Longsword', 'Shield', 'Light Crossbow'],
        'armor': 'Chain mail',
        'items': ['Dungeoneer\'s Pack', '20 bolts'],
        'choices': [
            {'type': 'armor', 'options': ['Chain mail', 'Leather armor, longbow, and 20 arrows'], 'quantity': 1},
            {'type': 'weapon', 'options': ['Any martial weapon', 'Two martial weapons'], 'quantity': 1},
            {'type': 'item', 'options': ['Dungeoneer\'s pack', 'Explorer\'s pack'], 'quantity': 1}
        ]
    },
    'Monk': {
        'weapons': ['Shortsword', 'Ten darts'],
        'armor': None,
        'items': ['Explorer\'s Pack'],
        'choices': [
            {'type': 'weapon', 'options': ['Shortsword', 'Any simple weapon'], 'quantity': 1},
            {'type': 'item', 'options': ['Dungeoneer\'s pack', 'Explorer\'s pack'], 'quantity': 1}
        ]
    },
    'Paladin': {
        'weapons': ['Longsword', 'Shield', 'Five javelins'],
        'armor': 'Chain mail',
        'items': ['Priest\'s Pack', 'Holy Symbol'],
        'choices': [
            {'type': 'weapon', 'options': ['Any martial weapon', 'Two martial weapons'], 'quantity': 1},
            {'type': 'item', 'options': ['Priest\'s pack', 'Explorer\'s pack'], 'quantity': 1}
        ]
    },
    'Ranger': {
        'weapons': ['Longbow', 'Two shortswords'],
        'armor': 'Scale mail',
        'items': ['Explorer\'s Pack', 'Quiver with 20 arrows'],
        'choices': [
            {'type': 'armor', 'options': ['Scale mail', 'Leather armor'], 'quantity': 1},
            {'type': 'weapon', 'options': ['Two shortswords', 'Two simple melee weapons'], 'quantity': 1}
        ]
    },
    'Rogue': {
        'weapons': ['Rapier', 'Shortbow'],
        'armor': 'Leather',
        'items': ['Burglar\'s Pack', 'Thieves\' tools', 'Quiver with 20 arrows'],
        'choices': [
            {'type': 'weapon', 'options': ['Rapier', 'Shortsword'], 'quantity': 1},
            {'type': 'item', 'options': ['Burglar\'s pack', 'Dungeoneer\'s pack', 'Explorer\'s pack'], 'quantity': 1}
        ]
    },
    'Sorcerer': {
        'weapons': ['Light crossbow', 'Dagger'],
        'armor': None,
        'items': ['Explorer\'s Pack', 'Arcane focus', '20 bolts'],
        'choices': [
            {'type': 'weapon', 'options': ['Light crossbow', 'Any simple weapon'], 'quantity': 1},
            {'type': 'item', 'options': ['Component pouch', 'Arcane focus'], 'quantity': 1}
        ]
    },
    'Warlock': {
        'weapons': ['Light crossbow', 'Any simple weapon'],
        'armor': 'Leather',
        'items': ['Scholar\'s Pack', 'Arcane focus', '20 bolts'],
        'choices': [
            {'type': 'weapon', 'options': ['Light crossbow', 'Any simple weapon'], 'quantity': 1},
            {'type': 'item', 'options': ['Component pouch', 'Arcane focus'], 'quantity': 1},
            {'type': 'item', 'options': ['Scholar\'s pack', 'Dungeoneer\'s pack'], 'quantity': 1}
        ]
    },
    'Wizard': {
        'weapons': ['Quarterstaff', 'Dagger'],
        'armor': None,
        'items': ['Scholar\'s Pack', 'Spellbook', 'Arcane focus'],
        'choices': [
            {'type': 'weapon', 'options': ['Quarterstaff', 'Dagger'], 'quantity': 1},
            {'type': 'item', 'options': ['Component pouch', 'Arcane focus'], 'quantity': 1},
            {'type': 'pack', 'options': ['Scholar\'s pack', 'Explorer\'s pack'], 'quantity': 1}
        ]
    }
}

# Update the CLASS_FEATURES dictionary to include all classes
CLASS_FEATURES = {
    'Barbarian': {
        1: ['Rage', 'Unarmored Defense'],
        2: ['Reckless Attack', 'Danger Sense'],
        3: ['Primal Path', 'Path Feature']
    },
    'Bard': {
        1: ['Spellcasting', 'Bardic Inspiration'],
        2: ['Jack of All Trades', 'Song of Rest'],
        3: ['Bard College', 'Expertise']
    },
    'Cleric': {
        1: ['Spellcasting', 'Divine Domain'],
        2: ['Channel Divinity', 'Divine Domain Feature'],
        3: ['Divine Domain Feature']
    },
    'Druid': {
        1: ['Druidic', 'Spellcasting'],
        2: ['Wild Shape', 'Druid Circle'],
        3: ['Circle Feature']
    },
    'Fighter': {
        1: ['Fighting Style', 'Second Wind'],
        2: ['Action Surge'],
        3: ['Martial Archetype']
    },
    'Monk': {
        1: ['Unarmored Defense', 'Martial Arts'],
        2: ['Ki', 'Unarmored Movement'],
        3: ['Monastic Tradition', 'Deflect Missiles']
    },
    'Paladin': {
        1: ['Divine Sense', 'Lay on Hands'],
        2: ['Fighting Style', 'Divine Smite', 'Spellcasting'],
        3: ['Divine Health', 'Sacred Oath']
    },
    'Ranger': {
        1: ['Favored Enemy', 'Natural Explorer'],
        2: ['Fighting Style', 'Spellcasting'],
        3: ['Ranger Archetype', 'Primeval Awareness']
    },
    'Rogue': {
        1: ['Expertise', 'Sneak Attack', 'Thieves\' Cant'],
        2: ['Cunning Action'],
        3: ['Roguish Archetype']
    },
    'Sorcerer': {
        1: ['Spellcasting', 'Sorcerous Origin'],
        2: ['Font of Magic'],
        3: ['Metamagic']
    },
    'Warlock': {
        1: ['Otherworldly Patron', 'Pact Magic'],
        2: ['Eldritch Invocations'],
        3: ['Pact Boon']
    },
    'Wizard': {
        1: ['Spellcasting', 'Arcane Recovery'],
        2: ['Arcane Tradition'],
        3: ['Tradition Feature']
    }
}

# Primary abilities for each class
CLASS_PRIMARY_ABILITIES = {
    'Barbarian': ['Strength', 'Constitution'],
    'Bard': ['Charisma', 'Dexterity'],
    'Cleric': ['Wisdom', 'Constitution'],
    'Druid': ['Wisdom', 'Constitution'],
    'Fighter': ['Strength', 'Constitution'],
    'Monk': ['Dexterity', 'Wisdom'],
    'Paladin': ['Strength', 'Charisma'],
    'Ranger': ['Dexterity', 'Wisdom'],
    'Rogue': ['Dexterity', 'Intelligence'],
    'Sorcerer': ['Charisma', 'Constitution'],
    'Warlock': ['Charisma', 'Constitution'],
    'Wizard': ['Intelligence', 'Constitution']
}

# Spellcasting abilities for spellcasting classes
SPELLCASTING_ABILITIES = {
    'Bard': 'Charisma',
    'Cleric': 'Wisdom',
    'Druid': 'Wisdom',
    'Paladin': 'Charisma',
    'Ranger': 'Wisdom',
    'Sorcerer': 'Charisma',
    'Warlock': 'Charisma',
    'Wizard': 'Intelligence'
}

class CharacterClass:
    """Class representing a D&D character class and its features"""

    def __init__(self, class_name: str):
        """Initialize a character class"""
        self.name = class_name
        self.description = CLASS_DESCRIPTIONS.get(class_name, "No description available")
        self.hit_die = CLASS_HIT_DICE.get(class_name.lower(), 8)
        self.primary_abilities = CLASS_PRIMARY_ABILITIES.get(class_name, [])
        self.spellcasting_ability = SPELLCASTING_ABILITIES.get(class_name)
        self.features = CLASS_FEATURES.get(class_name, {})
        self.starting_equipment = CLASS_STARTING_EQUIPMENT.get(class_name, {})

    def get_features_by_level(self, level: int) -> List[str]:
        """Get class features available at a specific level"""
        features = []
        for lvl in range(1, level + 1):
            features.extend(self.features.get(lvl, []))
        return features

    def get_spellcasting_modifier(self, ability_scores: Dict[str, int]) -> Optional[int]:
        """Calculate spellcasting modifier based on the class's spellcasting ability"""
        if not self.spellcasting_ability:
            return None

        ability_score = ability_scores.get(self.spellcasting_ability.lower(), 10)
        return (ability_score - 10) // 2

    def can_use_armor(self, armor_type: str) -> bool:
        """Check if the class can use a specific type of armor"""
        armor_restrictions = {
            'Barbarian': ['light', 'medium', 'shields'],
            'Bard': ['light', 'medium', 'shields'],
            'Cleric': ['light', 'medium', 'heavy', 'shields'],
            'Druid': ['light', 'medium', 'shields'],
            'Fighter': ['light', 'medium', 'heavy', 'shields'],
            'Monk': ['none'],
            'Paladin': ['light', 'medium', 'heavy', 'shields'],
            'Ranger': ['light', 'medium', 'shields'],
            'Rogue': ['light'],
            'Sorcerer': ['none'],
            'Warlock': ['light'],
            'Wizard': ['none']
        }

        allowed_armor = armor_restrictions.get(self.name, [])
        return armor_type.lower() in allowed_armor

    def can_use_weapon(self, weapon_type: str) -> bool:
        """Check if the class can use a specific type of weapon"""
        weapon_restrictions = {
            'Barbarian': ['simple', 'martial'],
            'Bard': ['simple', 'hand crossbow', 'longsword', 'rapier', 'shortsword'],
            'Cleric': ['simple'],
            'Druid': ['club', 'dagger', 'dart', 'javelin', 'mace', 'quarterstaff', 'scimitar', 'sickle', 'sling', 'spear'],
            'Fighter': ['simple', 'martial'],
            'Monk': ['simple', 'shortsword'],
            'Paladin': ['simple', 'martial'],
            'Ranger': ['simple', 'martial'],
            'Rogue': ['simple', 'hand crossbow', 'longsword', 'rapier', 'shortsword'],
            'Sorcerer': ['dagger', 'dart', 'sling', 'quarterstaff', 'light crossbow'],
            'Warlock': ['simple'],
            'Wizard': ['dagger', 'dart', 'sling', 'quarterstaff', 'light crossbow']
        }

        allowed_weapons = weapon_restrictions.get(self.name, [])
        weapon_type = weapon_type.lower()

        return (weapon_type in allowed_weapons or
                ('simple' in allowed_weapons and weapon_type in SIMPLE_WEAPONS) or
                ('martial' in allowed_weapons and weapon_type in MARTIAL_WEAPONS))

# Define weapon categories
SIMPLE_WEAPONS = {
    'club', 'dagger', 'greatclub', 'handaxe', 'javelin', 'light hammer', 'mace',
    'quarterstaff', 'sickle', 'spear', 'light crossbow', 'dart', 'shortbow', 'sling'
}

MARTIAL_WEAPONS = {
    'battleaxe', 'flail', 'glaive', 'greataxe', 'greatsword', 'halberd', 'lance',
    'longsword', 'maul', 'morningstar', 'pike', 'rapier', 'scimitar', 'shortsword',
    'trident', 'war pick', 'warhammer', 'whip', 'blowgun', 'hand crossbow',
    'heavy crossbow', 'longbow', 'net'
}