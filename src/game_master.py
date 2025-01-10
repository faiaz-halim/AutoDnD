"""
Main Game Master class that orchestrates the D&D game
"""
from typing import List, Optional, Dict, Tuple
import random

from .ollama_client import OllamaClient
from .game_state import GameState, Player
from .utils.dice import DiceRoller
from .utils.text_formatter import TextFormatter as Fmt
from .combat.actions import CombatHandler
from .combat.validation import CombatValidator
from .ai.companion import AICompanion
from .character.stats import generate_class_stats, calculate_hit_points
from .character.classes import CLASS_DESCRIPTIONS, CLASS_HIT_DICE, CharacterClass
from .prompts import SYSTEM_PROMPT, generate_environment_prompt, format_player_action

class GameMaster:
    def __init__(self):
        """Initialize GameMaster with necessary components"""
        self.ollama = OllamaClient()
        self.game_state = GameState()
        self.dice = DiceRoller()
        self.combat_handler = CombatHandler()
        self.current_player_index = 0

    def start_game(self):
        """Initialize and start the game"""
        Fmt.clear_screen()
        print(Fmt.header("Welcome to D&D Command Line Adventure!"))

        # Create player character
        self._create_player_character()

        # Generate AI companions
        self._generate_ai_companions()

        # Generate game environment
        self._generate_environment()

        # Start game loop
        self.game_loop()

    def _create_player_character(self):
        """Guide player through character creation"""
        print(Fmt.header("Create Your Character"))
        name = input(Fmt.menu_option("Your character name", "") + ": ")

        # Show available classes with descriptions
        print(Fmt.system_message("\nAvailable Classes:"))
        for class_name, description in CLASS_DESCRIPTIONS.items():
            print(Fmt.menu_option(f"{class_name}", f"{description}"))

        # Class selection with validation
        while True:
            char_class = input(Fmt.menu_option("\nChoose your class", "") + ": ").capitalize()
            if char_class in CLASS_DESCRIPTIONS:
                break
            print(Fmt.failure_text("Invalid class choice. Please select from the available classes."))

        # Generate character
        character_class = CharacterClass(char_class)
        stats, proficiencies = generate_class_stats(char_class)
        player = Player(
            name=name,
            character_class=char_class,
            stats=stats,
            skills=proficiencies['skills'],
            saving_throws=proficiencies['saves']
        )

        # Calculate HP and add character features
        player.max_hp = calculate_hit_points(char_class, player.get_ability_modifier("constitution"))
        player.hp = player.max_hp

        self.game_state.players.append(player)

        # Display character info
        print(Fmt.success_text(f"\nCreated {name} the {char_class}!"))
        self._display_character_stats(player)
        print(Fmt.system_message("\nClass Features:"))
        for feature in character_class.get_features_by_level(1):
            print(Fmt.system_message(f"- {feature}"))

    def _generate_ai_companions(self):
        """Generate AI companion characters"""
        print(Fmt.header("\nGenerating Your Party Members"))

        # Get existing class to avoid duplicates
        existing_classes = [p.character_class for p in self.game_state.players]

        # Generate 2-3 companions
        num_companions = random.randint(2, 3)

        for i in range(num_companions):
            companion = AICompanion.generate_companion(existing_classes)
            if companion:
                name, char_class, description = companion

                # Generate stats for companion
                stats, proficiencies = generate_class_stats(char_class)
                ai_player = Player(
                    name=name,
                    character_class=char_class,
                    stats=stats,
                    skills=proficiencies['skills'],
                    saving_throws=proficiencies['saves'],
                    is_ai=True
                )

                # Calculate HP
                ai_player.max_hp = calculate_hit_points(char_class, ai_player.get_ability_modifier("constitution"))
                ai_player.hp = ai_player.max_hp

                self.game_state.players.append(ai_player)
                existing_classes.append(char_class)

                print(Fmt.system_message(f"\nCompanion {i+1}:"))
                print(Fmt.success_text(f"Meet {name}, the {char_class}"))
                print(Fmt.system_message(description))
                self._display_character_stats(ai_player)

    def _display_character_stats(self, player: Player):
        """Display a character's stats"""
        print(Fmt.system_message("\nCharacter Stats:"))
        for stat, value in player.stats.items():
            mod = player.get_ability_modifier(stat)
            print(Fmt.system_message(f"{stat.title()}: {value} ({'+' if mod >= 0 else ''}{mod})"))
        print(Fmt.system_message(f"HP: {player.hp}/{player.max_hp}"))

        print(Fmt.system_message("\nProficient Skills:"))
        prof_skills = [skill for skill, is_prof in player.skills.items() if is_prof]
        for skill in prof_skills:
            print(Fmt.system_message(f"- {skill.replace('_', ' ').title()}"))

    def _generate_environment(self):
        """Generate the initial game environment"""
        print(Fmt.header("Generating Game World"))
        prompt = generate_environment_prompt(len(self.game_state.players))
        response = self.ollama.generate_response(prompt, SYSTEM_PROMPT)

        self.game_state.environment_description = response
        self.game_state.add_to_history("Game started")

        print(Fmt.gm_speech(response))

    def game_loop(self):
        """Main game loop"""
        print(Fmt.header("Game Started"))
        print(Fmt.system_message("Type 'quit' to end the game, or 'save' to save your progress."))
        print(Fmt.system_message("Type 'help' for more commands."))

        while True:
            try:
                current_player = self.game_state.players[self.current_player_index]

                # Handle AI or player turn
                if current_player.is_ai:
                    self._handle_ai_turn(current_player)
                else:
                    self._handle_player_turn(current_player)

                # Move to next player
                self.current_player_index = (self.current_player_index + 1) % len(self.game_state.players)

            except KeyboardInterrupt:
                self._handle_game_interrupt()
                break
            except Exception as e:
                if not self._handle_game_error(e):
                    break

    def _handle_ai_turn(self, ai_player: Player):
        """Handle AI companion's turn"""
        print(Fmt.header(f"{ai_player.name}'s Turn"))

        # Generate AI action
        action = AICompanion.get_action(ai_player, str(self.game_state.to_dict()))
        print(Fmt.system_message(f"{ai_player.name} acts: {action}"))

        # Get player's input on AI action
        print(Fmt.system_message("\nWhat do you think about this action? (Press Enter to skip)"))
        player_opinion = input(Fmt.menu_option("Your thoughts", "") + ": ").strip()

        if player_opinion:
            action += f"\nPlayer's thoughts: {player_opinion}"

        # Process AI action
        self._process_action(ai_player, action)

    def _handle_player_turn(self, player: Player):
        """Handle human player's turn"""
        while True:
            action = self._get_player_input(player)
            if not action:
                continue

            if action.lower() == "quit":
                print(Fmt.system_message("\nThanks for playing!"))
                raise KeyboardInterrupt
            elif action.lower() == "save":
                self.game_state.save_game()
                print(Fmt.success_text("Game saved!"))
                continue
            elif action.lower() == "help":
                self._show_help()
                continue
            elif action.lower() == "status":
                self._display_character_stats(player)
                continue

            # Get AI companions' opinions
            opinions = self._get_ai_opinions(action, player)
            if opinions:
                action += "\nCompanions' thoughts:\n" + "\n".join(opinions)

            # Process player action
            self._process_action(player, action)
            break

    def _process_action(self, actor: Player, action: str):
        """Process a player or AI action"""
        # Validate action
        is_valid, message = CombatValidator.validate_combat_action(actor, action, {})
        if not is_valid:
            print(Fmt.failure_text(message))
            return

        # Format action with game state
        prompt = format_player_action(action, self.game_state.to_dict())

        # Get GM response
        response = self.ollama.generate_response(prompt, SYSTEM_PROMPT)

        # Handle dice rolls and combat
        response = self.combat_handler.handle_combat_action(response, actor, action)

        # Update game history
        self.game_state.add_to_history(f"{actor.name}: {action}")
        self.game_state.add_to_history(f"GM: {response}")

        # Display the response
        print("\n" + Fmt.gm_speech(response))

        # Check for conditions
        self._check_conditions(response, actor)

    def _get_player_input(self, player: Player) -> Optional[str]:
        """Get input from a specific player"""
        print(Fmt.header(f"{player.name}'s Turn"))
        print(Fmt.system_message("What would you like to do?"))
        action = input(Fmt.menu_option(">", "") + " ").strip()
        return action if action else None

    def _get_ai_opinions(self, action: str, current_player: Player) -> List[str]:
        """Get AI companions' opinions about the player's action"""
        opinions = []
        for companion in self.game_state.players:
            if companion.is_ai:
                opinion = AICompanion.get_response(companion, action, str(self.game_state.to_dict()))
                opinions.append(opinion)
        return opinions

    def _handle_game_interrupt(self):
        """Handle game interruption"""
        print(Fmt.system_message("\nGame interrupted. Would you like to save before quitting? (y/n)"))
        if input().lower().startswith('y'):
            self.game_state.save_game()
            print(Fmt.success_text("Game saved!"))

    def _handle_game_error(self, error: Exception) -> bool:
        """Handle game error and return whether to continue"""
        print(Fmt.failure_text(f"\nAn error occurred: {str(error)}"))
        print(Fmt.system_message("Would you like to continue? (y/n)"))
        return input().lower().startswith('y')

    def _check_conditions(self, response: str, actor: Player):
        """Check for condition changes from GM response"""
        response_lower = response.lower()
        conditions = {
            'unconscious': 'falls unconscious',
            'prone': 'is knocked prone',
            'poisoned': 'is poisoned',
            'stunned': 'is stunned',
            'blinded': 'is blinded',
            'deafened': 'is deafened'
        }

        for condition, message in conditions.items():
            if condition in response_lower:
                print(Fmt.combat_text(f"{actor.name} {message}!"))

    def _show_help(self):
        """Display help information"""
        help_text = """
Available Commands:
- quit: End the game
- save: Save your current progress
- help: Show this help message
- status: Show your character's current stats

Game Tips:
- Describe your actions clearly
- Common actions: look, move, attack, talk, search, investigate
- For ability checks, just describe what you want to do
- The GM will ask for rolls when needed
- Other players can provide input on your actions

Combat Tips:
- Specify your target and weapon
- You can say "with advantage" or "with disadvantage" if applicable
- Critical hits occur on natural 20s
- Natural 1s are automatic misses

Examples:
- "I want to search the room for traps"
- "I approach the merchant and ask about rumors"
- "I attack the goblin with my sword"
- "I try to sneak past the guard with advantage"
- "I attempt to recall any information about this creature"
        """
        print(Fmt.system_message(help_text))

    def load_game(self, filename: str = "game_save.json") -> bool:
        """Load a saved game"""
        try:
            self.game_state = GameState.load_game(filename)
            print(Fmt.success_text("Game loaded successfully!"))
            return True
        except Exception as e:
            print(Fmt.failure_text(f"Error loading game: {str(e)}"))
            return False