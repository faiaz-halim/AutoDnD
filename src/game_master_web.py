from typing import Dict, List, Optional
from .game_state import GameState, Player
from .ollama_client import OllamaClient
from .dice import DiceRoller
from .character.classes import CharacterClass
from .utils.text_formatter import TextFormatter as Fmt

class GameMasterWeb:
    def __init__(self):
        self.ollama = OllamaClient()
        self.game_state = GameState()
        self.dice = DiceRoller()
        self.current_player_index = 0
        self.pending_options = None

    def start_game(self) -> Dict:
        self.game_state = GameState()
        return {
            "currentLocation": None,
            "locationHistory": [],
            "activeQuests": [],
            "party": [],
            "messages": [{
                "sender": "Game Master",
                "content": "Welcome to your D&D adventure! Let's begin your journey.",
                "type": "normal"
            }]
        }

    def handle_action(self, action: str) -> Dict:
        response = self.ollama.generate_response(
            action,
            system_prompt=self._get_current_context()
        )

        dice_rolls = self._handle_dice_rolls(response)
        quest_updates = self._process_quest_updates(response)
        location_update = self._process_location_update(response)

        return {
            "messages": [{
                "sender": "Game Master",
                "content": response,
                "type": "normal"
            }],
            "diceRolls": dice_rolls,
            "questUpdates": quest_updates,
            "locationUpdate": location_update,
            "stateUpdate": self.game_state.to_dict()
        }

    def start_character_creation(self) -> Dict:
        return {
            "messages": [{
                "sender": "Game Master",
                "content": "Let's create your character. What class would you like to play?",
                "type": "normal"
            }],
            "options": [
                {"text": desc, "class": name}
                for name, desc in CharacterClass.get_all_descriptions().items()
            ]
        }

    def handle_option_selection(self, option_index: int, option: Dict) -> Dict:
        # Handle character creation or quest choices
        if "class" in option:
            return self._handle_class_selection(option)
        else:
            return self._handle_quest_choice(option_index, option)

    def _handle_class_selection(self, option: Dict) -> Dict:
        char_class = CharacterClass(option["class"])

        return {
            "messages": [{
                "sender": "Game Master",
                "content": f"Excellent choice! You've chosen to be a {option['class']}. "
                          f"Now, what shall we call your character?",
                "type": "normal"
            }],
            "stateUpdate": {"selectedClass": option["class"]}
        }

    def _handle_quest_choice(self, index: int, option: Dict) -> Dict:
        response = self.ollama.generate_response(
            f"Player chose option: {option['text']}",
            system_prompt=self._get_current_context()
        )

        return {
            "messages": [{
                "sender": "Game Master",
                "content": response,
                "type": "normal"
            }]
        }

    def _get_current_context(self) -> str:
        return f"""Current location: {self.game_state.current_location}
                  Party members: {', '.join(p.name for p in self.game_state.players)}
                  Active quests: {len(self.game_state.active_quests)}
                  Recent history: {' -> '.join(self.game_state.game_history[-3:])}"""

    def _handle_dice_rolls(self, response: str) -> List[Dict]:
        dice_results = []
        # Process dice roll commands from response
        # Add rolls to results
        return dice_results

    def _process_quest_updates(self, response: str) -> List[Dict]:
        updates = []
        # Process quest related information from response
        # Update quest status and progress
        return updates

    def _process_location_update(self, response: str) -> Optional[Dict]:
        # Check for location changes in response
        # Update location if needed
        return None

    def load_game_state(self, saved_state: Dict) -> Dict:
        # Reconstruct game state from saved data
        self.game_state = GameState.from_dict(saved_state)
        return self.game_state.to_dict()