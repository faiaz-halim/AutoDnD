#!/usr/bin/env python3
from src.game_master import GameMaster

def main():
    print("Welcome to D&D Command Line Adventure!")
    print("=====================================")

    try:
        game_master = GameMaster()
        game_master.start_game()
    except KeyboardInterrupt:
        print("\nGame session ended. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()