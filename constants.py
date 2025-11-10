"""
Game constants - All magic numbers and configuration values in one place
"""

# Grid and Screen
GRID_SIZE = 21
CELL_SIZE = 43
SCREEN_WIDTH = CELL_SIZE * GRID_SIZE + 300
SCREEN_HEIGHT = CELL_SIZE * GRID_SIZE + 100
FPS = 60

# Colors (RGB)
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (200, 0, 200)

    # UI Colors
    DARK_GRAY = (30, 30, 30)
    GRAY = (50, 50, 50)
    LIGHT_GRAY = (200, 200, 200)
    GOLD = (200, 156, 56)
    DARK_BLUE = (0, 0, 139)
    CYAN = (0, 191, 255)

    # Team Colors
    BLUE_TEAM = (90, 120, 200)
    RED_TEAM = (255, 90, 90)
    BLUE_TEXT = (10, 10, 200)
    RED_TEXT = (200, 10, 10)

    # Highlight Colors
    MOVE_HIGHLIGHT = (50, 150, 255, 100)
    ATTACK_HIGHLIGHT = (250, 0, 0, 50)
    ABILITY_HIGHLIGHT = (250, 0, 250, 50)

    # Fog of War
    FOG_OVERLAY = (0, 0, 0, 170)
    DIM_OVERLAY = (50, 50, 50, 85)

    # Effects
    FLASH_DAMAGE = (255, 255, 0, 100)
    FLASH_HEAL = (0, 255, 0, 100)

# Gameplay Constants
class Gameplay:
    MOVE_DELAY_MS = 100
    DAMAGE_DISPLAY_DURATION_MS = 1000
    BUFF_ANIMATION_DURATION_MS = 2500
    GAME_OVER_DELAY_MS = 6000
    COUNTDOWN_DELAY_MS = 1000

    # Respawn
    RESPAWN_BASE_TURNS = 8
    RESPAWN_MAX_CAP = 10

    # Pickups
    PICKUP_DESPAWN_TURNS = 15
    PICKUP_SPAWN_MIN_DELAY = 15
    PICKUP_SPAWN_MAX_DELAY = 20
    PICKUP_SPAWN_INITIAL_MIN = 5
    PICKUP_SPAWN_INITIAL_MAX = 8
    MAX_PICKUPS = 10

    # Keys
    KEYS_REQUIRED_TO_BREAK_BARRIER = 3
    MONSTER_RESPAWN_TURN_INTERVAL = 20

    # Regeneration (per turn)
    HEALTH_REGEN_PERCENT = 0.005  # 0.5%
    MANA_REGEN_PERCENT = 0.01     # 1%

    # Buff/Debuff
    DEFAULT_BUFF_DURATION = 8
    DEFAULT_DEBUFF_DURATION = 8

    # Vision
    VISIBILITY_RANGE_BONUS = 2  # Beyond movement range

    # Screen Effects
    SCREEN_SHAKE_DURATION_MS = 200  # How long shake lasts
    SCREEN_SHAKE_INTENSITY = 8  # Maximum shake offset in pixels
    FLASH_DURATION_MS = 150  # How long screen flash lasts

# UI Layout
class UI:
    # Info Panel
    INFO_PANEL_WIDTH = 300
    INFO_PANEL_PADDING = 10
    INFO_PANEL_LINE_SPACING = 5
    EVENT_LOG_MAX_EVENTS = 10

    # Abilities Bar
    ABILITIES_BAR_HEIGHT = 100
    ABILITIES_ICON_SIZE = 80

    # Health Bar
    HEALTH_BAR_WIDTH_RATIO = 0.95
    HEALTH_BAR_HEIGHT = 7
    HEALTH_BAR_MARGIN = 2
    HEALTH_BAR_BORDER_RADIUS = 3
    HEALTH_BAR_BORDER_THICKNESS = 1
    HEALTH_BAR_ANIMATION_SPEED = 0.15  # How fast bars animate (0-1, higher = faster)
    HEALTH_SEGMENT_SIZE = 100  # HP per segment marker

    # Key Display
    KEY_ICON_SIZE = 30
    UNIT_ICON_SIZE_RATIO = 3/4  # Ratio to CELL_SIZE

    # Damage Text
    DAMAGE_TEXT_SIZE = 18
    DAMAGE_TEXT_FADE_RATE = 4
    DAMAGE_TEXT_RISE_RATE = 40

    # Arrow Indicators (buff/debuff)
    ARROW_SIZE = 10
    BUFF_ARROW_OFFSET_X = CELL_SIZE // 5
    DEBUFF_ARROW_OFFSET_X = CELL_SIZE - 7

# Asset Paths
class Assets:
    # Fonts
    FONT_TITLE = "assets/League.otf"
    FONT_RUSSO = "assets/RussoOne.ttf"

    # Images - Terrain
    GRASS = "assets/grass_new.png"
    WATER = "assets/water.jpg"
    ROCK = "assets/new_rock.png"
    BUSH = "assets/bush.png"
    BARRIER = "assets/inhibetor.png"

    # Images - Units
    ASHE = "assets/ashe.png"
    GAREN = "assets/garen.png"
    DARIUS = "assets/darius.png"
    SORAKA = "assets/soraka.png"
    RENGAR = "assets/rengar.png"
    BLUE_BUFF = "assets/BlueBuff.png"
    RED_BUFF = "assets/Redbuff.png"
    BIG_BUFF = "assets/BigBuff.png"
    NEXUS_BLUE = "assets/Nexus_Blue.png"
    NEXUS_RED = "assets/Nexus_Red.png"

    # Images - Indicators
    INDICATOR = "assets/indicator.png"
    INDICATOR1 = "assets/indicator1.jpg"
    RED_SQUARE = "assets/redsquare.png"

    # Images - Potions
    RED_POTION = "assets/red_potion.png"
    BLUE_POTION = "assets/blue_potion.png"
    GREEN_POTION = "assets/green_potion.png"
    GOLDEN_POTION = "assets/golden_potion.png"
    BLACK_POTION = "assets/black_potion.png"

    # Images - Backgrounds
    MAIN_SCREEN = "assets/main_screen.jpg"
    LOL_BACKGROUND = "assets/lol_background.jpg"
    CHAMP_SELECT = "assets/champ_select.jpg"
    GAME_OVER = "assets/game_over_image.jpg"

    # Images - Keys
    RED_KEY = "assets/red_key.png"
    BLUE_KEY = "assets/blue_key.png"

    # Sounds - Movement
    MOVING = "sounds/moving.mp3"
    WATER_SOUND = "sounds/water.mp3"

# Audio Volume Settings
class Volume:
    MUSIC_DEFAULT = 0.03
    SELECTION = 0.5
    MOVEMENT = 0.2
    FADE_STEP = 0.01
    FADE_DELAY_MS = 10
