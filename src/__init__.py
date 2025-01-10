"""
D&D Command Line Adventure Game - A text-based D&D game with AI companions
"""
from .game_master import GameMaster
from .game_state import GameState, Player
from .ollama_client import OllamaClient

__version__ = "1.0.0"
__all__ = ['GameMaster', 'GameState', 'Player', 'OllamaClient']