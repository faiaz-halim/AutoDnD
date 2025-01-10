SYSTEM_PROMPT = """You are an experienced Dungeons & Dragons Game Master.
You create immersive and engaging adventures while following D&D 5e rules.
Keep responses concise but descriptive. Make decisions based on game rules and dice rolls.
Maintain consistency with previous events and descriptions.
When dice rolls are needed, specify the type (e.g., 'Roll a d20 for perception check').
"""

def generate_environment_prompt(num_players: int) -> str:
    return f"""As a D&D Game Master, generate a random starting environment and quest for {num_players} players.
Include:
1. Starting location name and brief description
2. Basic quest or mission
3. Current situation or immediate challenge
Keep it concise but engaging. Use standard D&D 5e settings and themes."""

def generate_action_context(game_state: dict) -> str:
    return f"""Current game state:
Location: {game_state['current_location']}
Environment: {game_state['environment_description']}
Quest: {game_state['quest_description']}
Recent history: {' -> '.join(game_state['game_history'][-3:])}

Consider this context for your next response. Stay consistent with established elements."""

def format_player_action(action: str, game_state: dict) -> str:
    return f"""Player action: {action}

Current context:
{generate_action_context(game_state)}

Respond as the Game Master, describing the outcome of this action.
If dice rolls are needed, specify them clearly.
Stay consistent with the established narrative and D&D 5e rules."""