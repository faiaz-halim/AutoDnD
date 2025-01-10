from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json

@dataclass
class Player:
    name: str
    character_class: str
    level: int = 1
    hp: int = 0
    max_hp: int = 0
    armor_class: int = 10
    initiative_bonus: int = 0
    proficiency_bonus: int = 2
    is_ai: bool = False  # Flag to identify AI companions
    personality: str = ""  # Brief personality description for AI companions

    # Base ability scores
    stats: Dict[str, int] = field(default_factory=lambda: {
        "strength": 10,
        "dexterity": 10,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 10,
        "charisma": 10
    })

    # Skill proficiencies
    skills: Dict[str, bool] = field(default_factory=lambda: {
        "acrobatics": False,
        "animal_handling": False,
        "arcana": False,
        "athletics": False,
        "deception": False,
        "history": False,
        "insight": False,
        "intimidation": False,
        "investigation": False,
        "medicine": False,
        "nature": False,
        "perception": False,
        "performance": False,
        "persuasion": False,
        "religion": False,
        "sleight_of_hand": False,
        "stealth": False,
        "survival": False
    })

    # Saving throw proficiencies
    saving_throws: Dict[str, bool] = field(default_factory=lambda: {
        "strength": False,
        "dexterity": False,
        "constitution": False,
        "intelligence": False,
        "wisdom": False,
        "charisma": False
    })

    # Equipment and weapons
    weapons: List[Dict[str, str]] = field(default_factory=list)
    armor: Optional[str] = None

    def get_ability_modifier(self, ability: str) -> int:
        """Calculate ability modifier from ability score"""
        score = self.stats.get(ability.lower(), 10)
        return (score - 10) // 2

    def get_skill_bonus(self, skill: str) -> int:
        """Calculate total bonus for a skill check"""
        # Map skills to their primary ability scores
        ability_map = {
            "acrobatics": "dexterity",
            "animal_handling": "wisdom",
            "arcana": "intelligence",
            "athletics": "strength",
            "deception": "charisma",
            "history": "intelligence",
            "insight": "wisdom",
            "intimidation": "charisma",
            "investigation": "intelligence",
            "medicine": "wisdom",
            "nature": "intelligence",
            "perception": "wisdom",
            "performance": "charisma",
            "persuasion": "charisma",
            "religion": "intelligence",
            "sleight_of_hand": "dexterity",
            "stealth": "dexterity",
            "survival": "wisdom"
        }

        ability = ability_map.get(skill.lower(), "dexterity")
        ability_mod = self.get_ability_modifier(ability)
        prof_bonus = self.proficiency_bonus if self.skills.get(skill.lower(), False) else 0

        return ability_mod + prof_bonus

    def get_saving_throw_bonus(self, ability: str) -> int:
        """Calculate total bonus for a saving throw"""
        ability_mod = self.get_ability_modifier(ability)
        prof_bonus = self.proficiency_bonus if self.saving_throws.get(ability.lower(), False) else 0

        return ability_mod + prof_bonus

    def get_attack_bonus(self, weapon: str) -> int:
        """Calculate attack bonus for a weapon"""
        # This is a simplified version - could be expanded based on weapon properties
        ability = "strength"  # Default to strength
        if weapon.lower() in ["shortbow", "longbow", "dagger", "dart"]:  # Finesse/ranged weapons
            # Use better of STR or DEX
            ability = "dexterity" if self.get_ability_modifier("dexterity") > self.get_ability_modifier("strength") else "strength"

        return self.get_ability_modifier(ability) + self.proficiency_bonus

@dataclass
class GameState:
    num_players: int = 1
    players: List[Player] = field(default_factory=list)
    current_location: str = ""
    environment_description: str = ""
    quest_description: str = ""
    current_enemies: List[str] = field(default_factory=list)
    game_history: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert the game state to a dictionary for API context"""
        return {
            "num_players": self.num_players,
            "players": [vars(p) for p in self.players],
            "current_location": self.current_location,
            "environment_description": self.environment_description,
            "quest_description": self.quest_description,
            "current_enemies": self.current_enemies,
            "game_history": self.game_history[-5:]  # Keep last 5 interactions for context
        }

    def add_to_history(self, event: str):
        """Add an event to the game history"""
        self.game_history.append(event)
        if len(self.game_history) > 20:  # Keep history manageable
            self.game_history.pop(0)

    def save_game(self, filename: str = "game_save.json"):
        """Save the current game state to a file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_game(cls, filename: str = "game_save.json") -> 'GameState':
        """Load a game state from a file"""
        with open(filename, 'r') as f:
            data = json.load(f)

        game_state = cls()
        game_state.num_players = data["num_players"]
        game_state.players = [Player(**p) for p in data["players"]]
        game_state.current_location = data["current_location"]
        game_state.environment_description = data["environment_description"]
        game_state.quest_description = data["quest_description"]
        game_state.current_enemies = data["current_enemies"]
        game_state.game_history = data["game_history"]

        return game_state