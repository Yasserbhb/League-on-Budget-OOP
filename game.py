import pygame
import random
from unit import Unit
from interface import Grid, Highlight, Pickup
from sounds import Sounds
from constants import *
from config import TEAM_POSITIONS, RESPAWN_LOCATIONS, MONSTER_BUFF_BONUSES

def load_textures():
    """Load textures for different terrain and overlays."""
    return {
        "grass": pygame.image.load(Assets.GRASS),
        "water": pygame.image.load(Assets.WATER),
        "rock": pygame.image.load(Assets.ROCK),
        "bush": pygame.image.load(Assets.BUSH),
        "barrier": pygame.image.load(Assets.BARRIER),
    }

def load_unit_images():
    """Load unit image paths."""
    return {
        "ashe": Assets.ASHE,
        "garen": Assets.GAREN,
        "darius": Assets.DARIUS,
        "soraka": Assets.SORAKA,
        "rengar": Assets.RENGAR,
        "bluebuff": Assets.BLUE_BUFF,
        "redbuff": Assets.RED_BUFF,
        "bigbuff": Assets.BIG_BUFF,
        "baseblue": Assets.NEXUS_BLUE,
        "basered": Assets.NEXUS_RED
    }

def load_indicators():
    """Load indicator images."""
    return {
        "indicator": pygame.image.load(Assets.INDICATOR),
        "indicator1": pygame.image.load(Assets.INDICATOR1),
        "redsquare": pygame.image.load(Assets.RED_SQUARE),
    }

def load_pickups():
    """Load the different potion types."""
    return {
        "red_potion": pygame.image.load(Assets.RED_POTION),
        "blue_potion": pygame.image.load(Assets.BLUE_POTION),
        "green_potion": pygame.image.load(Assets.GREEN_POTION),
        "golden_potion": pygame.image.load(Assets.GOLDEN_POTION),
        "black_potion": pygame.image.load(Assets.BLACK_POTION),
    }



