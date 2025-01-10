"""
Text formatting utilities for console output
"""
from colorama import init, Fore, Back, Style
import textwrap
import os

# Initialize colorama for cross-platform color support
init()

class TextFormatter:
    """Handles text formatting and coloring for console output"""

    # Color schemes
    COLORS = {
        'header': Fore.BLUE,
        'success': Fore.GREEN,
        'error': Fore.RED,
        'warning': Fore.YELLOW,
        'info': Fore.CYAN,
        'reset': Style.RESET_ALL
    }

    @staticmethod
    def wrap_text(text: str, width: int = 80) -> str:
        """Wrap text to specified width"""
        return textwrap.fill(text, width=width)

    @staticmethod
    def gm_speech(text: str) -> str:
        """Format Game Master's speech"""
        wrapped = TextFormatter.wrap_text(text)
        return f"{Fore.CYAN}{wrapped}{Style.RESET_ALL}"

    @staticmethod
    def system_message(text: str) -> str:
        """Format system messages"""
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

    @staticmethod
    def player_speech(player_name: str, text: str) -> str:
        """Format player speech"""
        return f"{Fore.GREEN}{player_name}: {Fore.WHITE}{text}{Style.RESET_ALL}"

    @staticmethod
    def dice_roll(text: str) -> str:
        """Format dice roll results"""
        return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"

    @staticmethod
    def combat_text(text: str) -> str:
        """Format combat-related text"""
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    @staticmethod
    def success_text(text: str) -> str:
        """Format success messages"""
        return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

    @staticmethod
    def failure_text(text: str) -> str:
        """Format failure messages"""
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    @staticmethod
    def header(text: str) -> str:
        """Format section headers"""
        width = os.get_terminal_size().columns
        padded_text = f" {text} "
        padding = "=" * ((width - len(padded_text)) // 2)
        header = padding + padded_text + padding
        return f"\n{Fore.BLUE}{header}{Style.RESET_ALL}\n"

    @staticmethod
    def menu_option(key: str, description: str = "") -> str:
        """Format menu options"""
        if description:
            return f"{Fore.YELLOW}{key}{Style.RESET_ALL}: {description}"
        return f"{Fore.YELLOW}{key}{Style.RESET_ALL}"

    @staticmethod
    def player_status(player_name: str, status: str) -> str:
        """Format player status"""
        return f"{Fore.CYAN}{player_name}{Style.RESET_ALL} - {status}"

    @staticmethod
    def stat_display(stat_name: str, value: int, modifier: int = None) -> str:
        """Format stat display"""
        if modifier is not None:
            return f"{Fore.CYAN}{stat_name}: {value} ({'+' if modifier >= 0 else ''}{modifier}){Style.RESET_ALL}"
        return f"{Fore.CYAN}{stat_name}: {value}{Style.RESET_ALL}"

    @staticmethod
    def spell_text(text: str) -> str:
        """Format spell-related text"""
        return f"{Fore.BLUE}{text}{Style.RESET_ALL}"

    @staticmethod
    def condition_text(condition: str, text: str) -> str:
        """Format condition effects"""
        return f"{Fore.RED}{condition}: {Fore.YELLOW}{text}{Style.RESET_ALL}"

    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')