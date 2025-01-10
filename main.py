#!/usr/bin/env python3
"""
D&D Command Line Adventure - Main Entry Point
"""
from src.game_master import GameMaster
from src.utils.text_formatter import TextFormatter as Fmt

def main():
    """Main entry point for the game"""
    print(Fmt.header("D&D Command Line Adventure"))
    print(Fmt.system_message("Initializing game..."))

    try:
        # Create and start game
        game_master = GameMaster()
        game_master.start_game()

    except KeyboardInterrupt:
        print(Fmt.system_message("\nGame session ended. Thanks for playing!"))

    except Exception as e:
        print(Fmt.failure_text(f"\nAn error occurred: {str(e)}"))
        print(Fmt.system_message("The game has encountered an unexpected error and must close."))
        raise

if __name__ == "__main__":
    main()