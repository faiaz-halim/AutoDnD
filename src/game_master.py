from .ollama_client import OllamaClient
from .game_state import GameState, Player
from .dice import DiceRoller
from .prompts import SYSTEM_PROMPT, generate_environment_prompt, format_player_action
from .text_formatter import TextFormatter as Fmt
import re
import random
from typing import List, Optional, Tuple, Dict, Union

class GameMaster:
    def __init__(self):
        self.ollama = OllamaClient()
        self.game_state = GameState()
        self.dice = DiceRoller()
        self.current_player_index = 0

    def start_game(self):
        """Initialize and start the game"""
        Fmt.clear_screen()
        print(Fmt.header("Welcome to D&D Command Line Adventure!"))

        while True:
            try:
                print(Fmt.system_message("\nHow many players will be joining the adventure?"))
                num_players = int(input(Fmt.menu_option("Enter number", "1-6") + ": "))
                if 1 <= num_players <= 6:
                    break
                print(Fmt.failure_text("Please enter a number between 1 and 6."))
            except ValueError:
                print(Fmt.failure_text("Please enter a valid number."))

        self.game_state.num_players = num_players
        self._setup_players()
        self._generate_environment()
        self.game_loop()

    def _setup_players(self):
        """Set up player characters and generate AI companions"""
        print(Fmt.header("Character Creation"))

        # First, create the human player's character
        print(Fmt.header("Create Your Character"))
        name = input(Fmt.menu_option("Your character name", "") + ": ")

        # Show available classes with descriptions
        class_descriptions = {
            'Fighter': 'Skilled warrior, master of weapons and armor',
            'Wizard': 'Master of arcane magic and spells',
            'Rogue': 'Skilled in stealth, thievery, and precision strikes',
            'Cleric': 'Divine spellcaster, healer, and warrior of faith',
            'Ranger': 'Expert tracker, archer, and wilderness survivor',
            'Paladin': 'Holy warrior combining martial might with divine power'
        }

        print(Fmt.system_message("\nAvailable Classes:"))
        for class_name, description in class_descriptions.items():
            print(Fmt.menu_option(f"{class_name}", f"{description}"))

        char_class = input(Fmt.menu_option("\nChoose your class", "") + ": ")

        # Create player character
        stats, proficiencies = self._generate_class_stats(char_class)
        player = self._create_character(name, char_class, stats, proficiencies)
        self.game_state.players.append(player)

        # Generate AI party members
        print(Fmt.header("\nGenerating Your Party Members"))

        # Number of AI companions (2-3 random companions)
        num_companions = random.randint(2, 3)

        # List of companion templates for variety
        companion_templates = [
            ('Thorin', 'Fighter', 'A gruff but loyal dwarf warrior'),
            ('Elara', 'Wizard', 'A studious elven mage with a dry sense of humor'),
            ('Shadow', 'Rogue', 'A mysterious halfling with a heart of gold'),
            ('Lightbringer', 'Cleric', 'A cheerful human priest devoted to helping others'),
            ('Silvermane', 'Ranger', 'A quiet wood elf with unmatched survival skills'),
            ('Dawn', 'Paladin', 'A noble human warrior sworn to protect the innocent')
        ]

        # Select random companions ensuring no class duplicates
        used_companions = []
        used_classes = [char_class]  # Include player's class

        for i in range(num_companions):
            while True:
                companion = random.choice(companion_templates)
                if companion not in used_companions and companion[1] not in used_classes:
                    used_companions.append(companion)
                    used_classes.append(companion[1])
                    break

            print(Fmt.system_message(f"\nCompanion {i+1}:"))
            print(Fmt.success_text(f"Meet {companion[0]}, the {companion[1]}"))
            print(Fmt.system_message(companion[2]))

            # Create AI companion character
            stats, proficiencies = self._generate_class_stats(companion[1])
            ai_player = self._create_character(companion[0], companion[1], stats, proficiencies)
            ai_player.is_ai = True  # Mark as AI companion
            self.game_state.players.append(ai_player)

        self.game_state.num_players = len(self.game_state.players)
        print(Fmt.header("\nYour Adventure Party is Complete!"))

    def _create_character(self, name: str, char_class: str, stats: Dict[str, int], proficiencies: Dict) -> Player:
        """Create a new character with given parameters"""
        player = Player(
            name=name,
            character_class=char_class,
            stats=stats,
            skills=proficiencies['skills'],
            saving_throws=proficiencies['saves']
        )

        # Roll for HP
        hp_roll = self.dice.roll(f"1d{self._get_class_hit_die(char_class)}")
        player.max_hp = hp_roll[0] + player.get_ability_modifier("constitution")
        player.hp = player.max_hp

        print(Fmt.success_text(f"\nCreated {name} the {char_class}!"))
        print(Fmt.system_message("Starting Stats:"))
        for stat, value in player.stats.items():
            mod = player.get_ability_modifier(stat)
            print(Fmt.system_message(f"{stat.title()}: {value} ({'+' if mod >= 0 else ''}{mod})"))
        print(Fmt.system_message(f"HP: {player.hp}"))

    def _generate_environment(self):
        """Generate the initial game environment"""
        print(Fmt.header("Generating Game World"))
        prompt = generate_environment_prompt(self.game_state.num_players)
        response = self.ollama.generate_response(prompt, SYSTEM_PROMPT)

        self.game_state.environment_description = response
        self.game_state.add_to_history("Game started")

        print(Fmt.gm_speech(response))

    def _determine_roll_type(self, action: str, player: Player) -> Tuple[str, Dict]:
        """
        Analyze player action and determine appropriate type of roll
        Returns tuple of (roll_type, roll_params)
        """
        action_lower = action.lower()
        roll_info = {
            'advantage': False,
            'disadvantage': False,
            'proficiency': False,
            'bonus': 0
        }

        # Common action keywords and their associated checks
        skill_checks = {
            'search': ('investigation', 'wisdom'),
            'look': ('perception', 'wisdom'),
            'investigate': ('investigation', 'intelligence'),
            'persuade': ('persuasion', 'charisma'),
            'intimidate': ('intimidation', 'charisma'),
            'sneak': ('stealth', 'dexterity'),
            'climb': ('athletics', 'strength'),
            'jump': ('athletics', 'strength'),
            'hide': ('stealth', 'dexterity'),
            'sense': ('perception', 'wisdom'),
            'study': ('investigation', 'intelligence'),
            'remember': ('history', 'intelligence'),
            'heal': ('medicine', 'wisdom'),
            'pick': ('sleight_of_hand', 'dexterity'),
            'perform': ('performance', 'charisma'),
            'charm': ('persuasion', 'charisma'),
            'track': ('survival', 'wisdom')
        }

        # Combat related keywords
        combat_actions = ['attack', 'fight', 'slash', 'shoot', 'stab', 'punch', 'strike']

        # Check if this is a combat action
        if any(word in action_lower for word in combat_actions):
            return 'attack', {
                'attack_bonus': player.get_attack_bonus('generic'),
                'advantage': 'advantage' in action_lower,
                'disadvantage': 'disadvantage' in action_lower
            }

        # Check for skill checks
        for keyword, (skill, ability) in skill_checks.items():
            if keyword in action_lower:
                return 'skill', {
                    'skill': skill,
                    'ability': ability,
                    'bonus': player.get_skill_bonus(skill),
                    'advantage': 'advantage' in action_lower,
                    'disadvantage': 'disadvantage' in action_lower
                }

        # Default to ability check if no specific match
        # Try to determine the most appropriate ability score
        abilities = {
            'strength': ['lift', 'push', 'pull', 'break', 'bend', 'carry'],
            'dexterity': ['dodge', 'balance', 'leap', 'catch', 'throw'],
            'constitution': ['endure', 'resist', 'withstand'],
            'intelligence': ['recall', 'analyze', 'understand', 'figure'],
            'wisdom': ['notice', 'sense', 'feel', 'spot'],
            'charisma': ['convince', 'persuade', 'deceive', 'lie', 'perform']
        }

        for ability, keywords in abilities.items():
            if any(word in action_lower for word in keywords):
                return 'ability', {
                    'ability': ability,
                    'bonus': player.get_ability_modifier(ability),
                    'advantage': 'advantage' in action_lower,
                    'disadvantage': 'disadvantage' in action_lower
                }

        # If no specific ability is indicated, default to wisdom for general checks
        return 'ability', {
            'ability': 'wisdom',
            'bonus': player.get_ability_modifier('wisdom'),
            'advantage': 'advantage' in action_lower,
            'disadvantage': 'disadvantage' in action_lower
        }

    def _handle_dice_rolls(self, gm_response: str, player: Player, action: str) -> str:
        """Enhanced dice roll handling with player stats"""
        # First determine the type of roll needed based on the action
        roll_type, roll_params = self._determine_roll_type(action, player)

        # Perform the appropriate roll
        roll_result = None
        if roll_type == 'attack':
            roll_result = self.dice.attack_roll(
                roll_params['attack_bonus'],
                roll_params['advantage'],
                roll_params['disadvantage']
            )
            # If it's an attack, also roll for damage on hit
            if roll_result['total'] >= 10:  # Simple AC threshold for example
                damage_roll = self.dice.damage_roll('1d8', player.get_ability_modifier('strength'),
                                                  roll_result['critical_hit'])
                roll_result['damage'] = damage_roll

        elif roll_type == 'skill':
            roll_result = self.dice.skill_check(
                roll_params['bonus'],
                roll_params['advantage'],
                roll_params['disadvantage']
            )

        elif roll_type == 'ability':
            roll_result = self.dice.ability_check(
                10 + roll_params['bonus'],  # Base ability score
                False,  # Proficiency
                roll_params['advantage'],
                roll_params['disadvantage']
            )

        # Format the roll result for the GM response
        result_desc = self._format_roll_result(roll_type, roll_result, roll_params)

        # Inject the roll result into the GM response
        return f"{result_desc}\n\n{gm_response}"

    def _format_roll_result(self, roll_type: str, roll_result: Dict, roll_params: Dict) -> str:
        """Format the roll result for display"""
        if roll_type == 'attack':
            result = f"Attack roll: {roll_result['total']}"
            if roll_result['critical_hit']:
                result += " (CRITICAL HIT!)"
            elif roll_result['critical_miss']:
                result += " (Critical Miss!)"
            if 'damage' in roll_result:
                result += f"\nDamage: {roll_result['damage']['total']}"
            return result

        elif roll_type == 'skill':
            skill_name = roll_params.get('skill', '').replace('_', ' ').title()
            result = f"{skill_name} check: {roll_result['total']}"
            if roll_result['critical_success']:
                result += " (Critical Success!)"
            elif roll_result['critical_failure']:
                result += " (Critical Failure!)"
            return result

        else:  # ability check
            ability_name = roll_params.get('ability', '').title()
            result = f"{ability_name} check: {roll_result['total']}"
            if roll_result['critical_success']:
                result += " (Critical Success!)"
            elif roll_result['critical_failure']:
                result += " (Critical Failure!)"
            return result

    def _get_player_input(self, player: Player) -> Optional[str]:
        """Get input from a specific player"""
        print(Fmt.header(f"{player.name}'s Turn"))
        print(Fmt.system_message("What would you like to do?"))
        action = input(Fmt.menu_option(">", "") + " ").strip()
        return action if action else None

    def _get_player_opinions(self, action: str, current_player: Player) -> List[str]:
        """Get opinions from other players about the current action"""
        opinions = []

        print(Fmt.system_message(f"\nOther players, what do you think about {current_player.name}'s action?"))
        print(Fmt.system_message("(Press Enter to skip, or type your thoughts)"))

        for player in self.game_state.players:
            if player != current_player:
                opinion = input(Fmt.menu_option(f"{player.name}", "") + ": ").strip()
                if opinion:
                    opinions.append(f"{player.name}: {opinion}")

        return opinions

    def game_loop(self):
        """Main game loop"""
        print(Fmt.header("Game Started"))
        print(Fmt.system_message("Type 'quit' to end the game, or 'save' to save your progress."))
        print(Fmt.system_message("Type 'help' for more commands."))

        while True:
            try:
                current_player = self.game_state.players[self.current_player_index]

                # Get current player's action
                if current_player.is_ai:
                    # AI companion's turn
                    print(Fmt.header(f"{current_player.name}'s Turn"))
                    action = self._get_ai_action(current_player, str(self.game_state.to_dict()))
                    print(Fmt.system_message(f"{current_player.name} acts: {action}"))

                    # Get player's opinion on AI action
                    print(Fmt.system_message("\nWhat do you think about this action? (Press Enter to skip)"))
                    player_opinion = input(Fmt.menu_option("Your thoughts", "") + ": ").strip()

                    if player_opinion:
                        action += f"\nPlayer's thoughts: {player_opinion}"
                else:
                    # Human player's turn
                    action = self._get_player_input(current_player)

                if not action:
                    continue

                if action.lower() == "quit":
                    print(Fmt.system_message("\nThanks for playing!"))
                    break
                elif action.lower() == "save":
                    self.game_state.save_game()
                    print(Fmt.success_text("Game saved!"))
                    continue
                elif action.lower() == "help":
                    self._show_help()
                    continue

                # Get other players' opinions
                opinions = self._get_player_opinions(action, current_player)

                # Include opinions in the prompt if any were given
                if opinions:
                    action = f"{action}\nOther players' thoughts:\n" + "\n".join(opinions)

                # Format the action with current game state
                prompt = format_player_action(action, self.game_state.to_dict())

                # Get GM response
                response = self.ollama.generate_response(prompt, SYSTEM_PROMPT)

                # Handle dice rolls with player stats
                response = self._handle_dice_rolls(response, current_player, action)

                # Update game history
                self.game_state.add_to_history(f"{current_player.name}: {action}")
                self.game_state.add_to_history(f"GM: {response}")

                # Check for conditions that might affect the next action
                if "you are knocked prone" in response.lower():
                    print(Fmt.combat_text(f"{current_player.name} is knocked prone!"))
                elif "you take damage" in response.lower():
                    print(Fmt.combat_text(f"{current_player.name} takes damage!"))

                # Display the response
                print("\n" + Fmt.gm_speech(response))

                # Move to next player
                self.current_player_index = (self.current_player_index + 1) % len(self.game_state.players)

            except KeyboardInterrupt:
                print(Fmt.system_message("\nGame interrupted. Would you like to save before quitting? (y/n)"))
                if input().lower().startswith('y'):
                    self.game_state.save_game()
                    print(Fmt.success_text("Game saved!"))
                break
            except Exception as e:
                print(Fmt.failure_text(f"\nAn error occurred: {str(e)}"))
                print(Fmt.system_message("Would you like to continue? (y/n)"))
                if not input().lower().startswith('y'):
                    break

    def _get_class_hit_die(self, char_class: str) -> int:
        """Get the hit die for a given class"""
        hit_dice = {
            'barbarian': 12,
            'fighter': 10,
            'paladin': 10,
            'ranger': 10,
            'cleric': 8,
            'druid': 8,
            'monk': 8,
            'rogue': 8,
            'warlock': 8,
            'bard': 8,
            'sorcerer': 6,
            'wizard': 6
        }
        return hit_dice.get(char_class.lower(), 8)

    def _generate_class_stats(self, char_class: str) -> Tuple[Dict[str, int], Dict[str, Dict[str, bool]]]:
        """Generate stats and proficiencies for a given class"""
        # Roll 4d6 drop lowest for each stat
        stats = {}
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            rolls = sorted([random.randint(1, 6) for _ in range(4)])
            stats[ability] = sum(rolls[1:])  # Drop lowest roll

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

        # Add class-specific proficiencies
        if char_class.lower() == 'fighter':
            proficiencies['saves']['strength'] = True
            proficiencies['saves']['constitution'] = True
            proficiencies['skills']['athletics'] = True
            proficiencies['skills']['intimidation'] = True
        elif char_class.lower() == 'rogue':
            proficiencies['saves']['dexterity'] = True
            proficiencies['saves']['intelligence'] = True
            proficiencies['skills']['stealth'] = True
            proficiencies['skills']['sleight_of_hand'] = True
        elif char_class.lower() == 'wizard':
            proficiencies['saves']['intelligence'] = True
            proficiencies['saves']['wisdom'] = True
            proficiencies['skills']['arcana'] = True
            proficiencies['skills']['history'] = True
        # Add more classes as needed

        return stats, proficiencies

    def _generate_ai_response(self, action: str, ai_player: Player) -> str:
        """Generate AI companion's response to player action"""
        personality_traits = {
            'Fighter': ['pragmatic', 'protective', 'direct'],
            'Wizard': ['analytical', 'curious', 'cautious'],
            'Rogue': ['witty', 'observant', 'skeptical'],
            'Cleric': ['supportive', 'wise', 'diplomatic'],
            'Ranger': ['perceptive', 'practical', 'reserved'],
            'Paladin': ['noble', 'determined', 'inspiring']
        }

        traits = personality_traits.get(ai_player.character_class, ['helpful', 'friendly'])
        trait = random.choice(traits)

        # Generate response based on character class and personality
        responses = {
            'Fighter': [
                f"As a {trait} warrior, I suggest we...",
                "Watch your back, I'll cover you.",
                "That's a bold move, let me help.",
            ],
            'Wizard': [
                "Interesting approach, but consider the arcane implications...",
                "I've read about similar situations in my studies...",
                "Perhaps a touch of magic could help here?",
            ],
            'Rogue': [
                "I notice something you might have missed...",
                "Let's be careful here...",
                "I have a sneaky idea...",
            ],
            'Cleric': [
                "May the gods guide your actions...",
                "I can provide healing if needed...",
                "Let us proceed with wisdom...",
            ],
            'Ranger': [
                "My wilderness experience suggests...",
                "I've tracked similar things before...",
                "The environment could be used to our advantage...",
            ],
            'Paladin': [
                "Honor guides us to...",
                "We shall overcome this challenge...",
                "Stand strong, my friend...",
            ]
        }

        class_responses = responses.get(ai_player.character_class, ["I support your decision."])
        return f"{ai_player.name}: {random.choice(class_responses)}"

    def _get_ai_action(self, ai_player: Player, context: str) -> str:
        """Generate an action for an AI companion"""
        class_actions = {
            'Fighter': [
                "I move to protect our flank",
                "I ready my weapon and watch for enemies",
                "I take a defensive stance",
                "I survey the battlefield for tactical advantages"
            ],
            'Wizard': [
                "I study the magical aura in the area",
                "I prepare a defensive spell",
                "I recall relevant arcane knowledge",
                "I examine any magical signatures"
            ],
            'Rogue': [
                "I check for hidden dangers",
                "I move silently to scout ahead",
                "I look for alternative routes",
                "I watch for suspicious behavior"
            ],
            'Cleric': [
                "I pray for divine guidance",
                "I prepare healing magic",
                "I sense for evil presence",
                "I bless our path forward"
            ],
            'Ranger': [
                "I search for tracks and signs",
                "I survey the environment",
                "I listen for unusual sounds",
                "I check for natural hazards"
            ],
            'Paladin': [
                "I stand guard vigilantly",
                "I sense for evil presence",
                "I inspire our allies",
                "I maintain a protective watch"
            ]
        }

        actions = class_actions.get(ai_player.character_class, ["I stay alert and ready"])
        return random.choice(actions)

    def _show_help(self):
        """Display help information"""
        help_text = """
Available Commands:
- quit: End the game
- save: Save your current progress
- help: Show this help message

Game Tips:
- Describe your actions clearly
- Common actions: look, move, attack, talk, search, investigate
- For ability checks, just describe what you want to do
- The GM will ask for rolls when needed
- Other players can provide input on your actions

Examples:
- "I want to search the room for traps"
- "I approach the merchant and ask about rumors"
- "I attack the goblin with my sword"
        """
        print(Fmt.system_message(help_text))