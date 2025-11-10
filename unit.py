import pygame
import random
from abilities import DamageHealAbility, BuffAbility, DebuffAbility
from sounds import Sounds
from constants import *
from config import CHAMPIONS, MONSTERS, BASES

class Unit:
    """A single unit in the game."""
    def __init__(self, x, y, name, health, damage,physical_defense,magical_defense,crit_chance,image_path, color, move_range, attack_range, unit_type, mana=100, abilities=None):
        self.x = x
        self.y = y
        self.initial_x = x  # Initial position for movement range
        self.initial_y = y
        self.name = name
        self.image = pygame.image.load(image_path)
        self.color = color
        self.health = health
        self.max_health = health
        self.physical_defense=physical_defense
        self.magical_defense=magical_defense
        self.damage=damage
        self.crit_chance=crit_chance
        self.mana = mana
        self.max_mana = mana
        self.move_range = move_range
        self.attack_range = attack_range
        self.unit_type=unit_type   #player or neutral or base_blue or base_red
        self.alive = True
        self.state = "move"  # "move" or "attack"
        self.selected_ability = None  # Currently selected ability

        # Attack targeting cursor
        self.target_x = x
        self.target_y = y
        self.abilities = abilities if abilities else []  # Default to an empty list if no abilities are provided


        # Buff and debuff trackers
        self.buffed_damage_increase = 0
        self.buffed_defense_increase = 0
        self.debuffed_attack_reduction = 0
        self.debuffed_defense_reduction = 0
        self.buff_duration = 0
        self.debuff_duration = 0
        self.is_buffed = False
        self.is_debuffed = False

        # Add key variables
        self.red_keys = 0  # Number of red keys this unit holds
        self.blue_keys = 0  # Number of blue keys this unit holds

        self.death_timer = 0  # Tracks turns since death

        # Initialize for damage display
        self.last_damage_time = None
        self.damage_taken = 0
        self.damage_taken_type = "physical"

        # Movement sounds
        self.grass_sound = pygame.mixer.Sound(Assets.MOVING)
        self.grass_sound.set_volume(Volume.MOVEMENT)
        self.water_sound = pygame.mixer.Sound(Assets.WATER_SOUND)
        self.water_sound.set_volume(Volume.MOVEMENT)


    @staticmethod
    def _create_abilities(abilities_config):
        """Create ability objects from configuration."""
        abilities = []
        for ability_cfg in abilities_config:
            ability_type = ability_cfg["type"]
            kwargs = {k: v for k, v in ability_cfg.items() if k != "type"}

            if ability_type == "DamageHealAbility":
                abilities.append(DamageHealAbility(**kwargs))
            elif ability_type == "BuffAbility":
                abilities.append(BuffAbility(**kwargs))
            elif ability_type == "DebuffAbility":
                abilities.append(DebuffAbility(**kwargs))

        return abilities

    def create_units(self):
        """Create units and place them on the grid from configuration."""
        units = []

        # Create player champions (unassigned, will be selected in menu)
        for champ_name, champ_data in CHAMPIONS.items():
            abilities = Unit._create_abilities(champ_data["abilities"])
            unit = Unit(
                0, 0,  # Placeholder position
                champ_name,
                champ_data["health"],
                champ_data["damage"],
                champ_data["physical_defense"],
                champ_data["magical_defense"],
                champ_data["crit_chance"],
                champ_data["image"],
                None,  # Color assigned later
                champ_data["move_range"],
                champ_data["attack_range"],
                "player",
                mana=champ_data["mana"],
                abilities=abilities
            )
            units.append(unit)

        # Create monsters
        for monster_data in MONSTERS:
            monster = MonsterUnit(
                monster_data["x"],
                monster_data["y"],
                monster_data["name"],
                monster_data["health"],
                monster_data["damage"],
                monster_data["physical_defense"],
                monster_data["magical_defense"],
                monster_data["crit_chance"],
                monster_data["image"],
                "neutral",
                monster_data["move_range"],
                monster_data["attack_range"],
                "monster"
            )
            units.append(monster)

        # Create bases
        for base_data in BASES:
            base = BaseUnit(
                base_data["x"],
                base_data["y"],
                base_data["name"],
                base_data["health"],
                base_data["damage"],
                base_data["physical_defense"],
                base_data["magical_defense"],
                base_data["crit_chance"],
                base_data["image"],
                base_data["color"],
                0, 0,  # Bases don't move or attack
                "base",
                "Up"  # Barrier status
            )
            units.append(base)

        return units




    def in_range(self, target):
        """Check if the target is within attack range."""
        return abs(self.x - target.x) + abs(self.y - target.y) <= self.attack_range




    def move(self, dx, dy, grid):
    
        """Move the unit if within movement range, traversable, and highlighted."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the current position is within grid bounds
        if 0 <= new_x < len(grid.tiles) and 0 <= new_y < len(grid.tiles[0]):

            # Get the target tile at the new position
            target_tile = grid.tiles[new_x][new_y]

            # Check if the target tile is highlighted
            if not target_tile.highlighted:
                print(f"Cannot move to ({new_x}, {new_y}) because it's not highlighted.")
                return  # Can't move if the tile is not highlighted
            # Jouer le son correspondant au type de terrain

            else :
                self.x, self.y = new_x, new_y
                if target_tile.terrain== "grass":
                    self.grass_sound.play()
                    
                elif target_tile.terrain == "water":
                    self.water_sound.play()



    #neutral monsters reacting to attacks
    def react_to_attack(self, attacker):
        return




    def attack(self, target,damage,damage_type="physical"):
        multiplyer=1
        #check if it's a damage ability a
        if random.randint(1, 100) <= self.crit_chance and damage>0:
            multiplyer = 2  # Double the damage for critical hit
        print(f"{self.name} attacks {target.name}!")

        
        if damage>0:
            if damage_type=="physical":
                damage_after_def=int(damage*multiplyer*(1-target.physical_defense/(target.physical_defense+100))) #reduce damage with defesnse
            elif damage_type=="magical":
                damage_after_def=int(damage*multiplyer*(1-target.magical_defense/(target.magical_defense+100))) #reduce damage with defesnse
        else:
            damage_after_def=damage

        if target.unit_type=="base" and target.barrier_status=="Up":
            damage_after_def=0
        target.health -= damage_after_def  
        target.damage_taken = damage_after_def 
        target.damage_taken_type=damage_type
        target.last_damage_time = pygame.time.get_ticks() 
        if target.health <= 0:
            target.health = 0
            target.alive = False
        target.react_to_attack(self)  # Trigger monster reaction
        return damage_after_def
        



    def update_buffs_and_debuffs(self):
            # Handle buffs
            if self.buff_duration > 0:
                self.buff_duration -= 1
                if self.buff_duration == 0:
                    print(f"{self.name}'s buff has expired.")
                    self.revert_buff()

            # Handle debuffs
            if self.debuff_duration > 0:
                self.debuff_duration -= 1
                if self.debuff_duration == 0:
                    print(f"{self.name}'s debuff has expired.")
                    self.revert_debuff()




    def revert_buff(self):
        # Revert buff effects
        self.damage -= self.buffed_damage_increase
        self.physical_defense -= self.buffed_defense_increase
        self.magical_defense -= self.buffed_defense_increase
        self.buffed_damage_increase = 0
        self.buffed_defense_increase = 0
        self.is_buffed = False
        print(f"{self.name}'s stats after buff ended: Damage: {self.damage}, Defense: {self.physical_defense } and {self.physical_defense} ")




    def revert_debuff(self):
        # Revert debuff effects
        self.damage += self.debuffed_attack_reduction
        self.physical_defense += self.buffed_defense_increase
        self.magical_defense += self.buffed_defense_increase
        self.debuffed_attack_reduction = 0
        self.debuffed_defense_reduction = 0
        self.is_debuffed = False
        print(f"{self.name}'s stats after debuff ended: Damage: {self.damage}, Defense: {self.physical_defense } and {self.physical_defense} ")




    def draw(self, screen, is_current_turn):
        # Draw the unit's image inside the square
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE)), rect)

        # Health bar settings
        health_ratio = self.health / self.max_health
        health_bar_full_width = int(CELL_SIZE * UI.HEALTH_BAR_WIDTH_RATIO)
        health_bar_width = int(CELL_SIZE * health_ratio * UI.HEALTH_BAR_WIDTH_RATIO)
        health_bar_height = UI.HEALTH_BAR_HEIGHT
        health_bar_x = self.x * CELL_SIZE + UI.HEALTH_BAR_MARGIN
        health_bar_y = self.y * CELL_SIZE + UI.HEALTH_BAR_MARGIN
        border_radius = UI.HEALTH_BAR_BORDER_RADIUS

        # Border settings
        border_thickness = UI.HEALTH_BAR_BORDER_THICKNESS
        border_x = health_bar_x - border_thickness
        border_y = health_bar_y - border_thickness
        border_width = health_bar_width/health_ratio + (2 * border_thickness)
        border_height = health_bar_height + (2 * border_thickness)

        # Draw the black border
        pygame.draw.rect(screen, Colors.BLACK, (border_x, border_y, border_width, border_height), border_radius=border_radius)

        # Glow effect for the current player's turn
        if is_current_turn:
            glow_rect = pygame.Rect(health_bar_x - 2, health_bar_y - 2, health_bar_full_width + 4, health_bar_height + 4)
            pygame.draw.rect(screen, Colors.YELLOW, glow_rect, border_radius=5)

        # Health bar background (gray for missing health)
        pygame.draw.rect(screen, Colors.BLACK, (health_bar_x, health_bar_y, CELL_SIZE - 4, health_bar_height), border_radius=border_radius)

        # Health bar foreground
        if self.color == "blue":
            health_color = Colors.BLUE_TEAM
        elif self.color == "red":
            health_color = Colors.RED_TEAM
        else:
            health_color = Colors.PURPLE
        pygame.draw.rect(screen, health_color, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), border_radius=border_radius)

        # Draw HP markers
        num_segments = self.health // UI.HEALTH_SEGMENT_SIZE
        for i in range(1, num_segments):
            marker_x = health_bar_x + (health_bar_width * i / num_segments)
            pygame.draw.line(screen, Colors.BLACK, (marker_x, health_bar_y), (marker_x, health_bar_y + health_bar_height - 3), 1)

        # Glossy overlay on the health bar
        gloss_surface = pygame.Surface((health_bar_width * 0.85, int(health_bar_height / 3)), pygame.SRCALPHA)
        gloss_surface.fill((255, 255, 255, 150))
        screen.blit(gloss_surface, (health_bar_x + 1, health_bar_y + 1))

        # Draw damage text with a black boundary
        if hasattr(self, "last_damage_time") and hasattr(self, "damage_taken") and self.damage_taken != 0:
            time_passed = pygame.time.get_ticks() - self.last_damage_time

            if time_passed < Gameplay.DAMAGE_DISPLAY_DURATION_MS:
                # Calculate alpha (opacity) and vertical position
                alpha = max(255 - (time_passed // UI.DAMAGE_TEXT_FADE_RATE), 0)
                offset_y = -time_passed // UI.DAMAGE_TEXT_RISE_RATE + 15

                # Determine flash color based on damage type
                if self.damage_taken > 0:
                    A = 255
                else:
                    A = 0

                # Purple for magical damage, red for physical
                if self.damage_taken_type == "magical":
                    B = 255
                else:
                    B = 0

                if time_passed < 200:
                    flash_overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    flash_overlay.fill((A, 255 - A, 0, 100))
                    screen.blit(flash_overlay, rect)

                # Create the text surface with fading effect
                font = pygame.font.Font(Assets.FONT_RUSSO, UI.DAMAGE_TEXT_SIZE)
                if self.damage_taken>0:
                    text_surface = font.render(f"-{abs(self.damage_taken)}", True, (A, 255-A, B))
                    outline_surface = font.render(f"-{abs(self.damage_taken)}", True, (0, 0, 0))
                else:
                    text_surface = font.render(f"+{abs(self.damage_taken)}", True, (A, 255-A, 0))
                    outline_surface = font.render(f"+{abs(self.damage_taken)}", True, (0, 0, 0))
                text_surface.set_alpha(alpha)

                # Add a black outline
                #outline_surface = font.render(f"-{abs(self.damage_taken)}", True, (0, 0, 0))
                outline_surface.set_alpha(alpha)

                # Draw the outline slightly offset in each direction
                x = self.x * CELL_SIZE + CELL_SIZE // 2 - text_surface.get_width() // 2
                y = self.y * CELL_SIZE + offset_y
                for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    screen.blit(outline_surface, (x + dx, y + dy))

                # Draw the text
                screen.blit(text_surface, (x, y))
            else:
                # Clear the damage_taken attribute after animation ends
                self.damage_taken = 0

        # Draw upward arrow if buffed and duration > 0
        if self.buff_duration > 0:
            arrow_center = (self.x * CELL_SIZE + UI.BUFF_ARROW_OFFSET_X, self.y * CELL_SIZE + CELL_SIZE - 2)
            pygame.draw.polygon(screen, Colors.GREEN, [
                (arrow_center[0], arrow_center[1] - UI.ARROW_SIZE),
                (arrow_center[0] - 5, arrow_center[1]),
                (arrow_center[0] + 5, arrow_center[1])
            ])

        # Draw downward arrow if debuffed and duration > 0
        if self.debuff_duration > 0:
            arrow_center = (self.x * CELL_SIZE + UI.DEBUFF_ARROW_OFFSET_X, self.y * CELL_SIZE + CELL_SIZE - 12)
            pygame.draw.polygon(screen, Colors.RED, [
                (arrow_center[0], arrow_center[1] + UI.ARROW_SIZE),
                (arrow_center[0] - 5, arrow_center[1]),
                (arrow_center[0] + 5, arrow_center[1])
            ])




                
class MonsterUnit(Unit):
    def __init__(self, x, y, name, health, damage,physical_defense,magical_defense,crit_chance,image_path, color, move_range, attack_range, unit_type):  
        Unit.__init__(self, x, y, name, health, damage,physical_defense,magical_defense,crit_chance,image_path, color, move_range, attack_range, unit_type)




    def react_to_attack(self, attacker):
        if self.alive:
            # Attack the attacker (if in range)    
            if self.in_range(attacker):
                self.attack(attacker,self.damage)
        



            
class BaseUnit(Unit):
    def __init__(self, x, y, name, health, damage, physical_defense,magical_defense, crit_chance, image_path, color, move_range, attack_range, unit_type, barrier_status):
        super().__init__(x, y, name, health, damage, physical_defense,magical_defense, crit_chance, image_path, color, move_range, attack_range, unit_type)
        self.barrier_status = barrier_status




    def draw(self, screen, is_current_turn):
        """Draw the Nexus along with its barrier status."""
        # Call the parent draw method
        super().draw(screen, is_current_turn)

        # Draw barrier status text above the Nexus
        font = pygame.font.Font(None, 24)
        barrier_status_text = "Barrier: UP" if self.barrier_status == "Up" else "Barrier: DOWN"
        color = Colors.GREEN if self.barrier_status == "Up" else Colors.RED
        text_surface = font.render(barrier_status_text, True, color)
        x = self.x * CELL_SIZE + CELL_SIZE // 2 - text_surface.get_width() // 2
        y = self.y * CELL_SIZE - 20
        screen.blit(text_surface, (x, y))