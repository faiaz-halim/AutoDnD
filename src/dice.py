import random
from typing import Tuple, Dict, Union, List
from .text_formatter import TextFormatter as Fmt

class DiceRoller:
    @staticmethod
    def roll(dice_str: str) -> Tuple[int, list]:
        """Roll dice based on standard D&D notation (e.g., '2d6', '1d20')"""
        try:
            num_dice, sides = map(int, dice_str.lower().split('d'))
            rolls = [random.randint(1, sides) for _ in range(num_dice)]
            return sum(rolls), rolls
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid dice notation: {dice_str}. Use format: NdM (e.g., 2d6)")

    def ability_check(self, ability_score: int, proficiency: bool = False,
                     advantage: bool = False, disadvantage: bool = False) -> Dict[str, Union[int, bool, List[int]]]:
        """
        Perform a D&D ability check with modifiers
        Returns dict with roll details
        """
        modifier = (ability_score - 10) // 2
        prof_bonus = 2 if proficiency else 0  # Basic proficiency bonus

        if advantage and disadvantage:
            advantage = disadvantage = False

        rolls = []
        if advantage or disadvantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            rolls = [roll1, roll2]
            base_roll = max(roll1, roll2) if advantage else min(roll1, roll2)
        else:
            base_roll = random.randint(1, 20)
            rolls = [base_roll]

        total = base_roll + modifier + prof_bonus

        result = {
            'total': total,
            'base_roll': base_roll,
            'modifier': modifier,
            'proficiency': prof_bonus,
            'rolls': rolls,
            'critical_success': base_roll == 20,
            'critical_failure': base_roll == 1
        }

        roll_text = f"d20 roll{'s' if len(rolls) > 1 else ''}: {rolls}"
        if modifier != 0:
            roll_text += f" {'+' if modifier > 0 else ''}{modifier} (ability modifier)"
        if prof_bonus != 0:
            roll_text += f" +{prof_bonus} (proficiency)"
        roll_text += f" = {total}"

        print(Fmt.dice_roll(roll_text))

        return result

    def attack_roll(self, attack_bonus: int, advantage: bool = False,
                   disadvantage: bool = False) -> Dict[str, Union[int, bool, List[int]]]:
        """Perform an attack roll with modifiers"""
        if advantage and disadvantage:
            advantage = disadvantage = False

        rolls = []
        if advantage or disadvantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            rolls = [roll1, roll2]
            base_roll = max(roll1, roll2) if advantage else min(roll1, roll2)
        else:
            base_roll = random.randint(1, 20)
            rolls = [base_roll]

        total = base_roll + attack_bonus

        result = {
            'total': total,
            'base_roll': base_roll,
            'attack_bonus': attack_bonus,
            'rolls': rolls,
            'critical_hit': base_roll == 20,
            'critical_miss': base_roll == 1
        }

        roll_text = f"Attack roll{'s' if len(rolls) > 1 else ''}: {rolls}"
        if attack_bonus != 0:
            roll_text += f" {'+' if attack_bonus > 0 else ''}{attack_bonus} (attack bonus)"
        roll_text += f" = {total}"

        print(Fmt.dice_roll(roll_text))

        return result

    def damage_roll(self, damage_dice: str, modifier: int = 0, critical: bool = False) -> Dict[str, Union[int, List[int]]]:
        """
        Roll damage dice with optional critical hit
        If critical, rolls dice twice
        """
        try:
            num_dice, sides = map(int, damage_dice.lower().split('d'))
            if critical:
                num_dice *= 2

            rolls = [random.randint(1, sides) for _ in range(num_dice)]
            total = sum(rolls) + modifier

            result = {
                'total': total,
                'base_damage': sum(rolls),
                'modifier': modifier,
                'rolls': rolls,
                'critical': critical
            }

            roll_text = f"Damage roll: {rolls}"
            if modifier != 0:
                roll_text += f" {'+' if modifier > 0 else ''}{modifier} (modifier)"
            roll_text += f" = {total}"

            print(Fmt.dice_roll(roll_text))

            return result

        except (ValueError, AttributeError):
            raise ValueError(f"Invalid damage dice: {damage_dice}")

    def skill_check(self, skill_bonus: int, advantage: bool = False,
                   disadvantage: bool = False) -> Dict[str, Union[int, bool, List[int]]]:
        """Perform a skill check with modifiers"""
        if advantage and disadvantage:
            advantage = disadvantage = False

        rolls = []
        if advantage or disadvantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            rolls = [roll1, roll2]
            base_roll = max(roll1, roll2) if advantage else min(roll1, roll2)
        else:
            base_roll = random.randint(1, 20)
            rolls = [base_roll]

        total = base_roll + skill_bonus

        result = {
            'total': total,
            'base_roll': base_roll,
            'skill_bonus': skill_bonus,
            'rolls': rolls,
            'critical_success': base_roll == 20,
            'critical_failure': base_roll == 1
        }

        roll_text = f"Skill check{'s' if len(rolls) > 1 else ''}: {rolls}"
        if skill_bonus != 0:
            roll_text += f" {'+' if skill_bonus > 0 else ''}{skill_bonus} (skill bonus)"
        roll_text += f" = {total}"

        print(Fmt.dice_roll(roll_text))

        return result

    def saving_throw(self, save_bonus: int, advantage: bool = False,
                    disadvantage: bool = False) -> Dict[str, Union[int, bool, List[int]]]:
        """Perform a saving throw with modifiers"""
        if advantage and disadvantage:
            advantage = disadvantage = False

        rolls = []
        if advantage or disadvantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            rolls = [roll1, roll2]
            base_roll = max(roll1, roll2) if advantage else min(roll1, roll2)
        else:
            base_roll = random.randint(1, 20)
            rolls = [base_roll]

        total = base_roll + save_bonus

        result = {
            'total': total,
            'base_roll': base_roll,
            'save_bonus': save_bonus,
            'rolls': rolls,
            'critical_success': base_roll == 20,
            'critical_failure': base_roll == 1
        }

        roll_text = f"Saving throw{'s' if len(rolls) > 1 else ''}: {rolls}"
        if save_bonus != 0:
            roll_text += f" {'+' if save_bonus > 0 else ''}{save_bonus} (save bonus)"
        roll_text += f" = {total}"

        print(Fmt.dice_roll(roll_text))

        return result