# Game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("League on Budget")
        self.clock = pygame.time.Clock()
        self.unit_images = load_unit_images()
        self.indicators = load_indicators()
        self.textures_file=load_textures()
        self.pickup=Pickup()
        self.sound=Sounds()
        self.pickup_textures=load_pickups()
        self.grid = Grid(GRID_SIZE, self.textures_file)
        self.units = [] 
        self.pickups=[]

        self.pickup.initialize(self.pickup_textures)  
        self.current_unit_index = 0
        self.last_move_time = 0  # Timestamp of the last movement
        self.visible_tiles = set()
        self.event_log = [] # Initialize event log



        # Initialize main menu
        self.font_title = pygame.font.Font(Assets.FONT_TITLE, 65)
        self.font_small = pygame.font.Font(Assets.FONT_RUSSO, 36)
        self.menu_image = pygame.image.load(Assets.MAIN_SCREEN)
        self.background_image = pygame.image.load(Assets.LOL_BACKGROUND)
        self.champ_select_image = pygame.image.load(Assets.CHAMP_SELECT)
        self.game_over_image = pygame.image.load(Assets.GAME_OVER)

        # Initialize key menu
        self.red_key_img = pygame.image.load(Assets.RED_KEY)
        self.blue_key_img = pygame.image.load(Assets.BLUE_KEY)
        self.font = pygame.font.Font(None, 24)
        
        
        self.key_last_state = {} # prevent repeated actions
        self.current_turn=1

        # Screen effects
        self.screen_shake_start = 0
        self.screen_shake_active = False
        self.screen_flash_start = 0
        self.screen_flash_color = None

        # Particle system
        self.particles = []

        #barrier status
        self.blue_barrier="Up"
        self.red_barrier="Up"





    def main_menu(self):
        """Display the main menu with options to start or quit."""
        menu_running = True
        start_time = pygame.time.get_ticks()

        # Start menu sound
        self.sound.play("game_music")

        while menu_running:
            rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), rect)

            # Pulsing glow effect for title
            elapsed = pygame.time.get_ticks() - start_time
            pulse = (pygame.math.Vector2(1, 0).rotate(elapsed * 0.1).x + 1) / 2  # 0-1 oscillation
            glow_intensity = int(100 + pulse * 155)  # 100-255
            glow_color = (glow_intensity, int(glow_intensity * 0.78), int(glow_intensity * 0.28))

            # Render game title with glow
            title_text = self.font_title.render("League on Budget", True, glow_color)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            title_text1 = self.font_title.render("League on Budget", True, Colors.BLACK)
            title_rect1 = title_text1.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 4 + 2))

            self.screen.blit(title_text1, title_rect1)
            self.screen.blit(title_text, title_rect)

            # Render instructions with hover effect
            mouse_pos = pygame.mouse.get_pos()

            # Check if hovering over Start button
            start_rect_area = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, 300, 40)
            start_color = Colors.GOLD if start_rect_area.collidepoint(mouse_pos) else Colors.LIGHT_GRAY
            start_text = self.font_small.render("Press ENTER to Play", True, start_color)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            # Check if hovering over Quit button
            quit_rect_area = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30, 300, 40)
            quit_color = Colors.RED if quit_rect_area.collidepoint(mouse_pos) else Colors.LIGHT_GRAY
            quit_text = self.font_small.render("Press ESC to Quit", True, quit_color)
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

            self.screen.blit(start_text, start_rect)
            self.screen.blit(quit_text, quit_rect)

            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start the game
                        menu_running = False
                    elif event.key == pygame.K_ESCAPE:  # Quit the game
                        pygame.quit()
                        exit()




    def show_menu(self):
        """Enhanced team selection menu."""
        menu_running = True
        
        # Initialize assets
        font = self.font_title
        small_font = self.font_small

        # Get all units from create_units
        all_units = Unit.create_units(self)

        # Filter player units for selection (those with team=None)
        available_units = [unit for unit in all_units if unit.color is None]

        # Track selected units and predefined positions
        blue_team = []
        red_team = []
        blue_positions = TEAM_POSITIONS["blue"]
        red_positions = TEAM_POSITIONS["red"]
        current_team = "blue"  # Start with Blue's turn
        selected_units = []
        selected_unit_info = None  # Track which unit's details are displayed

        while menu_running:
            rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.screen.blit(pygame.transform.scale(self.champ_select_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), rect)

            # Render the middle section with available units
            y_offset = SCREEN_HEIGHT // 3
            for i, unit in enumerate(available_units):
                color = (
                    Colors.BLUE_TEXT if unit in selected_units and unit.color == "blue" else
                    Colors.RED_TEXT if unit in selected_units and unit.color == "red" else
                    Colors.WHITE
                )

                unit_text = small_font.render(f"{i + 1}: {unit.name}", True, color)
                self.screen.blit(unit_text, (SCREEN_WIDTH // 2 - 50, y_offset))
                y_offset += 40

            # Display currently selected unit's attributes
            if selected_unit_info:
                attributes_text = [
                    f"Name: {selected_unit_info.name}",
                    f"HP: {selected_unit_info.health}",
                    f"ATK: {selected_unit_info.damage}",
                ]
                y_offset = SCREEN_HEIGHT // 3
                for line in attributes_text:
                    attr_text = small_font.render(line, True, Colors.WHITE)
                    self.screen.blit(attr_text, (SCREEN_WIDTH // 2 + 200, y_offset))
                    y_offset += 40
                # Show the selected champion's image larger with glow
                selected_image = pygame.transform.scale(selected_unit_info.image, (150, 150))
                image_x, image_y = SCREEN_WIDTH - 420, y_offset + 30

                # Draw glow effect around selected champion
                glow_surface = pygame.Surface((160, 160), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*Colors.GOLD, 100), (0, 0, 160, 160), border_radius=10)
                self.screen.blit(glow_surface, (image_x - 5, image_y - 5))

                self.screen.blit(selected_image, (image_x, image_y))

            # Render team rosters
            blue_text = font.render("Blue Team", True, Colors.BLUE)
            red_text = font.render("Red Team", True, Colors.RED)
            self.screen.blit(blue_text, (50, 50))
            self.screen.blit(red_text, (SCREEN_WIDTH-400, 50))

            y_offset_blue = 200
            for unit in blue_team:
                unit_text = small_font.render(unit.name, True, Colors.BLUE)
                self.screen.blit(unit_text, (100, y_offset_blue))
                selected_image = pygame.transform.scale(unit.image, (50, 50))
                self.screen.blit(selected_image, (250, y_offset_blue - 10))
                y_offset_blue += 60

            y_offset_red = 200
            for unit in red_team:
                unit_text = small_font.render(unit.name, True, Colors.RED)
                self.screen.blit(unit_text, (SCREEN_WIDTH - 400 + 50, y_offset_red))
                selected_image = pygame.transform.scale(unit.image, (50, 50))
                self.screen.blit(selected_image, (SCREEN_WIDTH - 200, y_offset_red - 10))
                y_offset_red += 60

            pygame.display.flip()

            # Handle menu events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1
                        if 0 <= index < len(available_units):
                            selected_unit_info = available_units[index]  # Show attributes for this unit
                    elif event.key == pygame.K_RETURN and selected_unit_info:
                        self.sound.play("selection")
                        self.sound.set_volume("selection", Volume.SELECTION)
                        if selected_unit_info not in selected_units:
                            # Assign the current team and position to the selected unit
                            if current_team == "blue":
                                selected_unit_info.color = "blue"
                                selected_unit_info.initial_x = blue_positions[len(blue_team)][0]
                                selected_unit_info.initial_y = blue_positions[len(blue_team)][1]
                                selected_unit_info.x = blue_positions[len(blue_team)][0]
                                selected_unit_info.y = blue_positions[len(blue_team)][1]
                                blue_team.append(selected_unit_info)
                                current_team = "red"
                            else:
                                selected_unit_info.color = "red"
                                selected_unit_info.initial_x = red_positions[len(red_team)][0]
                                selected_unit_info.initial_y = red_positions[len(red_team)][1]
                                selected_unit_info.x = red_positions[len(red_team)][0]
                                selected_unit_info.y = red_positions[len(red_team)][1]
                                red_team.append(selected_unit_info)
                                current_team = "blue"
                            selected_units.append(selected_unit_info)
                            selected_unit_info = None
                            # End selection if both teams have 2 units each
                            if len(blue_team) == 2 and len(red_team) == 2:
                                for i in range(3, 0, -1):  # Countdown from 3 to 1
                                    rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
                                    self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), rect)
                                    countdown_text = small_font.render(f"Starting in {i}...", True, Colors.GREEN)
                                    countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                    self.screen.blit(countdown_text, countdown_rect)
                                    pygame.display.flip()
                                    pygame.time.delay(Gameplay.COUNTDOWN_DELAY_MS)
                                # Fade out menu music
                                for volume in reversed([x / 100 for x in range(1, 101)]):
                                    self.sound.set_volume("game_music", volume)
                                    pygame.time.delay(Volume.FADE_DELAY_MS)
                                self.sound.set_volume("game_music", Volume.MUSIC_DEFAULT)
                                self.sound.sounds["game_music"].play(loops=-1)
                                menu_running = False

        # Build self.units in the required order: blue team → red team → monsters
        monsters = [unit for unit in all_units if unit.unit_type == "monster"]
        bases = [unit for unit in all_units if unit.unit_type == "base"]
        self.units = blue_team + red_team + monsters + bases

        return self.units
    



    def log_event(self, message):
        """Add an event to the event log."""
        self.event_log.append(message)
        if len(self.event_log) > UI.EVENT_LOG_MAX_EVENTS:
            self.event_log.pop(0)

    def handle_monster_defeat(self, target, killer):
        """Handle buff acquisition and key transfer when a monster is defeated."""
        if target is None or target.alive or target.unit_type != "monster":
            return

        # Apply team buff
        for unit in self.units:
            if unit.color == killer.color:
                if target.name == "BigBuff":
                    unit.max_health = int(unit.max_health * MONSTER_BUFF_BONUSES["BigBuff"]["max_health_multiplier"])
                    unit.damage = int(unit.damage * MONSTER_BUFF_BONUSES["BigBuff"]["damage_multiplier"])
                else:
                    unit.max_health = int(unit.max_health * MONSTER_BUFF_BONUSES["other"]["max_health_multiplier"])
                    unit.damage = int(unit.damage * MONSTER_BUFF_BONUSES["other"]["damage_multiplier"])

        # Show buff animation
        if target.red_keys == 1:
            Highlight.show_buff_animation(self, self.screen, target.image, "You won a red key + buff")
        elif target.blue_keys == 1:
            Highlight.show_buff_animation(self, self.screen, target.image, "You won a blue key + buff")
        else:
            Highlight.show_buff_animation(self, self.screen, target.image, "You got the Buff")

        # Transfer keys
        self.manage_keys(dead_player=target, killer=killer)




    def draw_info_panel(self):
        """Draw the modern information panel with word wrapping for event log."""
        panel_x = CELL_SIZE * GRID_SIZE
        panel_width = UI.INFO_PANEL_WIDTH
        panel_height = SCREEN_HEIGHT
        padding = UI.INFO_PANEL_PADDING

        # Modern gradient background
        gradient_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        for i in range(panel_width):
            alpha = int(220 - (i / panel_width) * 20)
            pygame.draw.rect(gradient_surface, (20, 25, 35, alpha), (i, 0, 1, panel_height))
        self.screen.blit(gradient_surface, (panel_x, 0))

        # Left accent line
        pygame.draw.rect(self.screen, Colors.GOLD, (panel_x, 0, 3, panel_height))

        # Header section
        header_font = pygame.font.Font(None, 28)
        header_text = header_font.render("BATTLE LOG", True, Colors.GOLD)
        header_shadow = header_font.render("BATTLE LOG", True, (0, 0, 0))
        self.screen.blit(header_shadow, (panel_x + padding + 2, padding + 2))
        self.screen.blit(header_text, (panel_x + padding, padding))

        # Divider line under header
        divider_y = padding + header_text.get_height() + 8
        pygame.draw.line(self.screen, Colors.GOLD, (panel_x + padding, divider_y), (panel_x + panel_width - padding, divider_y), 2)

        # Render event log with modern styling
        font = pygame.font.Font(None, 22)
        y_offset = divider_y + 12
        line_spacing = 8
        max_line_width = panel_width - 2 * padding

        for idx, event in enumerate(reversed(self.event_log)):
            # Fade older events
            event_age = idx
            alpha = max(255 - (event_age * 15), 100)

            # Event background
            event_start_y = y_offset
            words = event.split(" ")
            current_line = ""
            line_count = 0

            # Calculate lines needed
            temp_y = y_offset
            for word in words:
                test_line = f"{current_line} {word}".strip()
                text_surface = font.render(test_line, True, Colors.WHITE)
                if text_surface.get_width() > max_line_width:
                    line_count += 1
                    temp_y += font.get_height() + 4
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                line_count += 1

            # Draw event background
            event_bg_height = line_count * (font.get_height() + 4) + 8
            event_bg = pygame.Surface((panel_width - 2 * padding, event_bg_height), pygame.SRCALPHA)
            event_bg.fill((40, 45, 55, min(alpha, 150)))
            self.screen.blit(event_bg, (panel_x + padding, event_start_y - 4))

            # Draw event text with word wrapping
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                text_surface = font.render(test_line, True, Colors.WHITE)
                if text_surface.get_width() > max_line_width:
                    # Render current line
                    rendered_surface = font.render(current_line, True, (255, 255, 255))
                    rendered_surface.set_alpha(alpha)
                    self.screen.blit(rendered_surface, (panel_x + padding + 5, y_offset))
                    y_offset += font.get_height() + 4
                    current_line = word
                else:
                    current_line = test_line

            # Render last line
            if current_line:
                rendered_surface = font.render(current_line, True, (255, 255, 255))
                rendered_surface.set_alpha(alpha)
                self.screen.blit(rendered_surface, (panel_x + padding + 5, y_offset))
                y_offset += font.get_height() + 4

            y_offset += line_spacing

            # Stop if panel is full
            if y_offset > panel_height - padding - 50:
                break


    def draw_abilities_bar(self):
        """Draw the abilities bar and HUD for the current unit at the bottom of the screen."""
        # Bar dimensions
        bar_height = UI.ABILITIES_BAR_HEIGHT
        bar_y = SCREEN_HEIGHT - bar_height
        padding = 10
        icon_size = UI.ABILITIES_ICON_SIZE

        # Modern gradient background for the HUD
        gradient_surface = pygame.Surface((SCREEN_WIDTH, bar_height), pygame.SRCALPHA)
        for i in range(bar_height):
            alpha = int(230 - (i / bar_height) * 30)
            pygame.draw.rect(gradient_surface, (25, 25, 35, alpha), (0, i, SCREEN_WIDTH, 1))
        self.screen.blit(gradient_surface, (0, bar_y))

        # Top accent line
        pygame.draw.rect(self.screen, Colors.GOLD, (0, bar_y, SCREEN_WIDTH, 2))

        # Get the current unit
        current_unit = self.units[self.current_unit_index]

        # Define fonts
        font_large = pygame.font.Font(None, 26)
        font_small = pygame.font.Font(None, 18)

        # Modern champion icon with frame
        icon_frame_x = padding
        icon_frame_y = bar_y + (bar_height - icon_size) // 2 - 3

        if current_unit.image:
            # Outer glow
            glow_size = icon_size + 8
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            team_color = Colors.BLUE_TEAM if current_unit.color == "blue" else Colors.RED_TEAM if current_unit.color == "red" else Colors.PURPLE
            pygame.draw.rect(glow_surface, (*team_color, 80), (0, 0, glow_size, glow_size), border_radius=8)
            self.screen.blit(glow_surface, (icon_frame_x - 4, icon_frame_y - 4))

            # Icon background
            pygame.draw.rect(self.screen, (45, 45, 55), (icon_frame_x, icon_frame_y, icon_size, icon_size), border_radius=5)

            # Champion icon
            icon = pygame.transform.scale(current_unit.image, (icon_size, icon_size))
            self.screen.blit(icon, (icon_frame_x, icon_frame_y))

            # Icon border
            pygame.draw.rect(self.screen, team_color, (icon_frame_x, icon_frame_y, icon_size, icon_size), 3, border_radius=5)

        # Unit Stats Display (Name, HP, Mana)
        stats_x = padding + icon_size + padding
        stats_y = bar_y + padding

        # Unit name with shadow
        name_shadow = font_large.render(current_unit.name, True, (0, 0, 0))
        name_surface = font_large.render(current_unit.name, True, Colors.GOLD)
        self.screen.blit(name_shadow, (stats_x + 2, stats_y + 2))
        self.screen.blit(name_surface, (stats_x, stats_y))

        # HP Bar (with smooth animation)
        hp_bar_width = 200
        hp_bar_height = 18
        hp_x = stats_x
        hp_y = stats_y + name_surface.get_height() + padding + 2

        # HP bar background with shadow
        shadow_offset = 2
        pygame.draw.rect(self.screen, (0, 0, 0, 100), (hp_x + shadow_offset, hp_y + shadow_offset, hp_bar_width, hp_bar_height), border_radius=4)

        # Background (dark red for missing health)
        pygame.draw.rect(self.screen, (120, 20, 20), (hp_x, hp_y, hp_bar_width, hp_bar_height), border_radius=4)

        # Animated fill (gradient green for current health)
        hp_fill_width = int(hp_bar_width * (current_unit.displayed_health / current_unit.max_health))
        if hp_fill_width > 0:
            hp_gradient = pygame.Surface((hp_fill_width, hp_bar_height), pygame.SRCALPHA)
            for i in range(hp_bar_height):
                color_intensity = int(200 + (i / hp_bar_height) * 55)
                pygame.draw.rect(hp_gradient, (0, color_intensity, 0, 255), (0, i, hp_fill_width, 1))
            self.screen.blit(hp_gradient, (hp_x, hp_y))

        # Border with team color
        border_color = Colors.BLUE_TEAM if current_unit.color == "blue" else Colors.RED_TEAM if current_unit.color == "red" else Colors.PURPLE
        pygame.draw.rect(self.screen, border_color, (hp_x, hp_y, hp_bar_width, hp_bar_height), 2, border_radius=4)

        # HP text with outline
        hp_text = f"{int(current_unit.health)}/{current_unit.max_health}"
        hp_text_outline = font_small.render(hp_text, True, (0, 0, 0))
        hp_text_surface = font_small.render(hp_text, True, (255, 255, 255))
        text_x = hp_x + (hp_bar_width - hp_text_surface.get_width()) // 2
        text_y = hp_y + (hp_bar_height - hp_text_surface.get_height()) // 2
        for dx, dy in [(-1,-1), (1,-1), (-1,1), (1,1)]:
            self.screen.blit(hp_text_outline, (text_x + dx, text_y + dy))
        self.screen.blit(hp_text_surface, (text_x, text_y))

        # Mana Bar (with smooth animation)
        mana_bar_width = 200
        mana_bar_height = 12
        mana_x = stats_x
        mana_y = hp_y + hp_bar_height + 4

        # Mana bar background with shadow
        pygame.draw.rect(self.screen, (0, 0, 0, 100), (mana_x + shadow_offset, mana_y + shadow_offset, mana_bar_width, mana_bar_height), border_radius=3)

        # Background (dark blue for missing mana)
        pygame.draw.rect(self.screen, (20, 20, 80), (mana_x, mana_y, mana_bar_width, mana_bar_height), border_radius=3)

        # Animated fill (gradient cyan for current mana)
        mana_fill_width = int(mana_bar_width * (current_unit.displayed_mana / current_unit.max_mana))
        if mana_fill_width > 0:
            mana_gradient = pygame.Surface((mana_fill_width, mana_bar_height), pygame.SRCALPHA)
            for i in range(mana_bar_height):
                color_intensity = int(150 + (i / mana_bar_height) * 105)
                pygame.draw.rect(mana_gradient, (0, color_intensity, 255, 255), (0, i, mana_fill_width, 1))
            self.screen.blit(mana_gradient, (mana_x, mana_y))

        # Border
        pygame.draw.rect(self.screen, border_color, (mana_x, mana_y, mana_bar_width, mana_bar_height), 2, border_radius=3)

        # Mana text
        mana_text = f"{int(current_unit.mana)}/{current_unit.max_mana}"
        mana_text_outline = font_small.render(mana_text, True, (0, 0, 0))
        mana_text_surface = font_small.render(mana_text, True, (200, 240, 255))
        mana_text_x = mana_x + (mana_bar_width - mana_text_surface.get_width()) // 2
        mana_text_y = mana_y + (mana_bar_height - mana_text_surface.get_height()) // 2
        for dx, dy in [(-1,-1), (1,-1), (-1,1), (1,1)]:
            self.screen.blit(mana_text_outline, (mana_text_x + dx, mana_text_y + dy))
        self.screen.blit(mana_text_surface, (mana_text_x, mana_text_y))

        # Draw abilities with modern card design
        if hasattr(current_unit, "abilities"):
            num_abilities = len(current_unit.abilities)
            if num_abilities > 0:
                ability_x_start = stats_x + hp_bar_width + 3 * padding
                ability_width = (SCREEN_WIDTH - ability_x_start - padding - 10) // num_abilities - 5

                for i, ability in enumerate(current_unit.abilities):
                    ability_x = ability_x_start + i * (ability_width + 5)
                    card_y = bar_y + padding
                    card_height = bar_height - 2 * padding

                    # Check if ability is ready
                    is_ready = ability.remaining_cooldown == 0 and current_unit.mana >= ability.mana_cost
                    is_selected = current_unit.selected_ability == ability

                    # Card shadow
                    pygame.draw.rect(self.screen, (0, 0, 0, 120), (ability_x + 3, card_y + 3, ability_width, card_height), border_radius=8)

                    # Card background
                    if is_selected:
                        card_color = (40, 100, 180)
                    elif is_ready:
                        card_color = (50, 60, 70)
                    else:
                        card_color = (35, 35, 45)

                    pygame.draw.rect(self.screen, card_color, (ability_x, card_y, ability_width, card_height), border_radius=8)

                    # Glow effect for selected ability
                    if is_selected:
                        glow_rect = pygame.Rect(ability_x - 2, card_y - 2, ability_width + 4, card_height + 4)
                        pygame.draw.rect(self.screen, (100, 150, 255), glow_rect, 3, border_radius=10)

                    # Key number indicator
                    key_size = 18
                    key_bg = pygame.Rect(ability_x + 5, card_y + 5, key_size, key_size)
                    pygame.draw.rect(self.screen, (0, 0, 0, 180), key_bg, border_radius=3)
                    key_text = font_small.render(str(i + 1), True, Colors.GOLD)
                    self.screen.blit(key_text, (ability_x + 5 + (key_size - key_text.get_width()) // 2, card_y + 5))

                    # Ability name
                    name_y = card_y + 8
                    ability_name = ability.name
                    if len(ability_name) > 12:
                        ability_name = ability_name[:10] + ".."
                    name_shadow = font_small.render(ability_name, True, (0, 0, 0))
                    name_surface = font_small.render(ability_name, True, (255, 255, 255) if is_ready else (150, 150, 150))
                    self.screen.blit(name_shadow, (ability_x + 26, name_y + 1))
                    self.screen.blit(name_surface, (ability_x + 25, name_y))

                    # Mana cost
                    mana_y = name_y + 18
                    mana_icon_color = Colors.CYAN if is_ready else (80, 100, 120)
                    pygame.draw.circle(self.screen, mana_icon_color, (ability_x + 10, mana_y + 7), 6)
                    mana_text = font_small.render(str(ability.mana_cost), True, (255, 255, 255) if is_ready else (120, 120, 120))
                    self.screen.blit(mana_text, (ability_x + 20, mana_y + 2))

                    # Cooldown indicator
                    if ability.remaining_cooldown > 0:
                        cd_y = mana_y + 18
                        cd_surface = font_small.render(f"{ability.remaining_cooldown}s", True, Colors.RED)
                        self.screen.blit(cd_surface, (ability_x + 10, cd_y))

                    # Border
                    border_color = (100, 150, 255) if is_selected else (255, 215, 0) if is_ready else (60, 60, 70)
                    pygame.draw.rect(self.screen, border_color, (ability_x, card_y, ability_width, card_height), 2, border_radius=8)

                    # Cooldown bar
                    cooldown_bar_width = ability_width - 2 * padding
                    cooldown_bar_x = ability_x + padding
                    cooldown_bar_y = bar_y + bar_height - 15
                    pygame.draw.rect(
                        self.screen, (50, 50, 50), (cooldown_bar_x, cooldown_bar_y, cooldown_bar_width, 5)
                    )
                    if ability.cooldown > 0:
                        cooldown_fill_width = int(
                            cooldown_bar_width
                            * (1 - ability.remaining_cooldown / ability.cooldown)
                        )
                        pygame.draw.rect(
                            self.screen,
                            (0, 255, 0),
                            (cooldown_bar_x, cooldown_bar_y, cooldown_fill_width, 5),
                        )
            else:
                # No abilities available
                no_abilities_text = "No abilities available"
                no_abilities_surface = font_small.render(
                    no_abilities_text, True, (255, 255, 255)
                )
                no_abilities_x = stats_x + hp_bar_width + padding
                self.screen.blit(
                    no_abilities_surface, (no_abilities_x, bar_y + padding)
                )




    def draw_units(self):
        """Draw all units on the grid with visibility logic."""
        current_team_color = self.units[self.current_unit_index].color
        for index, unit in enumerate(self.units):
            if unit.alive:
                is_current_turn = (index == self.current_unit_index)  # Check if it's the current unit's turn
                # Draw units only if they belong to the current team or are in visible tiles
                if unit.color == current_team_color or (unit.x, unit.y) in self.visible_tiles and self.grid.tiles[unit.x][unit.y].overlay != "bush":
                    unit.draw(self.screen, is_current_turn=is_current_turn)
                    



    def basic_attack(self, unit):
        """Resolve the attack at the current target location."""
        target_hit = False

        # Find a valid target at the attack cursor location
        for other_unit in self.units:
            if (
                other_unit.alive
                and other_unit.x == unit.target_x
                and other_unit.y == unit.target_y
                and other_unit.color != unit.color
            ):
                damage=unit.attack(other_unit,unit.damage)  # Use the Unit's attack method
                if damage > 0:
                    self.log_event(f"{unit.name} attacked {other_unit.name} for {damage} damage!")
                    # Trigger screen shake, flash, and particles on damage
                    self.trigger_screen_shake()
                    self.trigger_screen_flash(Colors.RED)
                    self.spawn_particles(other_unit.x, other_unit.y, Colors.RED, count=15)
                    # Vérifier si l'unité est morte
                    if not other_unit.alive:
                        self.log_event(f"{other_unit.name} has been defeated!")
                else:
                    self.log_event(f"{unit.name} attacked {other_unit.name} but missed!")
                target_hit = True
                break
        if not target_hit:
            self.log_event(f"{unit.name} attacked but missed!")

        unit.state = "done"  # Mark the unit as done after the attack
        



    def advance_to_next_unit(self):
        """Advance to the next unit, skipping dead ones."""
        # Start from the current unit
        start_index = self.current_unit_index

        #we keep incrementing the index untill we fullfil the conditions
        while True:
            # Move to the next unit
            self.current_unit_index = (self.current_unit_index + 1) % len(self.units)

            # Check if the unit is alive and that is part of either team red or team blue
            if (self.units[self.current_unit_index].alive 
                and self.units[self.current_unit_index].unit_type=="player"):
                break

            # If we've cycled through all units and come back to the start, stop (prevents infinite loops)
            if self.current_unit_index == start_index:
                self.log_event("No alive units remaining!")
                return


#add a mana and health regen for each round (2% mana ,1%hp)   

    def handle_turn(self):
        """Handle movement and attacks for the current unit."""
        current_time = pygame.time.get_ticks()
        current_unit = self.units[self.current_unit_index]
        keys = pygame.key.get_pressed()

        action_key = pygame.K_SPACE

        # debounce mechanism to avoid repeated triggers.
        if not hasattr(self, "key_last_state"):
            self.key_last_state = {}

        key_just_pressed = keys[action_key] and not self.key_last_state.get(action_key, False)
        self.key_last_state[action_key] = keys[action_key]

        # Movement Phase
        if current_unit.state == "move":
            if current_time - self.last_move_time > Gameplay.MOVE_DELAY_MS:
                if keys[pygame.K_UP]:
                    current_unit.move(0, -1, self.grid)
                    self.last_move_time = current_time
                elif keys[pygame.K_DOWN]:
                    current_unit.move(0, 1, self.grid)
                    self.last_move_time = current_time
                elif keys[pygame.K_LEFT]:
                    current_unit.move(-1, 0, self.grid)
                    self.last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    current_unit.move(1, 0, self.grid)
                    self.last_move_time = current_time
                elif key_just_pressed:
                    if not any(
                        unit.x == current_unit.x and unit.y == current_unit.y and unit != current_unit
                        and unit.alive for unit in self.units 
                    ):  
                        self.log_event(f"{current_unit.name} finalized move at ({current_unit.x}, {current_unit.y}).")

                        for p in self.pickup.all_pickups:
                            if p.x == current_unit.x and p.y == current_unit.y:
                                self.pickup.picked_used(current_unit,p)


                        current_unit.state = "attack"
                        
                        current_unit.target_x, current_unit.target_y = current_unit.x, current_unit.y  # Initialize cursor

                        next_team_color = self.units[self.current_unit_index].color
                        Highlight.update_fog_visibility(self,next_team_color)



                            #check if there is enemy in bush
                    elif self.grid.tiles[current_unit.x][current_unit.y].overlay == "bush" and any(
                            unit.x == current_unit.x and unit.y == current_unit.y 
                            and unit.alive and unit.color != current_unit.color for unit in self.units
                        ) :   #in the presence of an enemy on this position but it's a bush u just get assassinated
                        enemy_unit = next(
                            (unit for unit in self.units if unit.x == current_unit.x and unit.y == current_unit.y 
                            and unit.alive and unit.color != current_unit.color), 
                            None
                        )
                        if enemy_unit:
                            self.log_event(f"{current_unit.name} got assassinated")
                            
                            enemy_unit.attack(current_unit,9999)
                            current_unit.state="done"
                            self.manage_keys(dead_player=current_unit, killer=enemy_unit)



                    else :      #if it's another unit u just can't finalise movement
                        self.log_event("can't finalise movement , another unit is filling this position")
                    
        # Attack Phase
        elif current_unit.state == "attack":
            if current_time - self.last_move_time > Gameplay.MOVE_DELAY_MS:
                new_target_x, new_target_y = current_unit.target_x, current_unit.target_y

                # Determine current range restriction
                if hasattr(current_unit, "selected_ability") and current_unit.selected_ability is not None:
                    current_range = current_unit.selected_ability.attack_radius
                else:
                    current_range = current_unit.attack_range

                # Move the attack cursor
                if keys[pygame.K_UP]:
                    new_target_y = max(0, current_unit.target_y - 1)
                elif keys[pygame.K_DOWN]:
                    new_target_y = min(GRID_SIZE - 1, current_unit.target_y + 1)
                elif keys[pygame.K_LEFT]:
                    new_target_x = max(0, current_unit.target_x - 1)
                elif keys[pygame.K_RIGHT]:
                    new_target_x = min(GRID_SIZE - 1, current_unit.target_x + 1)

                # Enforce range restriction
                if abs(current_unit.x - new_target_x) + abs(current_unit.y - new_target_y) <= current_range:
                    current_unit.target_x, current_unit.target_y = new_target_x, new_target_y
                    self.last_move_time = current_time

            # Ability Selection
            if hasattr(current_unit, "abilities"):
                if keys[pygame.K_1] and len(current_unit.abilities) > 0:
                    current_unit.selected_ability = current_unit.abilities[0]
                    current_unit.target_x, current_unit.target_y = current_unit.x, current_unit.y
                   
                elif keys[pygame.K_2] and len(current_unit.abilities) > 1:
                    current_unit.selected_ability = current_unit.abilities[1]
                    current_unit.target_x, current_unit.target_y = current_unit.x, current_unit.y

                elif keys[pygame.K_3] and len(current_unit.abilities) > 2:
                    current_unit.selected_ability = current_unit.abilities[2]
                    current_unit.target_x, current_unit.target_y = current_unit.x, current_unit.y
                   
                elif keys[pygame.K_c]:  # Cancel ability selection
                    current_unit.selected_ability = None
                    current_unit.target_x, current_unit.target_y = current_unit.x, current_unit.y


            # Execute Selected Ability or Basic Attack
            target = next(
                (unit for unit in self.units if unit.alive and unit.x == current_unit.target_x and unit.y == current_unit.target_y),
                None,
            )
            if current_unit.selected_ability is not None :
                if key_just_pressed:  # Confirm ability usage

                    if current_unit.selected_ability.is_aoe>0:   #logic when using aoe abilities

                        aoe_targets = current_unit.selected_ability.get_targets_in_aoe(current_unit, self.units)
                        if aoe_targets is not None:  # Ensure targets exist
                            if current_unit.selected_ability.use(current_unit, aoe_targets):
                                self.sound.play(current_unit.selected_ability.name)
                                current_unit.state = "done"
                                current_unit.selected_ability = None  # Reset ability selection
                        
                        else:
                            print("No valid target selected.")

                        # Handle monster defeats for AoE abilities
                        for targets in aoe_targets:
                            self.handle_monster_defeat(targets, current_unit)
                            if targets is not None and not targets.alive:
                                self.manage_keys(dead_player=targets, killer=current_unit)

                    else : #logic when using none aoe abilities
                        if target is not None:  # Ensure targets exist
                            if current_unit.selected_ability.use(current_unit, target):
                                self.sound.play(current_unit.selected_ability.name)
                                current_unit.state = "done"
                                current_unit.selected_ability = None  # Reset ability selection
                        
                        else:
                            print("No valid target selected.")
                        # Handle monster defeat for non-AoE abilities
                        self.handle_monster_defeat(target, current_unit)
                        if target is not None and not target.alive:
                            self.manage_keys(dead_player=target, killer=current_unit)



            elif  key_just_pressed:
                self.basic_attack(current_unit)  # Basic attack
                current_unit.state = "done"

                # Jouer le son d'attaque de base si il y'a un target
                basic_attack_sound = f"{current_unit.name} Basic Attack"
                if target is not None and target!=current_unit:
                    if basic_attack_sound in self.sound.sounds:
                        self.sound.play(basic_attack_sound)

                # Handle monster defeat for basic attack
                self.handle_monster_defeat(target, current_unit)
                if target is not None and not target.alive:
                    self.manage_keys(dead_player=target, killer=current_unit)

            

        # End Turn
        if  keys[pygame.K_r] and current_unit.state == "done" :
            self.current_turn+=1

            #each turn we reduce the cooldowns and reduce the duration remaaning on the buffs
            for unit in self.units:
                for ability in unit.abilities:
                        ability.reduce_cooldown()
            for unit in self.units:
                unit.update_buffs_and_debuffs()


            current_unit.state = "move"  # Reset state for the next turn
            current_unit.initial_x, current_unit.initial_y = current_unit.x, current_unit.y  # Reset initial position
            self.advance_to_next_unit()

            next_team_color = self.units[self.current_unit_index].color
            Highlight.update_fog_visibility(self,next_team_color)
            self.pickup.update(self.current_turn,self.grid)
            self.manage_keys(current_turn=self.current_turn)

            # Health and mana regeneration each turn
            for unit in self.units:
                if unit.unit_type == "player":
                    unit.health += min(unit.max_health - unit.health, int(Gameplay.HEALTH_REGEN_PERCENT * unit.max_health))
                    unit.mana += min(unit.max_mana - unit.mana, int(Gameplay.MANA_REGEN_PERCENT * unit.max_mana))

            # Respawn logic
            respawn = min(self.current_turn // Gameplay.RESPAWN_BASE_TURNS, Gameplay.RESPAWN_MAX_CAP)

            # Update death timers and respawn dead units
            for unit in self.units:
                if not unit.alive and unit.unit_type=="player":
                    unit.death_timer += 1  # Increment death timer for dead units
                    print(f"{unit.death_timer}seconds of death for {unit.name}")
                    # Respawn logic
                    if unit.death_timer >= respawn :
                        self.log_event(f"{unit.name} has respawned at base!")
                        unit.alive = True
                        unit.health = unit.max_health  # Restore health
                        unit.state = "move"
                        unit.initial_x, unit.initial_y = self.get_respawn_location(unit)  # Define respawn location logic
                        unit.x,unit.y = unit.initial_x, unit.initial_y
                        unit.death_timer = 0  # Reset death timer

            


    def get_respawn_location(self, unit):
        """Get respawn location for a unit based on their index."""
        unit_index = self.units.index(unit)
        return RESPAWN_LOCATIONS.get(unit_index, (0, 0))



    
    def remove_barrier_from_grid(self, team):
        """Remove barrier overlay from grid tiles when barrier falls."""
        from config import TERRAIN_OVERLAYS

        barrier_positions = TERRAIN_OVERLAYS.get("barrier", [])

        for x, y in barrier_positions:
            if 0 <= x < len(self.grid.tiles) and 0 <= y < len(self.grid.tiles[0]):
                tile = self.grid.tiles[x][y]
                # Determine which barrier this is based on position
                # Red barriers are on the upper right (around x=17-20, y=0-3)
                # Blue barriers are on the lower left (around x=0-3, y=17-20)
                if team == "red" and x >= 17:  # Red barrier
                    tile.overlay = None
                elif team == "blue" and y >= 17:  # Blue barrier
                    tile.overlay = None

    def manage_keys(self, dead_player=None, killer=None, current_turn=None):
        """
        Handles all key-related logic:
        - Initializes keys at the start of the game.
        - Transfers keys when a player dies.
        - Spawns additional keys based on turn events.
        - Tracks team progress on key collection.

        :param dead_player: The unit that died (optional).
        :param killer: The unit that killed the dead player (optional).
        :param current_turn: The current turn number (optional).
        """
        # Initialize keys at the start of the game
        if not hasattr(self, "keys_initialized") or not self.keys_initialized:
            self.units[0].blue_keys = 1  # Blue Player 1 starts with one Blue key
            self.units[1].blue_keys = 1  # Blue Player 2 starts with one Blue key
            self.units[2].red_keys = 1  # Red Player 1 starts with one Red key
            self.units[3].red_keys = 1  # Red Player 2 starts with one Red key
            self.keys_initialized = True
            print(f"Initial keys have been assigned to players.")

        # Handle key transfer on player death
        if dead_player and killer:
            if killer.unit_type == "player":
                # Transfer keys to the killer
                keys_collected = dead_player.red_keys + dead_player.blue_keys
                killer.red_keys += dead_player.red_keys
                killer.blue_keys += dead_player.blue_keys
                print(f"{killer.name} collected {dead_player.red_keys} Red key(s) and {dead_player.blue_keys} Blue key(s) from {dead_player.name}.")
                # Flash gold and spawn particles on key collection
                if keys_collected > 0:
                    self.trigger_screen_flash(Colors.GOLD)
                    self.spawn_particles(dead_player.x, dead_player.y, Colors.GOLD, count=20)
                dead_player.red_keys = 0
                dead_player.blue_keys = 0
            else:
                # Keys are lost if the killer is not a player
                print(f"{dead_player.name}'s {dead_player.red_keys} Red key(s) and {dead_player.blue_keys} Blue key(s) are not lost.")

            

        # Check if the team got enough keys to break barrier
        if self.units[0].red_keys + self.units[1].red_keys >= Gameplay.KEYS_REQUIRED_TO_BREAK_BARRIER:
            if self.red_barrier != "Down":
                print("blue team broke the red barrier")
                self.units[-1].barrier_status = "Down"
                self.red_barrier = "Down"
                # Remove red barrier tiles from grid
                self.remove_barrier_from_grid("red")
                # Flash effect
                self.trigger_screen_flash((255, 100, 100))

        if self.units[2].blue_keys + self.units[3].blue_keys >= Gameplay.KEYS_REQUIRED_TO_BREAK_BARRIER:
            if self.blue_barrier != "Down":
                print("red team broke the blue barrier")
                self.units[-2].barrier_status = "Down"
                self.blue_barrier = "Down"
                # Remove blue barrier tiles from grid
                self.remove_barrier_from_grid("blue")
                # Flash effect
                self.trigger_screen_flash((100, 100, 255))

        # Spawn additional keys based on turn events
        if current_turn:
            if current_turn % Gameplay.MONSTER_RESPAWN_TURN_INTERVAL == 0:
                # Assign keys to a monster
                for unit in self.units :
                    if unit.unit_type == "monster" :
                        if unit.alive==False:
                            unit.health=unit.max_health
                            unit.alive=True
                            if unit.name=="BlueBuff":
                                unit.blue_keys = 1
                                print("BlueBuff now holds 1 Blue key")
                            if unit.name=="RedBuff":
                                unit.red_keys = 1
                                print("RedBuff now holds 1 Red key.")
                    


                    
    def draw_key_counts(self):
        """Draw the number of red and blue keys each player has."""
        # Constants for layout
        key_icon_size = UI.KEY_ICON_SIZE
        unit_icon_size = int(CELL_SIZE * UI.UNIT_ICON_SIZE_RATIO)
        x_offset = SCREEN_WIDTH - 250
        y_offset = SCREEN_HEIGHT / 2
        spacing = 50

        # Create font for the key counts
        larger_font = pygame.font.Font(None, 32)

        # Draw individual player key counts
        for i, unit in enumerate(self.units):
            if unit.unit_type == "player":
                # Calculate vertical position
                player_y = y_offset + i * spacing

                # Draw unit image
                self.screen.blit(
                    pygame.transform.scale(unit.image, (unit_icon_size, unit_icon_size)),
                    (x_offset, player_y)
                )

                # Draw key images and counts
                self.screen.blit(
                    pygame.transform.scale(self.red_key_img, (key_icon_size, key_icon_size)),
                    (x_offset + unit_icon_size + 110, player_y)
                )
                self.screen.blit(
                    pygame.transform.scale(self.blue_key_img, (key_icon_size, key_icon_size)),
                    (x_offset + unit_icon_size + 20, player_y)
                )  # More space between key images

                # Draw key count texts
                red_key_count_text = larger_font.render(str(unit.red_keys), True, Colors.GOLD)
                blue_key_count_text = larger_font.render(str(unit.blue_keys), True, Colors.GOLD)
                self.screen.blit(
                    red_key_count_text,
                    (x_offset + unit_icon_size + 110 + key_icon_size + 10, player_y)
                )
                self.screen.blit(
                    blue_key_count_text,
                    (x_offset + unit_icon_size + 20 + key_icon_size + 10, player_y)
                )
        # Draw barrier statuses below key counts
        red_barrier_text = larger_font.render(f"Red Barrier: {self.red_barrier}", True, Colors.GOLD)
        blue_barrier_text = larger_font.render(f"Blue Barrier: {self.blue_barrier}", True, Colors.GOLD)
        self.screen.blit(
            red_barrier_text,
            (x_offset-10 , player_y + key_icon_size + 10)
        )
        self.screen.blit(
            blue_barrier_text,
            (x_offset-10 , player_y +spacing + key_icon_size + 10)
        )



        
    def check_game_over(self):
        """
        Checks if either Nexus is dead and triggers the Game Over screen.
        Returns True if the game is over, False otherwise.
        """
        for unit in self.units:
            if unit.unit_type=="base" and unit.health <= 0:
                # Determine the winner based on the color of the dead Nexus
                winner_team = "red" if unit.color == "blue" else "blue"

                # Call the game over handler to display the screen and stop further game logic
                self.game_over_screen(winner_team)
                return True  # Indicate that the game is over

        return False  # Continue the game if no Nexus is dead




    def game_over_screen(self, winner_team):
        """Display a 'Game Over' screen indicating which team won."""
        rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.blit(pygame.transform.scale(self.game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), rect)

        # Set up fonts
        game_over_font = pygame.font.Font(Assets.FONT_RUSSO, 80)
        winner_font = pygame.font.Font(Assets.FONT_RUSSO, 50)

        # Render text surfaces
        game_over_text = game_over_font.render("GAME OVER", True, Colors.WHITE)
        winner_text = winner_font.render(f"Team {winner_team.upper()} Won!", True, Colors.GOLD)

        # Center the texts on the screen
        screen_width, screen_height = self.screen.get_size()
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        winner_rect = winner_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

        # Draw text on the screen
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(winner_text, winner_rect)

        # Update the display
        pygame.display.flip()

        # Pause to show the screen
        pygame.time.delay(Gameplay.GAME_OVER_DELAY_MS)

   
        

    def spawn_particles(self, x, y, color, count=10):
        """Spawn particles at the given position."""
        import random
        for _ in range(count):
            particle = {
                'x': x * CELL_SIZE + CELL_SIZE // 2,
                'y': y * CELL_SIZE + CELL_SIZE // 2,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'life': random.randint(20, 40),
                'color': color,
                'size': random.randint(2, 5)
            }
            self.particles.append(particle)

    def update_particles(self):
        """Update and remove dead particles."""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self):
        """Draw all active particles."""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 40))
            color_with_alpha = (*particle['color'][:3], alpha)
            particle_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, (particle['size'] // 2, particle['size'] // 2), particle['size'] // 2)
            self.screen.blit(particle_surface, (int(particle['x']), int(particle['y'])))

    def fade_transition(self, fade_in=True, duration_ms=500):
        """Create a fade transition effect."""
        start_time = pygame.time.get_ticks()
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill(Colors.BLACK)

        while True:
            elapsed = pygame.time.get_ticks() - start_time
            if elapsed >= duration_ms:
                break

            progress = elapsed / duration_ms
            if fade_in:
                alpha = int(255 * (1 - progress))
            else:
                alpha = int(255 * progress)

            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)

    def trigger_screen_shake(self):
        """Trigger a screen shake effect."""
        self.screen_shake_start = pygame.time.get_ticks()
        self.screen_shake_active = True

    def trigger_screen_flash(self, color):
        """Trigger a screen flash effect with the given color."""
        self.screen_flash_start = pygame.time.get_ticks()
        self.screen_flash_color = color

    def get_screen_offset(self):
        """Calculate screen offset for shake effect."""
        if not self.screen_shake_active:
            return (0, 0)

        elapsed = pygame.time.get_ticks() - self.screen_shake_start
        if elapsed > Gameplay.SCREEN_SHAKE_DURATION_MS:
            self.screen_shake_active = False
            return (0, 0)

        # Random shake with decreasing intensity
        progress = elapsed / Gameplay.SCREEN_SHAKE_DURATION_MS
        intensity = Gameplay.SCREEN_SHAKE_INTENSITY * (1 - progress)
        import random
        offset_x = random.randint(-int(intensity), int(intensity))
        offset_y = random.randint(-int(intensity), int(intensity))
        return (offset_x, offset_y)

    def apply_screen_flash(self):
        """Draw screen flash overlay if active."""
        if self.screen_flash_color is None:
            return

        elapsed = pygame.time.get_ticks() - self.screen_flash_start
        if elapsed > Gameplay.FLASH_DURATION_MS:
            self.screen_flash_color = None
            return

        # Fade out the flash
        progress = elapsed / Gameplay.FLASH_DURATION_MS
        alpha = int(150 * (1 - progress))
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        color_with_alpha = (*self.screen_flash_color[:3], alpha)
        flash_surface.fill(color_with_alpha)
        self.screen.blit(flash_surface, (0, 0))

    def run(self):
        """Main game loop with return to main menu on game over."""
        while True:  # Allow restarting the game after game over
            self.main_menu()  # Display main menu
            self.units = self.show_menu()
            self.manage_keys()  # Initializes keys

            starting_team_color = self.units[self.current_unit_index].color
            Highlight.update_fog_visibility(self, starting_team_color)

            running = True
            while running:
                self.screen.fill((0, 0, 0))  # Clear the screen
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()  # Exit the game completely

                # Check for Game Over
                if self.check_game_over():
                    running = False  # Exit the game loop but go back to the main menu
                    break

                # Get screen shake offset
                shake_offset = self.get_screen_offset()

                # Update particles
                self.update_particles()

                # Apply shake offset to screen
                if shake_offset != (0, 0):
                    # Create a temporary surface for shaking
                    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    game_surface.fill((0, 0, 0))

                    # Draw everything on temp surface
                    self.grid.draw(game_surface)
                    current_unit = self.units[self.current_unit_index]
                    Highlight.highlight_range(self, current_unit)
                    Highlight.draw_fog(self, game_surface)
                    self.pickup.draw_pickups(game_surface, self.visible_tiles)
                    self.draw_units()
                    self.handle_turn()
                    self.draw_info_panel()
                    self.draw_abilities_bar()
                    self.draw_key_counts()

                    # Blit with offset
                    self.screen.blit(game_surface, shake_offset)
                else:
                    # Normal drawing without shake
                    self.grid.draw(self.screen)
                    current_unit = self.units[self.current_unit_index]
                    Highlight.highlight_range(self, current_unit)
                    Highlight.draw_fog(self, self.screen)
                    self.pickup.draw_pickups(self.screen, self.visible_tiles)
                    self.draw_units()
                    self.handle_turn()
                    self.draw_info_panel()
                    self.draw_abilities_bar()
                    self.draw_key_counts()

                # Draw particles (always on top)
                self.draw_particles()

                # Apply screen flash effect
                self.apply_screen_flash()

                pygame.display.flip()
                self.clock.tick(FPS)
