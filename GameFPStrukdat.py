import pygame
import random
import math

pygame.init()

### Constants (Paten)
HEIGHT, WIDTH = 720, 1280
FPS = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

### Fonts and Caption
font = pygame.font.Font(None, 50)
pygame.display.set_caption("Magician's Curse")


### Load Models
new_width = 50 
new_height = 50 

player_idle_1 = pygame.image.load("Assets/Player/Idle-1.png")
player_idle_2 = pygame.image.load("Assets/Player/Idle-2.png")

player_idle_1 = pygame.transform.scale(player_idle_1, (new_width, new_height))
player_idle_2 = pygame.transform.scale(player_idle_2, (new_width, new_height))

background = pygame.image.load("Assets/background.png")
background = pygame.transform.scale(background, (1280*1.2, 720*1.2))

### Colors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

### Variable (Paten)
CHAR_SIZE = 50
SPAWN_INTERVAL = 1000
BULLET_RADIUS = 5
BULLET_SPEED = 20
BULLET_COOLDOWN = 700
DAMAGE_BULLET = 5
DAMAGE_MELEE_WEAPON = 7
MELEE_WEAPON_RANGE = 150
MELEE_WEAPON_ANGLE = 60
MELEE_COOLDOWN = 3000
ENEMY_COLLISION_RADIUS = 60  # Increased collision radius for enemies

# Spells and incantations List
SPELLS = {
    "Fireball": {
        "incantations": [
            "may the fire from hell burn upon you",
            "fiery inferno, the great destruction",
            "corpses die in blazing fire",
            "fire"
        ],
        "color": RED
    },
    "Lightning": {
        "incantations": [
            "strike with the wrath of the storm",
            "thunder, heed my call",
            "let the heavens unleash their fury"
        ],
        "color": YELLOW
    },
    "Meteor": {
        "incantations": [
            "stars fall to destroy my foes",
            "celestial flames, rain upon the earth",
            "a fiery comet to obliterate all"
        ],
        "color": ORANGE
    },
    "Regenerate": {
        "incantations": [
            "renew my body and spirit",
            "life springs eternal within me",
            "a cycle of rebirth restores me"
        ],
        "color": GREEN
    },
    "Haste": {
        "incantations": [
            "speed of the wind, carry me forward",
            "light as a feather, swift as a hawk",
            "time slows as I accelerate"
        ],
        "color": BLUE
    },
    "Freeze": {
        "incantations": [
            "time stands still at my command",
            "halt the motion of all things",
            "freeze this moment for eternity"
        ],
        "color": CYAN
    },
    "Weaken": {
        "incantations": [
            "sap their strength and resolve",
            "drain their power, leave them fragile",
            "with my will, they crumble"
        ],
        "color": PURPLE
    },
    "Spirit": {
        "incantations": [
            "a wraith of the ether, come forth",
            "spirit of the otherworld, join me",
            "a phantom ally, answer my plea",
            "ghost"
        ],
        "color": WHITE
    }
}

# Function to activate a spell
def activate_spell(spell, player_x, player_y, bullets, fireballs):
    print(f"Spell Activated: {spell}")
    if spell == "Fireball":
        mouse_x, mouse_y = pygame.mouse.get_pos()
        fireball = Fireball(player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2, mouse_x, mouse_y)
        fireballs.append(fireball)
    elif spell == "Lightning":
        pass
    elif spell == "Meteor":
        pass
    elif spell == "Regenerate":
        pass
    elif spell == "Haste":
        pass
    elif spell == "Freeze":
        pass
    elif spell == "Weaken":
        pass
    elif spell == "Spirit":
        pass

