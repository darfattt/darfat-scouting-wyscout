"""
Domain knowledge for football scouting
"""

COMPOSITE_ATTRIBUTES_EXPLANATIONS = {
    'Security': {
        'tactical_significance': 'Ability to retain possession under pressure',
        'when_important': 'Building from back, playing out from defense',
        'key_metrics': ['Accurate short/medium passes', 'Successful dribbles', 'Duels won'],
        'archetypes': ['William Saliba', 'Manuel Akanji', 'Lucas Beraldo']
    },
    'ProgPass': {
        'tactical_significance': 'Progressing possession through forward passing',
        'when_important': 'Ball-playing defenders, playmakers',
        'key_metrics': ['Progressive passes', 'Accurate forward passes', 'Smart passes'],
        'archetypes': ['Nico Schlotterbeck', 'Dayot Upamecano', 'Jan Paul Van Hecke']
    },
    'BallCarrying': {
        'tactical_significance': 'Dribbling and carrying ball up the pitch',
        'when_important': 'Wide CBs, wingbacks, transition play',
        'key_metrics': ['Progressive runs', 'Accelerations', 'Successful dribbles'],
        'archetypes': ['Arthur Theate', 'Oumar Solet', 'Noussair Mazraoui']
    },
    'Creativity': {
        'tactical_significance': 'Creating chances through passing',
        'when_important': 'Attacking fullbacks, playmaking defenders',
        'key_metrics': ['Shot assists', 'Smart passes', 'Passes to penalty area'],
        'archetypes': ['Alessandro Bastoni', 'Facundo Medina', 'Lisandro Martinez']
    },
    'Finishing': {
        'tactical_significance': 'Taking chances efficiently near goal',
        'when_important': 'Inside forwards, strikers, poachers',
        'key_metrics': ['Goal conversion', 'Shots on target', 'Non-penalty goals per 90'],
        'archetypes': ['Jamal Musiala', 'Ousman Dembélé', 'Kevin Schade']
    },
    'BoxPresence': {
        'tactical_significance': 'Occupying the penalty area to receive chances',
        'when_important': 'Target strikers, shadow strikers, false nines',
        'key_metrics': ['Touches in box', 'xG per 90', 'Goals per 90'],
        'archetypes': ['Ademola Lookman', 'Zakaria Aboukhlal', 'Ismaila Sarr']
    }
}

ROLE_EXPLANATIONS = {
    'Ball Playing CB': {
        'description': 'Comfortable in possession, builds play from back',
        'key_attributes': ['Security', 'ProgPass', 'BallCarrying'],
        'tactical_role': 'Starts attacks, progresses play through passing'
    },
    'Sweeper': {
        'description': 'Covers behind defensive line, cleans up danger',
        'key_attributes': ['ProactiveDefending', 'BoxDefending', 'Security'],
        'tactical_role': 'Deep defender who intercepts and clears'
    },
    'Poacher': {
        'description': 'Finishes chances inside the box',
        'key_attributes': ['Finishing', 'BoxPresence', 'Movement'],
        'tactical_role': 'Scores goals from close range'
    },
    'Regista': {
        'description': 'Creative deep-lying playmaker',
        'key_attributes': ['Creativity', 'ProgPass', 'Dictating'],
        'tactical_role': 'Combines ball progression with defensive discipline'
    }
}

POSITION_GUIDELINES = {
    'CB': {
        'primary_focus': 'Defending + Ball progression',
        'key_composite_attrs': ['Security', 'ProgPass', 'BoxDefending'],
        'tactical_importance': 'Stop attacks, build from back'
    },
    'DM': {
        'primary_focus': 'Ball winning + Distribution',
        'key_composite_attrs': ['Destroying', 'BallWinning', 'Dictating'],
        'tactical_importance': 'Protect backline, start attacks'
    },
    'CM': {
        'primary_focus': 'Ball progression + Pressing',
        'key_composite_attrs': ['Creativity', 'BallCarrying', 'Pressing'],
        'tactical_importance': 'Connect defense to attack'
    },
    'AM': {
        'primary_focus': 'Chance creation + Finishing',
        'key_composite_attrs': ['Creativity', 'Finishing', 'OneOnOneAbility'],
        'tactical_importance': 'Create and score chances'
    },
    'CF': {
        'primary_focus': 'Finishing + Box presence',
        'key_composite_attrs': ['Finishing', 'BoxPresence', 'LinkPlay'],
        'tactical_importance': 'Score goals'
    },
    'Winger': {
        'primary_focus': 'Wide chance creation + 1v1',
        'key_composite_attrs': ['WideCreation', 'OneOnOneAbility', 'BallCarrying'],
        'tactical_importance': 'Beat defenders, create chances wide'
    }
}

METRIC_DEFINITIONS = {
    'xG per 90': {
        'definition': 'Expected Goals per 90 minutes',
        'what_it_measures': 'Quality of shot selection and finishing',
        'good_range': '>0.7 (excellent), 0.5-0.7 (very good), 0.3-0.5 (good)',
        'context': 'Compare across positions, higher for attackers'
    },
    'xA per 90': {
        'definition': 'Expected Assists per 90 minutes',
        'what_it_measures': 'Chance creation ability',
        'good_range': '>0.4 (excellent), 0.25-0.4 (very good), 0.15-0.25 (good)',
        'context': 'Higher for creative players, midfielders, AMs'
    },
    'Progressive passes per 90': {
        'definition': 'Passes that move the ball towards goal',
        'what_it_measures': 'Ball progression ability',
        'good_range': '>8 (excellent), 5-8 (very good), 3-5 (good)',
        'context': 'High for ball-playing defenders, playmakers'
    },
    'Duels won, %': {
        'definition': 'Percentage of duels (1v1 situations) won',
        'what_it_measures': 'Physical dominance and technical ability',
        'good_range': '>60% (excellent), 55-60% (very good), 50-55% (good)',
        'context': 'Important for defenders, defensive midfielders'
    },
    'Touches in box per 90': {
        'definition': 'Number of touches inside penalty area per 90 minutes',
        'what_it_measures': 'Goal-scoring positioning',
        'good_range': '>6 (excellent), 4-6 (very good), 2-4 (good)',
        'context': 'High for strikers, wingers, attacking midfielders'
    }
}
