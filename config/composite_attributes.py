"""
Composite attribute definitions for forward and attacking midfielder analysis
Each attribute is calculated from weighted combinations of statistical metrics
Focused exclusively on forward and attacking midfielder scouting and evaluation
"""

COMPOSITE_ATTRIBUTES = {
    #DF & DM
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
    },
    # ========== AM AND WINGER RESPONSIBILITIES ==========
    
    "Finishing": {
        "display_name": "Finishing",
        "description": "Ability to take chances efficiently. Focus on shooting efficiency when close to goal and shot selection, with a little bit of shot volume. Key for inside forwards who play quite narrow, inside the box.",
        "archetypes": ["Jamal Musiala", "Ousmane Dembélé", "Kevin Schade"],
        "components": [
            {"stat": "Goal conversion, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Shots on target, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Non-penalty goals per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "xG per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Shots per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "⚽"
    },
    
    "BoxPresence": {
        "display_name": "Box Presence",
        "description": "Ability to occupy the box, receiving the ball close to goal and converting this into good quality chances. Heavily influenced by a players preferred zones to play in. Key for players who are effective goalscorers, or play a shadow striker style role.",
        "archetypes": ["Ademola Lookman", "Zakaria Aboukhlal", "Ismaila Sarr"],
        "components": [
            {"stat": "Touches in box per 90", "weight": 0.35, "use_percentile": True},
            {"stat": "xG per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Non-penalty goals per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Goals per 90", "weight": 0.20, "use_percentile": True},
        ],
        "icon": "📦"
    },
    "OneOnOneAbility": {
        "display_name": "1v1 Ability",
        "description": "Ability to dribble past opponents in an isolated 1v1 situation. Efficacy in take ons, ability to convert this into chances for either the player or their teammate. Also attitude towards take ons, how happy are they to carry towards defenders. Key for wingers who often find themselves in 1v1 situations.",
        "archetypes": ["Jeremy Doku", "Jamie Gittens", "Vinicius Júnior"],
        "components": [
            {"stat": "Successful dribbles, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Offensive duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Dribbles per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Offensive duels per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Fouls suffered per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🥋"
    },
    "WINGER_BallCarrying": {
        "display_name": "Ball Carrying (Winger)",
        "description": "Ability to dribble and carry the ball up the pitch, progressing play or catalysing a transition for your team. Take on ability is part of the responsibility but not the focus, the focus is more on driving into space and retaining the ball. Key for industrious wingers who play in transition sides.",
        "archetypes": ["Bukayo Saka", "Francisco Conceição", "Anthony Gordon"],
        "components": [
            {"stat": "Progressive runs per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Accelerations per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Successful dribbles, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Duels won, %", "weight": 0.15, "use_percentile": True},
            {"stat": "Offensive duels won, %", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🏃"
    },
    
    "Movement": {
        "display_name": "Movement",
        "description": "Ability to move well both with and without the ball, to progress play into advanced areas. Off-ball movement is key here, making runs and sprints to find dangerous space and then receiving the ball. Key for players playing alongside a ball-dominant playmaker.",
        "archetypes": ["Alejandro Garnacho", "Yankuba Minteh", "Karim Adeyemi"],
        "components": [
            {"stat": "Accelerations per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Progressive runs per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Touches in box per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Received passes per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Shots per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🔄"
    },
    
    "WideCreation": {
        "display_name": "Wide Creation",
        "description": "Ability to turn possession into chances for your team from wide areas. Primarily focused on take ons and crossing, key elements to a traditional wingers game. Key for wingers who are told to stay wide, rather than moving into narrow areas.",
        "archetypes": ["Michael Olise", "Junya Ito", "Dwight McNeil"],
        "components": [
            {"stat": "Shot assists per 90", "weight": 0.22, "use_percentile": True},
            {"stat": "Crosses per 90", "weight": 0.18, "use_percentile": True},
            {"stat": "Accurate crosses, %", "weight": 0.18, "use_percentile": True},
            {"stat": "Successful dribbles, %", "weight": 0.15, "use_percentile": True},
            {"stat": "xA per 90", "weight": 0.12, "use_percentile": True},
            {"stat": "Key passes per 90", "weight": 0.10, "use_percentile": True},
            {"stat": "Deep completed crosses per 90", "weight": 0.05, "use_percentile": True},
        ],
        "icon": "✨"
    },
    
    "FinalBall": {
        "display_name": "Final Ball",
        "description": "Ability to convert final third possession into chances through passing. Focus on shot-creating actions, box penetration and tendencies around creation. Key for most attacking midfielders, but especially playmakers types.",
        "archetypes": ["Rayan Cherki", "Thomas Müller", "Alex Baena"],
        "components": [
            {"stat": "Shot assists per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Smart passes per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Key passes per 90", "weight": 0.18, "use_percentile": True},
            {"stat": "Passes to penalty area per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "xA per 90", "weight": 0.12, "use_percentile": True},
            {"stat": "Second assists per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🎯"
    },
    
    "BuildUp": {
        "display_name": "Build Up",
        "description": "Ability to contribute to build up and early possession phases. Primarily passing based, focused on ball progression, final third penetration and expansive passing ability. Key for playmakers who tend to drop deeper at times, contributing in early build up.",
        "archetypes": ["Cole Palmer", "Alexsandr Golovin", "Isco"],
        "components": [
            {"stat": "Progressive passes per 90", "weight": 0.22, "use_percentile": True},
            {"stat": "Passes to final third per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Accurate progressive passes, %", "weight": 0.15, "use_percentile": True},
            {"stat": "Smart passes per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Accurate passes, %", "weight": 0.12, "use_percentile": True},
            {"stat": "Passes per 90", "weight": 0.10, "use_percentile": True},
            {"stat": "Average pass length, m", "weight": 0.06, "use_percentile": True},
        ],
        "icon": "🏗️"
    },
    
    "Pressing": {
        "display_name": "Pressing",
        "description": "Ability to contribute defensively, applying pressure to the opponent in order to win possession back. Emphasis on defensive volume and height, winning the ball in the final third of the pitch. Key for any attacking midfielders in a pressing system, or those who play for teams often on the back foot.",
        "archetypes": ["Facundo Buonanotte", "Mikkel Damsgaard", "Antoine Semenyo"],
        "components": [
            {"stat": "Successful defensive actions per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Defensive duels per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Defensive duels won, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Interceptions per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.10, "use_percentile": True},
            {"stat": "PAdj Interceptions", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🔥"
    },
    
    # ========== STRIKER / CF RESPONSIBILITIES ==========
    
    # "CF_Finishing": {
    #     "display_name": "Finishing",
    #     "description": "Ability to take chances efficiently. Focus on shooting efficiency when close to goal and shot selection, with a little bit of shot volume. Key for any goalscoring forward, but especially poachers.",
    #     "archetypes": ["Kylian Mbappé", "Mika Biereth", "Nick Woltemade"],
    #     "components": [
    #         {"stat": "Goal conversion, %", "weight": 0.30, "use_percentile": True},
    #         {"stat": "Shots on target, %", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Non-penalty goals per 90", "weight": 0.20, "use_percentile": True},
    #         {"stat": "xG per 90", "weight": 0.15, "use_percentile": True},
    #         {"stat": "Shots per 90", "weight": 0.10, "use_percentile": True},
    #     ],
    #     "icon": "⚽"
    # },
    
    # "CF_BoxPresence": {
    #     "display_name": "Box Presence",
    #     "description": "Ability to occupy the box, receiving the ball close to goal and converting this into good quality chances. Heavily influenced by a players preferred zones to play in. Key for poachers primarily, though it's a beneficial trait for most.",
    #     "archetypes": ["Alexandre Lacazette", "Erling Haaland", "Artem Dovbyk"],
    #     "components": [
    #         {"stat": "Touches in box per 90", "weight": 0.35, "use_percentile": True},
    #         {"stat": "xG per 90", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Non-penalty goals per 90", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Goals per 90", "weight": 0.20, "use_percentile": True},
    #     ],
    #     "icon": "📦"
    # },
    
    # "CF_Movement": {
    #     "display_name": "Movement",
    #     "description": "Ability to move well both with and without the ball, to progress play into advanced areas. Off-ball movement is key here, making runs and sprints to find dangerous space and then receiving the ball. Key for forwards who run in behind or into channels, and those who play in counter attacking sides.",
    #     "archetypes": ["Ollie Watkins", "Hugo Ekitike", "Loïs Openda"],
    #     "components": [
    #         {"stat": "Accelerations per 90", "weight": 0.30, "use_percentile": True},
    #         {"stat": "Progressive runs per 90", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Touches in box per 90", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Received passes per 90", "weight": 0.15, "use_percentile": True},
    #         {"stat": "Shots per 90", "weight": 0.10, "use_percentile": True},
    #     ],
    #     "icon": "🔄"
    # },
    "LinkPlay": {
        "display_name": "Link Play",
        "description": "Ability to receive the ball in advanced areas or under pressure, before connecting with teammates around them. Focus on quick passing and receiving the ball in the final third. Key for forwards used as an escape route from pressure, often in counter attacking or defensive sides.",
        "archetypes": ["Romelu Lukaku", "Artem Dovbyk", "Randal Kolo Muani"],
        "components": [
            {"stat": "Accurate passes, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Passes to final third per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Received passes per 90", "weight": 0.18, "use_percentile": True},
            {"stat": "Received long passes per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Duels won, %", "weight": 0.12, "use_percentile": True},
            {"stat": "Offensive duels won, %", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🔗"
    },
    # "CF_Creativity": {
    #     "display_name": "Creativity",
    #     "description": "Ability to create chances for others using their final pass. Primarily focused on passes and crosses into the box, to create shooting chances. Key for false nine style forwards who tend to create space for others before exploiting it with a pass.",
    #     "archetypes": ["Harry Kane", "Jonathan Burkardt", "Matthis Abline"],
    #     "components": [
    #         {"stat": "Shot assists per 90", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Passes to penalty area per 90", "weight": 0.22, "use_percentile": True},
    #         {"stat": "xA per 90", "weight": 0.18, "use_percentile": True},
    #         {"stat": "Key passes per 90", "weight": 0.15, "use_percentile": True},
    #         {"stat": "Crosses per 90", "weight": 0.12, "use_percentile": True},
    #         {"stat": "Second assists per 90", "weight": 0.08, "use_percentile": True},
    #     ],
    #     "icon": "🎨"
    # },
    # "CF_BallCarrying": {
    #     "display_name": "Ball Carrying",
    #     "description": "Ability to dribble and carry the ball up the pitch, progressing play or catalysing a transition for your team. Take on ability is part of the responsibility but not the focus, the focus is more on driving into space and retaining the ball. Key for mobile, powerful forwards, who drive forward with the ball, perhaps in a transition side.",
    #     "archetypes": ["Alexander Isak", "Liam Delap", "Marcus Thuram"],
    #     "components": [
    #         {"stat": "Progressive runs per 90", "weight": 0.30, "use_percentile": True},
    #         {"stat": "Accelerations per 90", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Successful dribbles, %", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Duels won, %", "weight": 0.15, "use_percentile": True},
    #         {"stat": "Offensive duels won, %", "weight": 0.10, "use_percentile": True},
    #     ],
    #     "icon": "🏃"
    # },
    # "CF_Pressing": {
    #     "display_name": "Pressing",
    #     "description": "Ability to contribute defensively, applying pressure to the opponent in order to win possession back. Emphasis on defensive volume and height, winning the ball in the final third of the pitch. Key for any forwards playing in a pressing system, especially one with a high defensive line.",
    #     "archetypes": ["Tim Kleindienst", "Raúl Jiménez", "Beto"],
    #     "components": [
    #         {"stat": "Successful defensive actions per 90", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Defensive duels per 90", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Defensive duels won, %", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Interceptions per 90", "weight": 0.15, "use_percentile": True},
    #         {"stat": "Fouls per 90", "weight": -0.10, "use_percentile": True},
    #         {"stat": "PAdj Interceptions", "weight": 0.10, "use_percentile": True},
    #     ],
    #     "icon": "🔥"
    # }
}