### Classes
class Enemy:
    def __init__(self, x, y, hp, attack_damage):
        self.x = x
        self.y = y
        self.hp = hp
        self.attack_damage = attack_damage
        self.width = CHAR_SIZE
        self.height = CHAR_SIZE
        self.speed = 2
        self.idle_counter = 0
        self.new_width = 50
        self.new_height = 50

        # Load Image
        self.enemy_run_1 = pygame.image.load("Assets/Enemy/slimeIdle1.png")
        self.enemy_run_2 = pygame.image.load("Assets/Enemy/slimeIdle2.png")
        self.enemy_run_3 = pygame.image.load("Assets/Enemy/slimeIdle3.png")
        self.enemy_run_4 = pygame.image.load("Assets/Enemy/slimeIdle4.png")

        self.enemy_run_1 = pygame.transform.scale(self.enemy_run_1, (self.new_width, self.new_height))
        self.enemy_run_2 = pygame.transform.scale(self.enemy_run_2, (self.new_width, self.new_height))
        self.enemy_run_3 = pygame.transform.scale(self.enemy_run_3, (self.new_width, self.new_height))
        self.enemy_run_4 = pygame.transform.scale(self.enemy_run_4, (self.new_width, self.new_height))

        self.enemy_image = self.enemy_run_1  # Default to the first frame

    def move(self):
        # Flip the image based on movement direction
        if self.speed > 0:
            # Moving right, no need to flip
            self.enemy_image = self.enemy_run_1
        elif self.speed < 0:
            # Moving left, flip the image
            self.enemy_image = pygame.transform.flip(self.enemy_run_1, False, True)

    def draw(self, window):
        if self.speed != 0:  # If enemy is moving
            if self.idle_counter // 15 % 4 == 0:
                self.enemy_image = self.enemy_run_1
            elif self.idle_counter // 15 % 4 == 1:
                self.enemy_image = self.enemy_run_2
            elif self.idle_counter // 15 % 4 == 2:
                self.enemy_image = self.enemy_run_3
            elif self.idle_counter // 15 % 4 == 3:
                self.enemy_image = self.enemy_run_4

            # Increment idle counter to cycle through frames
            self.idle_counter += 1

        # Draw the current frame of the animation
        self.move()

        WIN.blit(self.enemy_image, (self.x, self.y))

        # Enemy health text
        hp_text = font.render(str(self.hp), True, WHITE)
        text_rect = hp_text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2 - 30))
        window.blit(hp_text, text_rect)

    def update(self, player_x, player_y, enemies, spell_box):

        self.move()

        WIN.blit(self.enemy_image, (self.x, self.y))

        # Slow enemies down when spell box is active
        if spell_box == 1:
            self.speed = 0.5  # Slow speed
        else:
            self.speed = 2  # Normal speed

        # Move towards player
        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed

        if self.y < player_y:
            self.y += self.speed
        elif self.y > player_y:
            self.y -= self.speed

        self.idle_counter += 1

        # Check for collisions with other enemies
        for enemy in enemies:
            if enemy != self:
                # Increase collision radius
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < ENEMY_COLLISION_RADIUS:  # If enemies are too close, sundul2an
                    angle = math.atan2(self.y - enemy.y, self.x - enemy.x)
                    self.x += math.cos(angle) * self.speed
                    self.y += math.sin(angle) * self.speed

    def is_hit(self, bullet_x, bullet_y):
        return self.x < bullet_x < self.x + self.width and self.y < bullet_y < self.y + self.height

    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0

