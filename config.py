"""
Game configuration - Champion stats, terrain layouts, and spawn positions
"""
from constants import Assets

# Team spawn positions
TEAM_POSITIONS = {
    "blue": [(3, 15), (4, 16)],
    "red": [(15, 2), (17, 4)]
}

# Respawn locations (indexed by unit position in units list)
RESPAWN_LOCATIONS = {
    0: (3, 15),   # Blue player 1
    1: (4, 16),   # Blue player 2
    2: (15, 2),   # Red player 1
    3: (17, 4)    # Red player 2
}

# Champion definitions
CHAMPIONS = {
    "Garen": {
        "health": 900,
        "damage": 80,
        "physical_defense": 50,
        "magical_defense": 50,
        "crit_chance": 20,
        "mana": 220,
        "move_range": 3,
        "attack_range": 2,
        "image": Assets.GAREN,
        "abilities": [
            {
                "type": "DamageHealAbility",
                "name": "Slash",
                "mana_cost": 30,
                "cooldown": 5,
                "ability_type": "damage",
                "attack": 90,
                "description": "A quick slash attack.",
                "attack_radius": 4,
                "is_aoe": 1,
                "damage_type": "magical"
            },
            {
                "type": "BuffAbility",
                "name": "Fortify",
                "mana_cost": 20,
                "cooldown": 14,
                "defense": 50,
                "description": "Increases defense temporarily for 3 turns.",
                "attack_radius": 8
            },
            {
                "type": "DamageHealAbility",
                "name": "Charge",
                "mana_cost": 40,
                "cooldown": 8,
                "ability_type": "damage",
                "attack": 300,
                "description": "A powerful charging attack that stuns the target.",
                "attack_radius": 2
            }
        ]
    },
    "Ashe": {
        "health": 500,
        "damage": 120,
        "physical_defense": 10,
        "magical_defense": 30,
        "crit_chance": 50,
        "mana": 150,
        "move_range": 4,
        "attack_range": 3,
        "image": Assets.ASHE,
        "abilities": [
            {
                "type": "DamageHealAbility",
                "name": "Arrow Shot",
                "mana_cost": 20,
                "cooldown": 5,
                "ability_type": "damage",
                "attack": 150,
                "description": "Shoots an arrow at the target."
            },
            {
                "type": "DebuffAbility",
                "name": "Frost Arrow",
                "mana_cost": 30,
                "cooldown": 10,
                "attack": 20,
                "defense": 10,
                "description": "Slows and weakens the target.",
                "attack_radius": 5
            },
            {
                "type": "BuffAbility",
                "name": "Healing Wind",
                "mana_cost": 50,
                "cooldown": 15,
                "defense": 20,
                "description": "Restores health to an ally and grants temporary defense.",
                "attack_radius": 3
            }
        ]
    },
    "Darius": {
        "health": 700,
        "damage": 90,
        "physical_defense": 50,
        "magical_defense": 50,
        "crit_chance": 50,
        "mana": 120,
        "move_range": 3,
        "attack_range": 2,
        "image": Assets.DARIUS,
        "abilities": [
            {
                "type": "DamageHealAbility",
                "name": "Decimate",
                "mana_cost": 50,
                "cooldown": 7,
                "ability_type": "damage",
                "attack": 250,
                "description": "Spins his axe, dealing damage to nearby enemies."
            },
            {
                "type": "DebuffAbility",
                "name": "Crippling Strike",
                "mana_cost": 40,
                "cooldown": 8,
                "attack": 30,
                "defense": 10,
                "description": "A heavy strike that slows and weakens the target."
            },
            {
                "type": "DamageHealAbility",
                "name": "Noxian Guillotine",
                "mana_cost": 80,
                "cooldown": 15,
                "ability_type": "damage",
                "attack": 400,
                "description": "Executes an enemy with low health."
            }
        ]
    },
    "Soraka": {
        "health": 490,
        "damage": 50,
        "physical_defense": 50,
        "magical_defense": 33,
        "crit_chance": 50,
        "mana": 250,
        "move_range": 4,
        "attack_range": 3,
        "image": Assets.SORAKA,
        "abilities": [
            {
                "type": "DamageHealAbility",
                "name": "Starcall",
                "mana_cost": 30,
                "cooldown": 5,
                "ability_type": "damage",
                "attack": 50,
                "description": "Calls a star down, dealing magic damage.",
                "is_aoe": 2,
                "damage_type": "magical"
            },
            {
                "type": "DamageHealAbility",
                "name": "Astral Infusion",
                "mana_cost": 40,
                "cooldown": 8,
                "ability_type": "heal",
                "attack": 100,
                "description": "Sacrifices own health to heal an ally."
            },
            {
                "type": "BuffAbility",
                "name": "Wish",
                "mana_cost": 100,
                "cooldown": 20,
                "defense": 30,
                "description": "Restores health to all allies and grants defense for 3 turns."
            }
        ]
    },
    "Rengar": {
        "health": 500,
        "damage": 190,
        "physical_defense": 0,
        "magical_defense": 0,
        "crit_chance": 30,
        "mana": 150,
        "move_range": 4,
        "attack_range": 1,
        "image": Assets.RENGAR,
        "abilities": [
            {
                "type": "DamageHealAbility",
                "name": "Savagery",
                "mana_cost": 50,
                "cooldown": 5,
                "ability_type": "damage",
                "attack": 300,
                "description": "Empowered strike dealing extra damage.",
                "attack_radius": 4
            },
            {
                "type": "BuffAbility",
                "name": "Battle Roar",
                "mana_cost": 40,
                "cooldown": 8,
                "defense": 40,
                "description": "Boosts defense and regenerates health."
            },
            {
                "type": "DebuffAbility",
                "name": "Thrill of the Hunt",
                "mana_cost": 80,
                "cooldown": 20,
                "attack": 20,
                "description": "Tracks the enemy, reducing their attack temporarily."
            }
        ]
    }
}

