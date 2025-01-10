# D&D Command Line Adventure

A command-line D&D game that uses Ollama's API to create an AI game master experience.

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally (with llama2 model)
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd dnd-game
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Ensure Ollama is running with llama3.2 model:
```bash
ollama run llama3.2
```

## Running the Game

To start the game, run:
```bash
python main.py
```

## Game Commands

- Type actions in natural language to interact with the game
- `save` - Save your current game progress
- `quit` - Exit the game
- `help` - Show available commands and tips

## Features

- AI-powered game master using llama2
- Dynamic story generation
- Dice rolling system
- Save/load game functionality
- Multiple player support
- D&D 5e rules integration

## Project Structure

```
dnd_game/
├── README.md
├── requirements.txt
├── config/
│   └── game_settings.py
├── src/
│   ├── __init__.py
│   ├── game_master.py
│   ├── ollama_client.py
│   ├── dice.py
│   ├── game_state.py
│   └── prompts.py
└── main.py
```

## Contributing

Feel free to submit issues and enhancement requests!