class Bullet:
    def __init__(self, x, y, target_x, target_y, speed=BULLET_SPEED, color=WHITE):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        angle = math.atan2(target_y - y, target_x - x)
        self.vel_x = self.speed * math.cos(angle)
        self.vel_y = self.speed * math.sin(angle)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), BULLET_RADIUS)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def is_out_of_bounds(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

class Fireball:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 15
        self.color = RED
        self.radius = 15  # Slightly larger than the bullet
        angle = math.atan2(target_y - y, target_x - x)
        self.vel_x = self.speed * math.cos(angle)
        self.vel_y = self.speed * math.sin(angle)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def is_out_of_bounds(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

    def check_collision(self, enemy):
        dist = math.hypot(self.x - (enemy.x + enemy.width // 2), self.y - (enemy.y + enemy.height // 2))
        if dist < self.radius + ENEMY_COLLISION_RADIUS:
            return True
        return False

### Draw
def draw_window(player_x, player_y, enemies, bullets, fireballs, spell_box_text, damage_area, bullet_cooldown_counter, melee_cooldown_counter, spell_box, active_spell_text, active_spell_color, player_hp, player_invisible=False, player_idle_counter=0):
    WIN.blit(background, (-120, -100))

     # Alternate player image every 0.5 seconds (every 15 frames at 30 FPS)
    if player_idle_counter // 15 % 2 == 0:
        player_image = player_idle_1
    else:
        player_image = player_idle_2

    # Draw the player
    WIN.blit(player_image, (player_x, player_y))

    for enemy in enemies:
        enemy.draw(WIN)

    for bullet in bullets:
        bullet.draw(WIN)

    for fireball in fireballs:
        fireball.draw(WIN)

    for start_angle, end_angle in damage_area:
        pygame.draw.line(
            WIN, WHITE,
            (player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2),
            (player_x + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.cos(start_angle),
             player_y + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.sin(start_angle)),
            2
        )
        pygame.draw.line(
            WIN, WHITE,
            (player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2),
            (player_x + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.cos(end_angle),
             player_y + CHAR_SIZE // 2 + MELEE_WEAPON_RANGE * math.sin(end_angle)),
            2
        )

    bullet_text = "READY" if bullet_cooldown_counter == 0 else f"{bullet_cooldown_counter // 1000}s"
    bullet_label = font.render(f"Bullet: {bullet_text}", True, WHITE)
    WIN.blit(bullet_label, (WIDTH - bullet_label.get_width() - 20, HEIGHT - 80))

    melee_text = "READY" if melee_cooldown_counter == 0 else f"{melee_cooldown_counter // 1000}s"
    melee_label = font.render(f"Melee: {melee_text}", True, WHITE)
    WIN.blit(melee_label, (WIDTH - melee_label.get_width() - 20, HEIGHT - 40))

    # Display player's health
    health_label = font.render(f"HP: {player_hp}", True, WHITE)
    WIN.blit(health_label, (20, 720-50))

    if spell_box == 1:
        pygame.draw.rect(WIN, WHITE, (WIDTH // 4, HEIGHT // 4, WIDTH // 2, 100), 2)
        spellbox_label = font.render("Spellbox Active", True, WHITE)
        WIN.blit(spellbox_label, (WIDTH // 4 + 10, HEIGHT // 4 - 40))
        user_input_label = font.render(spell_box_text, True, WHITE)
        WIN.blit(user_input_label, (WIDTH // 4 + 10, HEIGHT // 4 + 30))

    if active_spell_text:
        active_spell_label = font.render(active_spell_text, True, active_spell_color)
        WIN.blit(active_spell_label, ((WIDTH - active_spell_label.get_width()) // 2, HEIGHT - 120))

    pygame.display.update()

def main():
    player_x, player_y = 590, 310
    player_hp = 3
    vel = 5
    spell_box, spell_box_text = 0, ""
    enemies, bullets, fireballs = [], [], []  # Initialize the enemy, bullets, and fireballs list
    last_bullet_time, last_melee_time = 0, 0
    bullet_cooldown_counter, melee_cooldown_counter = 0, 0
    active_spell_text = ""
    active_spell_color = WHITE
    player_invisible = False
    player_idle_counter = 0

    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, SPAWN_INTERVAL)

    run_game = True
    while run_game:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        damage_area = []

        bullet_cooldown_counter = max(0, bullet_cooldown_counter - clock.get_time())
        melee_cooldown_counter = max(0, melee_cooldown_counter - clock.get_time())


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            if event.type == pygame.KEYDOWN:
                if spell_box == 1:
                    if event.key == pygame.K_BACKSPACE:
                        spell_box_text = spell_box_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        spell_box, spell_box_text = 0, ""
                    else:
                        spell_box_text += event.unicode
                elif event.key == pygame.K_i:
                    spell_box = 1

            if event.type == pygame.USEREVENT:
                side = random.choice(["left", "right"])
                x = 0 if side == "left" else WIDTH - CHAR_SIZE
                y = random.randint(0, HEIGHT - CHAR_SIZE)
                hp, attack_damage = 15, random.randint(5, 20)
                enemies.append(Enemy(x, y, hp, attack_damage))

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left-click: Shooting bullets
                if event.button == 1:
                    if bullet_cooldown_counter == 0:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        bullets.append(Bullet(player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2, mouse_x, mouse_y))
                        bullet_cooldown_counter = BULLET_COOLDOWN

                # Right-click: Melee attack
                elif event.button == 3:
                    if melee_cooldown_counter == 0:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + CHAR_SIZE // 2), mouse_x - (player_x + CHAR_SIZE // 2)))

                        start_angle = math.radians(angle_to_mouse + MELEE_WEAPON_ANGLE / 2)
                        end_angle = math.radians(angle_to_mouse - MELEE_WEAPON_ANGLE / 2)
                        damage_area.append((start_angle, end_angle))

                        for enemy in enemies[:]:
                            enemy_center_x, enemy_center_y = enemy.x + enemy.width // 2, enemy.y + enemy.height // 2
                            distance = math.hypot(enemy_center_x - (player_x + CHAR_SIZE // 2), enemy_center_y - (player_y + CHAR_SIZE // 2))

                            if distance <= MELEE_WEAPON_RANGE:
                                angle_to_enemy = math.degrees(math.atan2(enemy_center_y - (player_y + CHAR_SIZE // 2), enemy_center_x - (player_x + CHAR_SIZE // 2)))
                                angle_diff = (angle_to_enemy - angle_to_mouse + 360) % 360

                                if angle_diff <= MELEE_WEAPON_ANGLE / 2 or angle_diff >= 360 - MELEE_WEAPON_ANGLE / 2:
                                    if enemy.take_damage(DAMAGE_MELEE_WEAPON):
                                        enemies.remove(enemy)
                        melee_cooldown_counter = MELEE_COOLDOWN

                # Middle-click: Activate Fireball spell if ready
                elif event.button == 2:
                    if active_spell_text.endswith("READY"):  # Check if spell is ready
                        spell_name = active_spell_text.split()[0]  # Extract the spell name from the active text
                        activate_spell(spell_name, player_x, player_y, bullets, fireballs)  # Pass the fireballs list here
                        active_spell_text = ""  # Reset after activation
                        active_spell_color = WHITE  # Reset color


        keys = pygame.key.get_pressed()
        if spell_box == 0:
            if keys[pygame.K_a]:
                player_x -= vel
            if keys[pygame.K_d]:
                player_x += vel
            if keys[pygame.K_w]:
                player_y -= vel
            if keys[pygame.K_s]:
                player_y += vel

        player_x = max(0, min(player_x, WIDTH - CHAR_SIZE))
        player_y = max(0, min(player_y, HEIGHT - CHAR_SIZE))

        for enemy in enemies:
            enemy.update(player_x, player_y, enemies, spell_box)

        if pygame.mouse.get_pressed()[0] and bullet_cooldown_counter == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullets.append(Bullet(player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2, mouse_x, mouse_y))
            bullet_cooldown_counter = BULLET_COOLDOWN

        if pygame.mouse.get_pressed()[2] and melee_cooldown_counter == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + CHAR_SIZE // 2), mouse_x - (player_x + CHAR_SIZE // 2)))

            start_angle = math.radians(angle_to_mouse + MELEE_WEAPON_ANGLE / 2)
            end_angle = math.radians(angle_to_mouse - MELEE_WEAPON_ANGLE / 2)
            damage_area.append((start_angle, end_angle))

            for enemy in enemies[:]:
                enemy_center_x, enemy_center_y = enemy.x + enemy.width // 2, enemy.y + enemy.height // 2
                distance = math.hypot(enemy_center_x - (player_x + CHAR_SIZE // 2), enemy_center_y - (player_y + CHAR_SIZE // 2))

                if distance <= MELEE_WEAPON_RANGE:
                    angle_to_enemy = math.degrees(math.atan2(enemy_center_y - (player_y + CHAR_SIZE // 2), enemy_center_x - (player_x + CHAR_SIZE // 2)))
                    angle_diff = (angle_to_enemy - angle_to_mouse + 360) % 360

                    if angle_diff <= MELEE_WEAPON_ANGLE / 2 or angle_diff >= 360 - MELEE_WEAPON_ANGLE / 2:
                        if enemy.take_damage(DAMAGE_MELEE_WEAPON):
                            enemies.remove(enemy)
            melee_cooldown_counter = MELEE_COOLDOWN

        for enemy in enemies[:]:
            enemy_center_x, enemy_center_y = enemy.x + enemy.width // 2, enemy.y + enemy.height // 2
            player_center_x, player_center_y = player_x + CHAR_SIZE // 2, player_y + CHAR_SIZE // 2
            distance = math.hypot(enemy_center_x - player_center_x, enemy_center_y - player_center_y)

            if distance < ENEMY_COLLISION_RADIUS:  # If the enemy collides with the player
                player_hp -= 1
                enemies.remove(enemy)  # Remove the enemy on collision

        if player_hp <= 0:
            
            game_over_label = font.render("Game Over!", True, WHITE)
            WIN.blit(game_over_label, ((WIDTH - game_over_label.get_width()) // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            run_game = False

        for bullet in bullets[:]:
            bullet.update()
            if bullet.is_out_of_bounds():
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if enemy.is_hit(bullet.x, bullet.y):
                        if enemy.take_damage(DAMAGE_BULLET):
                            enemies.remove(enemy)
                        bullets.remove(bullet)
        
        for fireball in fireballs[:]:
            fireball.update()
            if fireball.is_out_of_bounds():
                fireballs.remove(fireball)
            else:
                for enemy in enemies[:]:
                    if fireball.check_collision(enemy):
                        if enemy.take_damage(15):
                            enemies.remove(enemy)
                        
        # Update spell box logic when it's active
        if spell_box == 1 and spell_box_text:
            for spell, data in SPELLS.items():
                if spell_box_text.lower() in [incantation.lower() for incantation in data["incantations"]]:
                    spell_box = 0
                    spell_box_text = ""
                    active_spell_text = f"{spell} READY"  # Show the "READY" status for the matched spell
                    active_spell_color = data["color"]
                    break  # Stop checking once a match is found

        player_idle_counter += 1  # Increment the idle counter to cycle through player's frames

        draw_window(player_x, player_y, enemies, bullets, fireballs, spell_box_text, damage_area, bullet_cooldown_counter, melee_cooldown_counter, spell_box, active_spell_text, active_spell_color, player_hp, player_invisible, player_idle_counter)
        

    pygame.quit()


if __name__ == "__main__":
    main()
