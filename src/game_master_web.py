from typing import Dict, List, Optional
import random

from .game_state import GameState, Player
from .ollama_client import OllamaClient
from .utils.dice import DiceRoller
from .utils.text_formatter import TextFormatter as Fmt
from .ai.companion import AICompanion
from .character.stats import generate_class_stats, calculate_hit_points
from .character.classes import CLASS_DESCRIPTIONS, CharacterClass
from .prompts import SYSTEM_PROMPT, generate_environment_prompt, format_player_action

class GameMasterWeb:
    def __init__(self):
        self.ollama = OllamaClient()
        self.game_state = GameState()
        self.dice = DiceRoller()

        # Creation steps
        self.creation_step = 0
        self.temp_player_name = ""
        self.temp_class_choice = ""

        # Once creation is done, we can generate environment
        self.environment_generated = False

    def start_game(self) -> Dict:
        """
        Initialize a new game session (clear game state, begin character creation).
        Returns a dictionary with the initial messages and updated state.
        """
        self.game_state = GameState()
        self.creation_step = 1
        self.environment_generated = False

        return {
            "messages": [{
                "sender": "Game Master",
                "content": (
                    "Welcome to your D&D adventure!\n"
                    "First, let's create your character.\n"
                    "What is your character's name?"
                ),
                "type": "normal"
            }],
            "stateUpdate": self.game_state.to_dict()
        }

    def handle_action(self, action: str) -> Dict:
        """
        Handles any chat-based action from the player. This includes:
          - Character creation steps (name -> class)
          - Generating environment if needed
          - Normal free-form actions (once creation is complete)
        """
        # If still in character creation steps
        if 0 < self.creation_step < 3:
            return self._handle_character_creation_steps(action)

        # If environment not yet generated, do that automatically once player is created
        if not self.environment_generated and len(self.game_state.players) > 0:
            return self._generate_environment()

        # Otherwise handle normal free-form action in the style of a GM response
        return self._handle_normal_action(action)

    def _handle_character_creation_steps(self, action: str) -> Dict:
        """
        Step-by-step creation logic:
          Step 1 -> Ask for name
          Step 2 -> Ask for class (show classes & descriptions)
          Then generate AI companions, mark creation done
        """
        if self.creation_step == 1:
            # Player name
            name = action.strip()
            if not name:
                return {
                    "messages": [{
                        "sender": "Game Master",
                        "content": "I didn't catch your name. Please tell me your character's name again.",
                        "type": "normal"
                    }]
                }
            self.temp_player_name = name
            self.creation_step = 2

            class_list = "\n".join(
                f"{cls_name}: {CLASS_DESCRIPTIONS[cls_name]}"
                for cls_name in CLASS_DESCRIPTIONS
            )
            return {
                "messages": [{
                    "sender": "Game Master",
                    "content": (
                        f"Nice to meet you, {name}!\n\n"
                        "Available Classes:\n"
                        f"{class_list}\n\n"
                        "Which class would you like to play?"
                    ),
                    "type": "normal"
                }]
            }

        elif self.creation_step == 2:
            # Class choice
            valid_classes = list(CLASS_DESCRIPTIONS.keys())
            choice = action.capitalize()
            if choice not in valid_classes:
                return {
                    "messages": [{
                        "sender": "Game Master",
                        "content": (
                            "That class is not recognized. Please pick from:\n"
                            + ", ".join(valid_classes)
                        ),
                        "type": "normal"
                    }]
                }

            self.temp_class_choice = choice
            self._create_player_character(
                self.temp_player_name,
                self.temp_class_choice
            )
            self._generate_companions()

            self.creation_step = 0
            return {
                "messages": [{
                    "sender": "Game Master",
                    "content": (
                        f"Excellent choice! You are now {self.temp_player_name} the {self.temp_class_choice}.\n"
                        "Your character has been created.\n"
                        "I've also gathered a few companions to join you on your journey.\n"
                        "Preparing the world now..."
                    ),
                    "type": "normal"
                }],
                "stateUpdate": self.game_state.to_dict()
            }

        return {
            "messages": [{
                "sender": "Game Master",
                "content": "Character creation flow encountered an unexpected step.",
                "type": "normal"
            }]
        }

    def _create_player_character(self, name: str, class_name: str):
        """
        Create a player character, generate stats, set HP, add to game state.
        """
        stats, proficiencies = generate_class_stats(class_name)
        player = Player(
            name=name,
            character_class=class_name,
            stats=stats,
            skills=proficiencies['skills'],
            saving_throws=proficiencies['saves']
        )
        player.max_hp = calculate_hit_points(class_name, player.get_ability_modifier("constitution"))
        player.hp = player.max_hp
        self.game_state.players.append(player)

    def _generate_companions(self):
        """
        Generate 2-3 random AI companions with distinct classes
        and add them to the party.
        """
        existing_classes = [p.character_class for p in self.game_state.players]
        num_companions = random.randint(2, 3)

        for _ in range(num_companions):
            companion_data = AICompanion.generate_companion(existing_classes)
            if companion_data:
                name, comp_class, desc = companion_data
                stats, proficiencies = generate_class_stats(comp_class)
                ai_player = Player(
                    name=name,
                    character_class=comp_class,
                    stats=stats,
                    skills=proficiencies['skills'],
                    saving_throws=proficiencies['saves'],
                    is_ai=True
                )
                ai_player.max_hp = calculate_hit_points(comp_class, ai_player.get_ability_modifier("constitution"))
                ai_player.hp = ai_player.max_hp
                self.game_state.players.append(ai_player)

                existing_classes.append(comp_class)

    def _generate_environment(self) -> Dict:
        """
        Generate a game world environment once the party is formed,
        store the environment in the game state, and return a response.
        """
        prompt = generate_environment_prompt(len(self.game_state.players))
        response = self.ollama.generate_response(prompt, SYSTEM_PROMPT)

        self.game_state.environment_description = response
        self.game_state.add_to_history("Game started in a newly generated environment.")
        self.environment_generated = True

        return {
            "messages": [{
                "sender": "Game Master",
                "content": (
                    f"{response}\n\n"
                    "The world is ready! What would you like to do next?"
                ),
                "type": "normal"
            }],
            "stateUpdate": self.game_state.to_dict()
        }

    def _handle_normal_action(self, action: str) -> Dict:
        """
        Handle any free-form action from the player. Potentially incorporate
        AI companions' responses or other logic, similar to the command line version.
        """
        # If the current speaker is the main player, we can gather
        # AI companions' opinions or add them to the prompt, similar to CLI approach.
        # For simplicity, let's have each AI companion weigh in on the player's action.
        companion_opinions = []
        for companion in self.game_state.players:
            if companion.is_ai:
                opinion = AICompanion.get_response(companion, action, str(self.game_state.to_dict()))
                companion_opinions.append(opinion)

        # We'll append these opinions to the player's action so the GM (LLM) sees them
        if companion_opinions:
            action += "\nCompanions' thoughts:\n" + "\n".join(companion_opinions)

        # Format the prompt with the game state
        prompt = format_player_action(action, self.game_state.to_dict())
        response_text = self.ollama.generate_response(prompt, SYSTEM_PROMPT)

        # Add to game history
        self.game_state.add_to_history(f"Player action: {action}")
        self.game_state.add_to_history(f"GM response: {response_text}")

        return {
            "messages": [{
                "sender": "Game Master",
                "content": response_text,
                "type": "normal"
            }],
            "stateUpdate": self.game_state.to_dict()
        }

    def start_character_creation(self) -> Dict:
        """
        Not used in this particular flow, but remains for compatibility
        with existing endpoints.
        """
        return {
            "messages": [{
                "sender": "Game Master",
                "content": "Character creation already triggered or in progress.",
                "type": "normal"
            }]
        }

    def handle_option_selection(self, option_index: int, option: Dict) -> Dict:
        """
        For any additional quest/option-based interaction.
        Currently minimal. Expand as needed.
        """
        if "class" in option:
            return self._handle_class_selection(option)
        else:
            return self._handle_quest_choice(option_index, option)

    def _handle_class_selection(self, option: Dict) -> Dict:
        chosen_class = CharacterClass(option["class"])
        return {
            "messages": [{
                "sender": "Game Master",
                "content": f"You chose {option['class']}.",
                "type": "normal"
            }]
        }

    def _handle_quest_choice(self, index: int, option: Dict) -> Dict:
        # Minimal example
        prompt = f"Player chose option: {option['text']}"
        response = self.ollama.generate_response(prompt, SYSTEM_PROMPT)
        return {
            "messages": [{
                "sender": "Game Master",
                "content": response,
                "type": "normal"
            }]
        }

    def _get_current_context(self) -> str:
        """
        Provide short context for the Ollama model about the current game state.
        """
        return (
            f"Current location: {self.game_state.current_location}\n"
            f"Party members: {', '.join(p.name for p in self.game_state.players)}\n"
            f"Active quests: {len(self.game_state.active_quests)}\n"
            f"Environment: {self.game_state.environment_description[:150]}...\n"
            f"Recent history: {' -> '.join(self.game_state.game_history[-3:])}"
        )

    def load_game_state(self, saved_state: Dict) -> Dict:
        """
        Restore game state from a saved JSON object.
        """
        self.game_state = GameState.from_dict(saved_state)
        return self.game_state.to_dict()