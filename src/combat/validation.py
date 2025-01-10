"""
Combat action validation and restrictions
"""
from typing import Tuple, Dict, List
from ..game_state import Player

class CombatValidator:
    # Class-specific combat restrictions
    CLASS_RESTRICTIONS = {
        'Barbarian': {
            'restricted_during_rage': ['cast', 'spell', 'magic'],
            'message': "You cannot cast spells while raging!"
        },
        'Monk': {
            'restricted': ['heavy armor', 'shield'],
            'message': "Monks cannot use heavy armor or shields!"
        },
        'Wizard': {
            'restricted': ['heavy armor'],
            'message': "Wizards cannot wear heavy armor!"
        }
    }

    # Action requirements by type
    ACTION_REQUIREMENTS = {
        'spell': {
            'components': ['verbal', 'somatic', 'material'],
            'message': "You need to be able to speak and move to cast spells."
        },
        'rage': {
            'uses_per_day': 2,
            'message': "You've exhausted your rages for today."
        },
        'sneak_attack': {
            'conditions': ['advantage', 'ally_adjacent'],
            'message': "You need advantage or an adjacent ally to use Sneak Attack."
        }
    }

    @classmethod
    def validate_combat_action(cls, actor: Player, action: str, combat_state: Dict) -> Tuple[bool, str]:
        """
        Validate if a combat action is legal
        Returns (is_valid, message)
        """
        action_lower = action.lower()

        # Check if player is able to act
        if not cls._can_act(actor, combat_state):
            return False, "You cannot take actions in your current state!"

        # Check class-specific restrictions
        class_check = cls._check_class_restrictions(actor, action_lower)
        if not class_check[0]:
            return class_check

        # Check action-specific requirements
        action_check = cls._check_action_requirements(actor, action_lower, combat_state)
        if not action_check[0]:
            return action_check

        return True, ""

    @classmethod
    def _can_act(cls, actor: Player, combat_state: Dict) -> bool:
        """Check if actor can take actions"""
        # Check for incapacitating conditions
        conditions = combat_state.get('conditions', {}).get(actor.name, [])
        incapacitating = ['stunned', 'paralyzed', 'unconscious']

        return not any(cond in conditions for cond in incapacitating)

    @classmethod
    def _check_class_restrictions(cls, actor: Player, action: str) -> Tuple[bool, str]:
        """Check class-specific restrictions"""
        if actor.character_class in cls.CLASS_RESTRICTIONS:
            restrictions = cls.CLASS_RESTRICTIONS[actor.character_class]

            # Check general restrictions
            if 'restricted' in restrictions:
                if any(r in action for r in restrictions['restricted']):
                    return False, restrictions['message']

            # Check rage-specific restrictions for Barbarian
            if actor.character_class == 'Barbarian' and hasattr(actor, 'is_raging') and actor.is_raging:
                if any(r in action for r in restrictions['restricted_during_rage']):
                    return False, restrictions['message']

        return True, ""

    @classmethod
    def _check_action_requirements(cls, actor: Player, action: str, combat_state: Dict) -> Tuple[bool, str]:
        """Check if action requirements are met"""
        # Spell requirements
        if 'cast' in action or 'spell' in action:
            if not cls._can_cast_spells(actor, combat_state):
                return False, cls.ACTION_REQUIREMENTS['spell']['message']

        # Rage requirements
        if 'rage' in action:
            if not cls._can_rage(actor, combat_state):
                return False, cls.ACTION_REQUIREMENTS['rage']['message']

        # Sneak Attack requirements
        if 'sneak attack' in action:
            if not cls._can_sneak_attack(actor, combat_state):
                return False, cls.ACTION_REQUIREMENTS['sneak_attack']['message']

        return True, ""

    @classmethod
    def _can_cast_spells(cls, actor: Player, combat_state: Dict) -> bool:
        """Check if actor can cast spells"""
        conditions = combat_state.get('conditions', {}).get(actor.name, [])

        # Can't cast while silenced or restrained
        if 'silenced' in conditions or 'restrained' in conditions:
            return False

        return True

    @classmethod
    def _can_rage(cls, actor: Player, combat_state: Dict) -> bool:
        """Check if actor can rage"""
        if actor.character_class != 'Barbarian':
            return False

        rages_used = combat_state.get('resource_usage', {}).get(actor.name, {}).get('rage', 0)
        return rages_used < cls.ACTION_REQUIREMENTS['rage']['uses_per_day']

    @classmethod
    def _can_sneak_attack(cls, actor: Player, combat_state: Dict) -> bool:
        """Check if actor can use Sneak Attack"""
        if actor.character_class != 'Rogue':
            return False

        has_advantage = combat_state.get('advantages', {}).get(actor.name, False)
        has_ally_adjacent = cls._check_adjacent_allies(actor, combat_state)

        return has_advantage or has_ally_adjacent

    @classmethod
    def _check_adjacent_allies(cls, actor: Player, combat_state: Dict) -> bool:
        """Check if actor has allies adjacent to their target"""
        # This would need to be implemented based on your combat positioning system
        return combat_state.get('has_adjacent_ally', False)