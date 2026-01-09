"""
Composite attribute definitions for defender analysis
Each attribute is calculated from weighted combinations of statistical metrics
Focused exclusively on defender scouting and evaluation
"""

COMPOSITE_ATTRIBUTES = {
    "Security": {
        "display_name": "Security",
        "description": "Retain possession under pressure through passing and ball carrying. Focus on quality and safety of passing, with evasiveness and retention when dribbling. Key for a sweeper defender who acts as a safe passing option.",
        "archetypes": ["William Saliba", "Manuel Akanji", "Lucas Beraldo"],
        "components": [
            {"stat": "Accurate short / medium passes, %", "weight": 0.28, "use_percentile": True},
            {"stat": "Accurate passes, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Successful dribbles, %", "weight": 0.18, "use_percentile": True},
            {"stat": "Progressive runs per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Duels won, %", "weight": 0.12, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.07, "use_percentile": True},
        ],
        "icon": "🛡️"
    },
    "ProgPass": {
        "display_name": "Prog. Pass",
        "description": "Progress possession through expansive and forward passing. Emphasis on tendency to pass forward, ability to pass through defensive lines or over long distances. Key for a ball playing centre back, tasked with finding midfield and attack during build up play.",
        "archetypes": ["Nico Schlotterbeck", "Dayot Upamecano", "Jan Paul Van Hecke"],
        "components": [
            {"stat": "Progressive passes per 90", "weight": 0.28, "use_percentile": True},
            {"stat": "Accurate forward passes, %", "weight": 0.18, "use_percentile": True},
            {"stat": "Accurate long passes, %", "weight": 0.18, "use_percentile": True},
            {"stat": "Smart passes per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Passes to final third per 90", "weight": 0.12, "use_percentile": True},
            {"stat": "Average pass length, m", "weight": 0.09, "use_percentile": True},
        ],
        "icon": "⚡"
    },
    "BallCarrying": {
        "display_name": "Ball Carrying",
        "description": "Dribble and carry ball up pitch, exploiting space presented and bypassing opposing defenders. Take on ability is part of responsibility but not focus, focus is more on driving into space ahead of player. Key for a wide centre back who is afforded space in inside channels.",
        "archetypes": ["Arthur Theate", "Oumar Solet", "Noussair Mazraoui"],
        "components": [
            {"stat": "Progressive runs per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Accelerations per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Successful dribbles, %", "weight": 0.22, "use_percentile": True},
            {"stat": "Duels won, %", "weight": 0.15, "use_percentile": True},
            {"stat": "Offensive duels won, %", "weight": 0.08, "use_percentile": True},
        ],
        "icon": "🏃"
    },
    "Creativity": {
        "display_name": "Creativity",
        "description": "Create chances for their team, primarily through passing. Vital that player can penetrate box with passes and crosses, execute final ball well, and receive ball in final third. Key for a wide centre back who takes up advanced positions in possession.",
        "archetypes": ["Alessandro Bastoni", "Facundo Medina", "Lisandro Martinez"],
        "components": [
            {"stat": "Shot assists per 90", "weight": 0.22, "use_percentile": True},
            {"stat": "Smart passes per 90", "weight": 0.18, "use_percentile": True},
            {"stat": "Passes to penalty area per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Passes to final third per 90", "weight": 0.13, "use_percentile": True},
            {"stat": "Deep completions per 90", "weight": 0.12, "use_percentile": True},
            {"stat": "Accurate passes to penalty area, %", "weight": 0.10, "use_percentile": True},
            {"stat": "xA per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🎨"
    },
    "ProactiveDefending": {
        "display_name": "Proactive Defending",
        "description": "Aggressively win ball back from opponent, stepping onto forward and proactively regaining possession. Tackling high up pitch, duelling well and attacking space is key. Key for a centre back holding a high defensive line, allowing their team to press.",
        "archetypes": ["Marcos Senesi", "Sead Kolašinac", "Isak Hien"],
        "components": [
            {"stat": "Duels won, %", "weight": 0.28, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.22, "use_percentile": True},
            {"stat": "Defensive duels per 90", "weight": 0.18, "use_percentile": True},
            {"stat": "Defensive duels won, %", "weight": 0.15, "use_percentile": True},
            {"stat": "PAdj Sliding tackles", "weight": 0.12, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.05, "use_percentile": True},
        ],
        "icon": "⚔️"
    },
    "Duelling": {
        "display_name": "Duelling",
        "description": "Duel effectively with opposing forward, both on ground and in air. A simple focus on duel volume and success, using physical strength and technique to dominate 50/50 situations. Key for many roles, such as wide defenders, sweepers or aggressors.",
        "archetypes": ["Yerry Mina", "Willi Orban", "Harry Maguire"],
        "components": [
            {"stat": "Duels won, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Defensive duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Aerial duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Aerial duels per 90", "weight": 0.12, "use_percentile": True},
            {"stat": "Duels per 90", "weight": 0.08, "use_percentile": True},
        ],
        "icon": "💪"
    },
    "BoxDefending": {
        "display_name": "Box Defending",
        "description": "Defend deep primarily within penalty area, protecting box as opponent attempts to create chances. This involves clearing danger, blocking shot attempts and defending aerially in box. Key for a centre back playing in a deep block style defence.",
        "archetypes": ["James Tarkowski", "Joachim Andersen", "Willi Orban"],
        "components": [
            {"stat": "Shots blocked per 90", "weight": 0.28, "use_percentile": True},
            {"stat": "Aerial duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.22, "use_percentile": True},
            {"stat": "Interceptions per 90", "weight": 0.12, "use_percentile": True},
            {"stat": "Conceded goals per 90", "weight": -0.13, "use_percentile": True},
        ],
        "icon": "🧱"
    },
    "Sweeping": {
        "display_name": "Sweeping",
        "description": "Sweep behind your defensive line, cleaning up any danger that gets past. Emphasis on high quality tackling behind the defensive line and ability to recover ball by protecting space. Often key for a central centre back in a back three, tasked with covering more advanced wide centre backs.",
        "archetypes": ["Stefan de Vrij", "Loïc Bade", "Maxence Lacroix"],
        "components": [
            {"stat": "PAdj Interceptions", "weight": 0.30, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.22, "use_percentile": True},
            {"stat": "Sliding tackles per 90", "weight": 0.18, "use_percentile": True},
            {"stat": "PAdj Sliding tackles", "weight": 0.15, "use_percentile": True},
            {"stat": "Conceded goals per 90", "weight": -0.15, "use_percentile": True},
        ],
        "icon": "🧹"
    }
}
