from typing import List, Dict
import random
from ..game_state import Player

class AICompanion:
    PERSONALITY_TRAITS = {
        'Barbarian': ['fierce', 'primal', 'passionate'],
        'Bard': ['charismatic', 'witty', 'dramatic'],
        'Cleric': ['devout', 'wise', 'caring'],
        'Druid': ['naturalistic', 'contemplative', 'balanced'],
        'Fighter': ['tactical', 'practical', 'determined'],
        'Monk': ['disciplined', 'focused', 'insightful'],
        'Paladin': ['righteous', 'honorable', 'resolute'],
        'Ranger': ['observant', 'pragmatic', 'resourceful'],
        'Rogue': ['cunning', 'quick-witted', 'opportunistic'],
        'Sorcerer': ['confident', 'intuitive', 'unpredictable'],
        'Warlock': ['mysterious', 'enigmatic', 'knowledgeable'],
        'Wizard': ['analytical', 'studious', 'methodical']
    }

    @classmethod
    def generate_companion(cls, existing_classes: List[str] = None) -> Dict[str, str]:
        """Generate a random AI companion"""
        companion_templates = [
            ('Thorin', 'Barbarian', 'A gruff but loyal dwarf warrior'),
            ('Elara', 'Wizard', 'A studious elven mage'),
            ('Shadow', 'Rogue', 'A mysterious halfling with a heart of gold'),
            ('Lightbringer', 'Cleric', 'A cheerful human priest'),
            ('Silvermane', 'Ranger', 'A quiet wood elf with unmatched skills'),
            ('Dawn', 'Paladin', 'A noble human warrior'),
            ('Melody', 'Bard', 'A charismatic halfling performer'),
            ('Grove', 'Druid', 'A wise old forest gnome'),
            ('Serenity', 'Monk', 'A disciplined human martial artist'),
            ('Storm', 'Sorcerer', 'A powerful human spellcaster'),
            ('Twilight', 'Warlock', 'A mysterious tiefling warlock')
        ]

        available_companions = [
            comp for comp in companion_templates
            if comp[1] not in (existing_classes or [])
        ]

        if not available_companions:
            return None

        return random.choice(available_companions)

    @classmethod
    def get_response(cls, player: Player, action: str, context: str) -> str:
        """Generate an AI companion's response to a situation"""
        traits = cls.PERSONALITY_TRAITS.get(player.character_class, ['helpful'])
        trait = random.choice(traits)

        from .responses import CLASS_RESPONSES
        responses = CLASS_RESPONSES.get(player.character_class, ["I support your decision."])

        # Generate contextual response
        base_response = random.choice(responses)
        return f"{player.name} ({trait}): {base_response}"

    @classmethod
    def get_action(cls, player: Player, context: str) -> str:
        """Generate an AI companion's action"""
        from .actions import CLASS_ACTIONS, CONTEXT_ADDONS

        # Get class-specific actions
        actions = CLASS_ACTIONS.get(player.character_class, ["I stay alert and ready"])
        base_action = random.choice(actions)

        # Add context-based variations
        for context_type, addons in CONTEXT_ADDONS.items():
            if context_type in context.lower():
                return f"{base_action} {random.choice(addons)}"

        return base_action