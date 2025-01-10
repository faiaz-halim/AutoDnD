"""
System prompts and templates for LLM interaction
"""

SYSTEM_PROMPT = """You are an experienced Dungeons & Dragons Game Master.
Your role is to create an immersive and engaging adventure while following D&D 5e rules.
Keep responses concise but descriptive. Make decisions based on game rules and dice rolls.
Maintain consistency with previous events and descriptions.
When dice rolls are needed, specify the type (e.g., 'Roll a d20 for perception check').

Current adventure style: Classic fantasy with elements of exploration and combat.
Tone: Balanced between serious and light-hearted.
Rule enforcement: Moderate - follow core rules but prioritize fun and flow."""

def generate_environment_prompt(num_players: int) -> str:
    """Generate prompt for initial environment creation"""
    return f"""As a D&D Game Master, generate a starting environment and quest for {num_players} players.
Include:
1. Starting location name and brief description
2. Basic quest or mission
3. Current situation or immediate challenge
4. At least one NPC the party can interact with
5. A potential combat encounter
Keep it concise but engaging. Use standard D&D 5e settings and themes."""

def format_player_action(action: str, game_state: dict) -> str:
    """Format player action with game state context"""
    return f"""Current game state:
Location: {game_state['current_location']}
Environment: {game_state['environment_description']}
Quest: {game_state['quest_description']}
Recent history: {' -> '.join(game_state['game_history'][-3:])}

Player action: {action}

Respond as the Game Master, describing the outcome of this action.
If dice rolls are needed, specify them clearly.
Stay consistent with the established narrative and D&D 5e rules."""

def generate_combat_prompt(players: list, enemies: list) -> str:
    """Generate prompt for combat situations"""
    return f"""Combat situation:
Players: {', '.join(p['name'] for p in players)}
Enemies: {', '.join(enemies)}

Describe the tactical situation and options.
Include:
1. Enemy positions and apparent threats
2. Environmental factors that might affect combat
3. Any obvious tactical advantages or disadvantages
Keep combat dynamic and engaging while following D&D 5e combat rules."""

def generate_npc_interaction_prompt(npc_name: str, npc_type: str) -> str:
    """Generate prompt for NPC interactions"""
    return f"""NPC Interaction with {npc_name} ({npc_type})
Provide a realistic and engaging response that:
1. Maintains the NPC's personality and goals
2. Offers relevant information or assistance
3. Creates opportunities for further interaction
4. Stays consistent with previous interactions"""