import pygame
import random
import math
pygame.init()

# Constants
HEIGHT, WIDTH = 720, 1280
FPS = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# FONT
font = pygame.font.Font(None, 50)
pygame.display.set_caption("Anomaly")

# COLOURS
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# VARIABLE (PATTERN)
CHAR_SIZE = 50
SPAWN_INTERVAL = 1000  # in milliseconds (1 second)
BULLET_RADIUS = 5
BULLET_SPEED = 20
BULLET_COOLDOWN = 700  # in milliseconds
DAMAGE_BULLET = 5  # Damage to enemies when hit by a bullet
DAMAGE_MELEE_WEAPON = 7  # Damage of the new melee weapon
MELEE_WEAPON_RANGE = 100  # Range of the melee weapon
MELEE_WEAPON_ANGLE = 60  # Attack cone angle in degrees
MELEE_COOLDOWN = 3000  # in milliseconds (5 seconds cooldown for melee)

class Enemy:
    def __init__(self, x, y, hp, attack_damage):
        self.x = x
        self.y = y
        self.hp = hp
        self.attack_damage = attack_damage
        self.width = CHAR_SIZE
        self.height = CHAR_SIZE
        self.speed = 2  # Speed of the enemy

    def draw(self, window):
        pygame.draw.rect(window, BLUE, (self.x, self.y, self.width, self.height))

        # Draw HP text in the middle of the enemy
        hp_text = font.render(str(self.hp), True, WHITE)
        text_rect = hp_text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        window.blit(hp_text, text_rect)

    def update(self, player_x, player_y):
        # Move towards the player
        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed

        if self.y < player_y:
            self.y += self.speed
        elif self.y > player_y:
            self.y -= self.speed

    def is_hit(self, bullet_x, bullet_y):
        return self.x < bullet_x < self.x + self.width and self.y < bullet_y < self.y + self.height

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            return True  # Indicates that the enemy is dead
        return False

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        angle = math.atan2(target_y - y, target_x - x)
        self.vel_x = BULLET_SPEED * math.cos(angle)
        self.vel_y = BULLET_SPEED * math.sin(angle)

    def draw(self, window):
        pygame.draw.circle(window, WHITE, (int(self.x), int(self.y)), BULLET_RADIUS)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def is_out_of_bounds(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

def draw_window(player_x, player_y, enemies, bullets, spell_box_text, damage_area, bullet_cooldown_counter, melee_cooldown_counter, spell_box):
    WIN.fill(GREEN)

    # Player
    pygame.draw.rect(WIN, RED, (player_x, player_y, CHAR_SIZE, CHAR_SIZE))

    # Enemies
    for enemy in enemies:
        enemy.draw(WIN)

    # Bullets
    for bullet in bullets:
        bullet.draw(WIN)

    # Damage Area Visualization ("X" shape melee weapon)
    for start_angle, end_angle in damage_area:
        pygame.draw.line(WIN, WHITE, 
                         (player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2),
                         (player_x + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.cos(start_angle),
                          player_y + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.sin(start_angle)), 
                         2)
        pygame.draw.line(WIN, WHITE, 
                         (player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2),
                         (player_x + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.cos(end_angle),
                          player_y + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.sin(end_angle)), 
                         2)

    # Draw Cooldown Timers with "READY" or Countdown
    bullet_cooldown_text = "READY" if bullet_cooldown_counter == 0 else f"{bullet_cooldown_counter // 1000}s"
    bullet_cooldown_label = font.render(f"Bullet: {bullet_cooldown_text}", True, WHITE)
    WIN.blit(bullet_cooldown_label, (WIDTH - bullet_cooldown_label.get_width() - 20, HEIGHT - 80))

    melee_cooldown_text = "READY" if melee_cooldown_counter == 0 else f"{melee_cooldown_counter // 1000}s"
    melee_cooldown_label = font.render(f"Melee: {melee_cooldown_text}", True, WHITE)
    WIN.blit(melee_cooldown_label, (WIDTH - melee_cooldown_label.get_width() - 20, HEIGHT - 40))

    # Spell Box UI - display when active
    if spell_box == 1:
        # Draw Spellbox box
        pygame.draw.rect(WIN, WHITE, (WIDTH // 4, HEIGHT // 4, WIDTH // 2, 100), 2)  # Spellbox box
        # Draw text "Spellbox Active"
        spellbox_text = font.render("Spellbox Active", True, WHITE)
        WIN.blit(spellbox_text, (WIDTH // 4 + 10, HEIGHT // 4 - 40))
        # Draw the text that the player types
        user_input_text = font.render(spell_box_text, True, WHITE)
        WIN.blit(user_input_text, (WIDTH // 4 + 10, HEIGHT // 4 + 30))

def main():
    global spell_box  # Track if the spell box is active
    global spell_box_text  # Track the text typed in the spell box

    # VARIABLES (NEED TO UPDATE)
    player_x, player_y = 590, 310
    vel = 5
    spell_box = 0  # Spell box is initially closed (inactive)
    spell_box_text = ""  # Stores the text typed by the player in the spellbox
    enemies = []
    bullets = []
    last_bullet_time = 0
    last_melee_time = 0  # Track last time melee was used
    bullet_cooldown_counter = 0
    melee_cooldown_counter = 0

    run_game = True
    clock = pygame.time.Clock()

    # Spawn timer
    pygame.time.set_timer(pygame.USEREVENT, SPAWN_INTERVAL)

    ### EVENT CHECKER
    while run_game:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        damage_area = []  # Reset damage areas each frame

        # Cooldown counters
        bullet_cooldown_counter = max(0, bullet_cooldown_counter - clock.get_time())
        melee_cooldown_counter = max(0, melee_cooldown_counter - clock.get_time())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # exit
                run_game = False

            # Spellbox event handling
            if event.type == pygame.KEYDOWN:
                if spell_box == 1:  # If the spell box is active
                    if event.key == pygame.K_BACKSPACE:
                        spell_box_text = spell_box_text[:-1]  # Remove the last character
                    elif event.key == pygame.K_ESCAPE:
                        spell_box = 0  # Close the spell box when Escape is pressed
                        spell_box_text = ""  # Reset the text when closing the spell box
                    else:
                        spell_box_text += event.unicode  # Add the typed character
                else:  # If the spell box is not active
                    if event.key == pygame.K_i:
                        spell_box = 1  # Activate the spell box when 'i' is pressed

            # Spawn enemy
            if event.type == pygame.USEREVENT:
                side = random.choice(["left", "right"])
                x = 0 if side == "left" else WIDTH - CHAR_SIZE
                y = random.randint(0, HEIGHT - CHAR_SIZE)
                hp = 15  # Initial HP of the enemy
                attack_damage = random.randint(5, 20)
                enemies.append(Enemy(x, y, hp, attack_damage))

        keys = pygame.key.get_pressed()

        # Player movement restrictions when spell box is active
        if spell_box == 0:  # Only allow player movement if spell box is inactive
            # Player Control
            if keys[pygame.K_a]:  # LEFT
                player_x -= vel
            if keys[pygame.K_d]:  # RIGHT
                player_x += vel
            if keys[pygame.K_w]:  # UP
                player_y -= vel
            if keys[pygame.K_s]:  # DOWN
                player_y += vel

        # Map Area for Player bound
        player_x = max(0, min(player_x, WIDTH - CHAR_SIZE))
        player_y = max(0, min(player_y, HEIGHT - CHAR_SIZE))

        # Enemy movement speed reduction when spell box is active
        for enemy in enemies:
            if spell_box == 1:  # Slow down enemies if spell box is active
                enemy.speed = 1  # Reduced speed
            else:
                enemy.speed = 2  # Normal speed

        # Shooting bullets with cooldown
        if pygame.mouse.get_pressed()[0] and bullet_cooldown_counter == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullets.append(Bullet(player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2, mouse_x, mouse_y))
            bullet_cooldown_counter = BULLET_COOLDOWN

        # Melee Weapon Activation (Right Click)
        if pygame.mouse.get_pressed()[2] and melee_cooldown_counter == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Calculate the angle between the player's center and the mouse position
            angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + CHAR_SIZE // 2), mouse_x - (player_x + CHAR_SIZE // 2)))

            # Invert the arc by swapping the start and end angles
            start_angle = math.radians(angle_to_mouse + MELEE_WEAPON_ANGLE / 2)
            end_angle = math.radians(angle_to_mouse - MELEE_WEAPON_ANGLE / 2)

            # Display attack range visualization as a cross ("X")
            damage_area.append((start_angle, end_angle))

            # Melee attack logic
            for enemy in enemies[:]:
                enemy_center_x = enemy.x + enemy.width // 2
                enemy_center_y = enemy.y + enemy.height // 2
                distance = math.hypot(enemy_center_x - (player_x + CHAR_SIZE // 2), enemy_center_y - (player_y + CHAR_SIZE // 2))

                if distance <= MELEE_WEAPON_RANGE:
                    angle_to_enemy = math.degrees(math.atan2(enemy_center_y - (player_y + CHAR_SIZE // 2), enemy_center_x - (player_x + CHAR_SIZE // 2)))
                    angle_diff = (angle_to_enemy - angle_to_mouse + 360) % 360

                    if angle_diff <= MELEE_WEAPON_ANGLE / 2 or angle_diff >= 360 - MELEE_WEAPON_ANGLE / 2:
                        if enemy.take_damage(DAMAGE_MELEE_WEAPON):
                            enemies.remove(enemy)
            melee_cooldown_counter = MELEE_COOLDOWN

        # Update bullets
        for bullet in bullets[:]:  # Iterating over a copy of the list
            bullet.update()
            if bullet.is_out_of_bounds():
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:  # Check each enemy for collision with this bullet
                    if enemy.is_hit(bullet.x, bullet.y):
                        if enemy.take_damage(DAMAGE_BULLET):
                            enemies.remove(enemy)
                        if bullet in bullets:  # Check if bullet is still in the list before removing
                            bullets.remove(bullet)


        # Update enemies
        for enemy in enemies:
            enemy.update(player_x, player_y)

        # Draw the game window
        draw_window(player_x, player_y, enemies, bullets, spell_box_text, damage_area, bullet_cooldown_counter, melee_cooldown_counter, spell_box)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
ddd