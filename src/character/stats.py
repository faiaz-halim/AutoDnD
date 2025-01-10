import random
from typing import Dict, List, Tuple
from .classes import CLASS_SETUPS, CLASS_HIT_DICE

def generate_ability_scores() -> Dict[str, int]:
    """Generate ability scores using 4d6 drop lowest method"""
    stats = {}
    abilities = ["strength", "dexterity", "constitution",
                "intelligence", "wisdom", "charisma"]

    for ability in abilities:
        rolls = sorted([random.randint(1, 6) for _ in range(4)])
        stats[ability] = sum(rolls[1:])  # Drop lowest roll

    return stats

def optimize_stats(stats: Dict[str, int], important_stats: List[str]) -> Dict[str, int]:
    """Optimize stats by swapping highest rolls to important stats"""
    # Get stats sorted by value
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    # Swap highest values to important stats if they're not already there
    for i, important_stat in enumerate(important_stats):
        if i >= len(sorted_stats):
            break
        if important_stat not in [stat for stat, _ in sorted_stats[:i+1]]:
            # Find the highest stat that's not in important_stats
            for high_stat, high_value in sorted_stats:
                if high_stat not in important_stats:
                    # Swap values
                    stats[important_stat], stats[high_stat] = stats[high_stat], stats[important_stat]
                    break

    return stats

def generate_class_stats(char_class: str) -> Tuple[Dict[str, int], Dict[str, Dict[str, bool]]]:
    """Generate stats and proficiencies for a given class"""
    # Generate base stats
    stats = generate_ability_scores()

    # Set up base proficiencies
    proficiencies = {
        'skills': {skill: False for skill in [
            "acrobatics", "animal_handling", "arcana", "athletics",
            "deception", "history", "insight", "intimidation",
            "investigation", "medicine", "nature", "perception",
            "performance", "persuasion", "religion", "sleight_of_hand",
            "stealth", "survival"
        ]},
        'saves': {save: False for save in [
            "strength", "dexterity", "constitution",
            "intelligence", "wisdom", "charisma"
        ]}
    }

    # Apply class-specific setups
    char_class = char_class.lower()
    if char_class in CLASS_SETUPS:
        setup = CLASS_SETUPS[char_class]

        # Set saving throw proficiencies
        for save in setup['saves']:
            proficiencies['saves'][save] = True

        # Set skill proficiencies
        for skill in setup['skills']:
            proficiencies['skills'][skill] = True

        # Optimize primary stats
        stats = optimize_stats(stats, setup['primary_stats'])

    return stats, proficiencies

def calculate_hit_points(char_class: str, constitution_mod: int) -> int:
    """Calculate starting hit points for a character"""
    hit_die = CLASS_HIT_DICE.get(char_class.lower(), 8)
    return hit_die + constitution_mod