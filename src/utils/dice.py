"""
Dice rolling utility class
"""
import random
from typing import Tuple, Dict, Union, List

class DiceRoller:
    @staticmethod
    def parse_dice_string(dice_str: str) -> Tuple[int, int]:
        """Parse a dice string (e.g., '2d6') into number of dice and sides"""
        try:
            num_dice, sides = map(int, dice_str.lower().split('d'))
            return num_dice, sides
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid dice notation: {dice_str}. Use format: NdM (e.g., 2d6)")

    def roll(self, dice_str: str) -> Tuple[int, List[int]]:
        """Roll dice based on standard D&D notation (e.g., '2d6', '1d20')"""
        num_dice, sides = self.parse_dice_string(dice_str)
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        return sum(rolls), rolls

    def ability_check(self, ability_score: int, proficiency: bool = False,
                     advantage: bool = False, disadvantage: bool = False) -> Dict[str, Union[int, bool, List[int]]]:
        """Perform a D&D ability check with modifiers"""
        modifier = (ability_score - 10) // 2
        prof_bonus = 2 if proficiency else 0  # Basic proficiency bonus

        if advantage and disadvantage:  # They cancel each other
            advantage = disadvantage = False

        if advantage or disadvantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            base_roll = max(roll1, roll2) if advantage else min(roll1, roll2)
            rolls = [roll1, roll2]
        else:
            base_roll = random.randint(1, 20)
            rolls = [base_roll]

        total = base_roll + modifier + prof_bonus

        return {
            'total': total,
            'base_roll': base_roll,
            'modifier': modifier,
            'proficiency': prof_bonus,
            'rolls': rolls,
            'critical_success': base_roll == 20,
            'critical_failure': base_roll == 1
        }

    def attack_roll(self, attack_bonus: int, advantage: bool = False,
                   disadvantage: bool = False) -> Dict[str, Union[int, bool, List[int]]]:
        """Perform an attack roll with modifiers"""
        if advantage and disadvantage:
            advantage = disadvantage = False

        if advantage or disadvantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            base_roll = max(roll1, roll2) if advantage else min(roll1, roll2)
            rolls = [roll1, roll2]
        else:
            base_roll = random.randint(1, 20)
            rolls = [base_roll]

        total = base_roll + attack_bonus

        return {
            'total': total,
            'base_roll': base_roll,
            'attack_bonus': attack_bonus,
            'rolls': rolls,
            'critical_hit': base_roll == 20,
            'critical_miss': base_roll == 1
        }

    def damage_roll(self, damage_dice: str, modifier: int = 0,
                   critical: bool = False) -> Dict[str, Union[int, List[int]]]:
        """Roll damage dice with optional critical hit"""
        num_dice, sides = self.parse_dice_string(damage_dice)

        if critical:
            num_dice *= 2

        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls) + modifier

        return {
            'total': total,
            'base_damage': sum(rolls),
            'modifier': modifier,
            'rolls': rolls,
            'critical': critical
        }

    def saving_throw(self, save_bonus: int, advantage: bool = False,
                    disadvantage: bool = False) -> Dict[str, Union[int, bool, List[int]]]:
        """Perform a saving throw with modifiers"""
        if advantage and disadvantage:
            advantage = disadvantage = False

        if advantage or disadvantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            base_roll = max(roll1, roll2) if advantage else min(roll1, roll2)
            rolls = [roll1, roll2]
        else:
            base_roll = random.randint(1, 20)
            rolls = [base_roll]

        total = base_roll + save_bonus

        return {
            'total': total,
            'base_roll': base_roll,
            'save_bonus': save_bonus,
            'rolls': rolls,
            'critical_success': base_roll == 20,
            'critical_failure': base_roll == 1
        }

    def initiative_roll(self, modifier: int = 0, advantage: bool = False) -> int:
        """Roll initiative with optional advantage and modifier"""
        if advantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            base_roll = max(roll1, roll2)
        else:
            base_roll = random.randint(1, 20)

        return base_roll + modifier