"""
AI companion action patterns and behavior
"""

CLASS_ACTIONS = {
    'Barbarian': [
        "I enter a rage and prepare to charge",
        "I scan for the strongest enemy to challenge",
        "I position myself to protect the weaker members",
        "I let out a battle cry to intimidate our foes",
        "I grip my weapon tightly, ready to strike"
    ],
    'Bard': [
        "I begin performing an inspiring song",
        "I analyze the situation for a tale worth telling",
        "I prepare a magical melody",
        "I try to diplomatically resolve the situation",
        "I ready a performance to distract our foes"
    ],
    'Cleric': [
        "I call upon divine guidance",
        "I ready healing magic",
        "I channel divine energy",
        "I look for undead to turn",
        "I prepare a blessing for the party"
    ],
    'Druid': [
        "I commune with nature for guidance",
        "I prepare to wild shape if needed",
        "I analyze the natural environment",
        "I look for ways to use the terrain",
        "I listen to the whispers of the wild"
    ],
    'Fighter': [
        "I take a defensive stance",
        "I ready my weapon and assess the situation",
        "I look for tactical advantages",
        "I prepare a combat maneuver",
        "I survey the battlefield for opportunities"
    ],
    'Monk': [
        "I center myself and prepare to strike",
        "I move into a defensive stance",
        "I ready my ki energy",
        "I analyze the enemy's movements",
        "I find my inner balance"
    ],
    'Paladin': [
        "I channel divine power into my weapon",
        "I scan for evil presence",
        "I prepare to smite our foes",
        "I stand ready to protect my allies",
        "I invoke my sacred oath"
    ],
    'Ranger': [
        "I look for tracks and signs",
        "I prepare my bow for combat",
        "I analyze the terrain for advantages",
        "I mark my target for hunting",
        "I check the wind direction"
    ],
    'Rogue': [
        "I look for opportunities to hide",
        "I search for advantageous positions",
        "I prepare for a sneak attack",
        "I analyze potential escape routes",
        "I check for traps or ambush spots"
    ],
    'Sorcerer': [
        "I feel my magic surge within",
        "I prepare a powerful spell",
        "I channel my innate magic",
        "I look for the best spot to cast from",
        "I focus my magical bloodline"
    ],
    'Warlock': [
        "I commune with my patron",
        "I prepare an eldritch blast",
        "I sense for magical opportunities",
        "I invoke my pact magic",
        "I draw upon otherworldly power"
    ],
    'Wizard': [
        "I review my prepared spells",
        "I analyze the magical environment",
        "I prepare a strategic spell",
        "I calculate the best course of action",
        "I consult my spellbook"
    ]
}

CONTEXT_ADDONS = {
    'combat': [
        "while keeping an eye on our surroundings",
        "as I assess the battlefield",
        "preparing for potential threats",
        "with tactical awareness",
        "watching for enemy movements"
    ],
    'exploration': [
        "while watching for dangers",
        "as we explore further",
        "keeping alert for discoveries",
        "with careful attention",
        "noting everything unusual"
    ],
    'social': [
        "while observing the reactions",
        "gauging the situation",
        "reading the atmosphere",
        "considering the implications",
        "watching for social cues"
    ],
    'stealth': [
        "moving as quietly as possible",
        "staying in the shadows",
        "avoiding detection",
        "maintaining silence",
        "blending with surroundings"
    ],
    'investigation': [
        "searching for clues",
        "examining the details",
        "looking for patterns",
        "gathering information",
        "studying the scene"
    ]
}

ENVIRONMENT_ACTIONS = {
    'dungeon': [
        "I check for traps",
        "I listen for echoes",
        "I look for secret doors",
        "I watch the ceiling and walls",
        "I test the floor ahead"
    ],
    'wilderness': [
        "I survey the landscape",
        "I check for animal signs",
        "I find natural shelter",
        "I look for fresh water",
        "I identify useful plants"
    ],
    'urban': [
        "I observe the crowd",
        "I look for escape routes",
        "I identify important buildings",
        "I listen for rumors",
        "I watch for guards"
    ],
    'underwater': [
        "I check water currents",
        "I look for air pockets",
        "I watch for aquatic life",
        "I gauge water pressure",
        "I search for safe passages"
    ]
}