# Monster definitions
MONSTERS = [
    {
        "x": 11, "y": 19, "name": "BigBuff",
        "health": 1000, "damage": 50,
        "physical_defense": 0, "magical_defense": 0, "crit_chance": 0,
        "image": Assets.BIG_BUFF,
        "move_range": 3, "attack_range": 2
    },
    {
        "x": 9, "y": 1, "name": "BigBuff",
        "health": 1000, "damage": 50,
        "physical_defense": 0, "magical_defense": 0, "crit_chance": 0,
        "image": Assets.BIG_BUFF,
        "move_range": 3, "attack_range": 2
    },
    {
        "x": 10, "y": 10, "name": "BigBuff",
        "health": 1000, "damage": 50,
        "physical_defense": 0, "magical_defense": 0, "crit_chance": 0,
        "image": Assets.BIG_BUFF,
        "move_range": 3, "attack_range": 2
    },
    {
        "x": 5, "y": 7, "name": "BlueBuff",
        "health": 390, "damage": 150,
        "physical_defense": 20, "magical_defense": 30, "crit_chance": 0,
        "image": Assets.BLUE_BUFF,
        "move_range": 3, "attack_range": 2
    },
    {
        "x": 15, "y": 13, "name": "RedBuff",
        "health": 390, "damage": 150,
        "physical_defense": 30, "magical_defense": 0, "crit_chance": 0,
        "image": Assets.RED_BUFF,
        "move_range": 3, "attack_range": 2
    }
]

# Base (Nexus) definitions
BASES = [
    {
        "x": 1, "y": 19, "name": "NexusBlue",
        "health": 2500, "damage": 50,
        "physical_defense": 0, "magical_defense": 0, "crit_chance": 0,
        "image": Assets.NEXUS_BLUE,
        "color": "blue"
    },
    {
        "x": 19, "y": 1, "name": "NexusRed",
        "health": 2500, "damage": 50,
        "physical_defense": 0, "magical_defense": 0, "crit_chance": 0,
        "image": Assets.NEXUS_RED,
        "color": "red"
    }
]

# Terrain layout
TERRAIN_LAKES = [
    [(5, 5), (5, 6), (6, 5), (6, 6), (7, 6)],
    [(10, 7), (11, 6), (11, 7), (12, 6), (12, 7)],
    [(8, 13), (9, 13), (8, 14), (9, 14), (10, 13)],
    [(13, 14), (14, 14), (14, 15), (15, 14), (15, 15)]
]

TERRAIN_HILLS = [
    [(2, 4), (2, 5), (2, 6), (2, 12), (3, 3), (3, 4), (3, 5), (3, 6), (3, 10), (3, 11), (3, 12),
     (3, 13), (3, 14), (4, 3), (5, 3), (5, 8), (5, 10), (5, 12), (6, 3), (6, 8), (6, 9),
     (6, 10), (6, 12), (6, 13), (6, 17), (7, 8), (7, 12), (7, 16), (7, 17), (8, 11), (8, 15), (8, 16), (8, 17),
     (9, 3), (9, 8), (9, 12), (9, 16), (9, 17), (10, 2), (10, 3), (10, 8), (10, 12), (10, 17), (10, 18),
     (11, 3), (11, 4), (11, 8), (11, 12), (11, 17), (12, 3), (12, 4), (12, 5), (12, 9), (13, 3), (13, 4), (13, 8), (13, 12),
     (14, 3), (14, 7), (14, 8), (14, 10), (14, 11), (14, 12), (14, 17), (15, 8), (15, 10), (15, 12), (15, 17), (16, 17),
     (17, 6), (17, 7), (17, 8), (17, 9), (17, 10), (17, 14), (17, 15), (17, 16), (17, 17),
     (18, 8), (18, 14), (18, 15), (18, 16)]
]

TERRAIN_OVERLAYS = {
    "bush": [(0, 0), (1, 0), (0, 1), (20, 20), (19, 20), (20, 19), (3, 7), (3, 8), (8, 3), (17, 12), (17, 13), (12, 17)],
    "barrier": [(0, 17), (1, 17), (2, 17), (3, 17), (3, 18), (3, 19), (3, 20), (17, 0), (17, 1), (17, 2), (17, 3), (18, 3), (19, 3), (20, 3)]
}

# Pickup (Potion) configurations
PICKUP_TYPES = {
    "red_potion": {"rarity": 0.8},
    "blue_potion": {"rarity": 0.8},
    "green_potion": {"rarity": 0.3},
    "golden_potion": {"rarity": 0.2},
    "black_potion": {"rarity": 0.2}
}

# Buff bonuses when killing monsters
MONSTER_BUFF_BONUSES = {
    "BigBuff": {
        "max_health_multiplier": 1.10,
        "damage_multiplier": 1.15
    },
    "other": {
        "max_health_multiplier": 1.05,
        "damage_multiplier": 1.05
    }
}
