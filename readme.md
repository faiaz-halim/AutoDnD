# D&D Command Line Adventure

A text-based Dungeons & Dragons game that uses Ollama's LLM to create an AI Game Master and companion experience. Play D&D with AI-controlled party members in an interactive, dynamic environment.

## Features

### Character Creation
- Create characters from all 12 standard D&D 5e classes
- Automatic stat generation using 4d6 drop lowest method
- Class-appropriate skill proficiencies and starting equipment
- Detailed character stats and abilities

### AI Companions
- 2-3 AI-controlled party members
- Class-appropriate behavior and responses
- Interactive party dynamics
- Context-aware actions and suggestions

### Combat System
- Turn-based combat following D&D 5e rules
- Automatic dice rolling and modifier calculation
- Combat conditions and status effects
- Weapon and spell damage calculations

### Game Features
- Dynamic environment generation
- Interactive storytelling
- Save/load game functionality
- Colored text interface
- Natural language input processing

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally (with llama3.2 model)
- Terminal with color support

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dnd-game
```

2. Create a virtual environment:
```bash
python -m venv venv
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

## Usage

1. Start the game:
```bash
python main.py
```

2. Follow the character creation prompts to create your character.

3. The game will generate AI companions and start your adventure.

### Available Commands

- `quit`: End the game
- `save`: Save your current progress
- `help`: Show available commands and tips
- `status`: Show your character's current stats

### Action Examples

- Combat: `I attack the goblin with my sword`
- Exploration: `I search the room for traps`
- Social: `I try to persuade the merchant to lower their prices`
- Skills: `I attempt to climb the wall`

## Project Structure

```
dnd_game/
├── src/
│   ├── ai/              # AI companion behavior
│   ├── character/       # Character creation and management
│   ├── combat/          # Combat system
│   ├── utils/           # Utilities and helpers
│   ├── game_master.py   # Main game orchestrator
│   └── game_state.py    # Game state management
```

## Game Mechanics

### Character Classes
- All standard D&D 5e classes supported
- Class-specific abilities and proficiencies
- Unique starting equipment and features

### Combat
- Initiative system
- Attack rolls with advantage/disadvantage
- Damage calculations
- Status effects and conditions

### Skill System
- Ability checks
- Skill proficiencies
- Saving throws
- Special ability usage

## Development

### Adding New Features

1. Character Classes:
   - Add new classes in `character/classes.py`
   - Define class features and proficiencies

2. Combat Actions:
   - Add new actions in `combat/actions.py`
   - Define validation rules in `combat/validation.py`

3. AI Behaviors:
   - Add responses in `ai/responses.py`
   - Define actions in `ai/actions.py`

### Running Tests
```bash
# TODO: Add testing instructions
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on Dungeons & Dragons 5th Edition
- Uses Ollama's implementation of LLaMA3.2 for AI interactions
- Inspired by classic text adventure games

## TODO

- [ ] Add more character classes and features
- [ ] Implement inventory management system
- [ ] Add spellcasting system
- [ ] Create character leveling system
- [ ] Add more complex combat scenarios
- [ ] Implement character progression
- [ ] Add quest tracking system
- [ ] Create campaign management tools