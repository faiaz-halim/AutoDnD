"""
Combat action handling and resolution
"""
from typing import Dict, Tuple, Optional
from ..game_state import Player
from ..utils.dice import DiceRoller

class CombatHandler:
    def __init__(self):
        self.dice = DiceRoller()

    def handle_combat_action(self, actor: Player, target: str, action: str) -> Tuple[str, Dict]:
        """Process a combat action and return results"""
        action_type = self._determine_action_type(action)

        if action_type == 'attack':
            return self._handle_attack(actor, target, action)
        elif action_type == 'spell':
            return self._handle_spell(actor, target, action)
        elif action_type == 'special':
            return self._handle_special_ability(actor, target, action)

        return "Invalid action", {}

    def _determine_action_type(self, action: str) -> str:
        """Determine the type of combat action"""
        action_lower = action.lower()

        if any(word in action_lower for word in ['attack', 'strike', 'slash', 'shoot']):
            return 'attack'
        elif any(word in action_lower for word in ['cast', 'spell', 'magic']):
            return 'spell'
        elif any(word in action_lower for word in ['rage', 'smite', 'sneak attack']):
            return 'special'

        return 'unknown'

    def _handle_attack(self, actor: Player, target: str, action: str) -> Tuple[str, Dict]:
        """Handle physical attack actions"""
        # Determine advantage/disadvantage
        has_advantage = 'advantage' in action.lower()
        has_disadvantage = 'disadvantage' in action.lower()

        # Get attack bonus
        attack_bonus = actor.get_attack_bonus('generic')  # Could be expanded for specific weapons

        # Roll attack
        attack_roll = self.dice.attack_roll(
            attack_bonus,
            advantage=has_advantage,
            disadvantage=has_disadvantage
        )

        # If hit, roll damage
        if attack_roll['total'] >= 10:  # Simplified AC
            damage_roll = self.dice.damage_roll(
                '1d8',  # Simplified damage die
                actor.get_ability_modifier('strength'),
                critical=attack_roll['critical_hit']
            )

            result = {
                'hit': True,
                'attack_roll': attack_roll,
                'damage_roll': damage_roll,
                'target': target
            }

            message = f"Attack hits! Dealing {damage_roll['total']} damage."
        else:
            result = {
                'hit': False,
                'attack_roll': attack_roll,
                'target': target
            }

            message = "Attack misses!"

        return message, result

    def _handle_spell(self, actor: Player, target: str, action: str) -> Tuple[str, Dict]:
        """Handle spell casting actions"""
        # This could be expanded with a proper spell system
        spell_attack_bonus = actor.get_ability_modifier(
            'intelligence' if actor.character_class == 'Wizard'
            else 'wisdom' if actor.character_class in ['Cleric', 'Druid']
            else 'charisma'
        )

        attack_roll = self.dice.attack_roll(spell_attack_bonus)

        if attack_roll['total'] >= 10:
            damage_roll = self.dice.damage_roll('1d10')  # Simplified spell damage
            return "Spell hits!", {'hit': True, 'damage': damage_roll['total']}

        return "Spell misses!", {'hit': False}

    def _handle_special_ability(self, actor: Player, target: str, action: str) -> Tuple[str, Dict]:
        """Handle class-specific special abilities"""
        action_lower = action.lower()

        if 'rage' in action_lower and actor.character_class == 'Barbarian':
            return "You enter a rage!", {'effect': 'rage', 'duration': 10}
        elif 'smite' in action_lower and actor.character_class == 'Paladin':
            damage_roll = self.dice.damage_roll('2d8')  # Divine Smite
            return f"Divine Smite deals {damage_roll['total']} extra damage!", {'effect': 'smite', 'damage': damage_roll['total']}
        elif 'sneak attack' in action_lower and actor.character_class == 'Rogue':
            damage_roll = self.dice.damage_roll('2d6')  # Sneak Attack
            return f"Sneak Attack deals {damage_roll['total']} extra damage!", {'effect': 'sneak_attack', 'damage': damage_roll['total']}

        return "Special ability not available!", {}