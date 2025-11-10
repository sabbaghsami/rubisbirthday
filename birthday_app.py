import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Firework colors
COLORS = [
    (255, 0, 0),      # Red
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 191, 255),    # Deep Sky Blue
    (138, 43, 226),   # Blue Violet
    (255, 20, 147),   # Deep Pink
    (255, 215, 0),    # Gold
]


class Particle:
    """Particle for firework explosions"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = 255
        self.gravity = 0.15
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 3

    def draw(self, screen):
        if self.lifetime > 0:
            alpha_color = (*self.color, max(0, self.lifetime))
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, alpha_color, (self.size, self.size), self.size)
            screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))

    def is_alive(self):
        return self.lifetime > 0


class Firework:
    """Firework that launches and explodes"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_y = random.randint(150, 400)
        self.color = random.choice(COLORS)
        self.vy = -random.uniform(8, 12)
        self.exploded = False
        self.particles = []

    def update(self):
        if not self.exploded:
            self.y += self.vy
            self.vy += 0.3
            if self.y <= self.target_y or self.vy > 0:
                self.explode()
        else:
            for particle in self.particles[:]:
                particle.update()
                if not particle.is_alive():
                    self.particles.remove(particle)

    def explode(self):
        self.exploded = True
        num_particles = random.randint(50, 100)
        for _ in range(num_particles):
            self.particles.append(Particle(self.x, self.y, self.color))

    def draw(self, screen):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
        else:
            for particle in self.particles:
                particle.draw(screen)

    def is_alive(self):
        return not self.exploded or len(self.particles) > 0


class BirthdayCake:
    """Animated birthday cake with realistic appearance"""
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.flame_offset = 0
        self.flame_direction = 1
        self.sparkle_timer = 0

    def update(self):
        self.flame_offset += 0.2 * self.flame_direction
        if abs(self.flame_offset) > 3:
            self.flame_direction *= -1
        self.sparkle_timer += 1

    def draw(self, screen):
        # Scale dimensions
        w = int(140 * self.scale)
        h = int(140 * self.scale)

        # Plate (draw first, underneath)
        plate_color = (220, 220, 220)
        plate_shadow = (150, 150, 150)
        pygame.draw.ellipse(screen, plate_shadow,
                          (self.x - w//2 - 18, self.y - 8, w + 36, 28))
        pygame.draw.ellipse(screen, plate_color,
                          (self.x - w//2 - 15, self.y - 10, w + 30, 25))
        # Plate shine
        pygame.draw.ellipse(screen, (240, 240, 240),
                          (self.x - w//2 - 10, self.y - 8, w + 20, 8))

        # Bottom layer (largest)
        layer1_h = int(45 * self.scale)
        # Main cake body
        pygame.draw.rect(screen, (101, 67, 33),
                       (self.x - w//2, self.y - layer1_h, w, layer1_h))
        # Shading on sides
        pygame.draw.rect(screen, (80, 50, 20),
                       (self.x - w//2, self.y - layer1_h, 8, layer1_h))
        pygame.draw.rect(screen, (120, 85, 45),
                       (self.x + w//2 - 8, self.y - layer1_h, 8, layer1_h))

        # Frosting on bottom layer
        frosting_points = []
        num_scallops = 12
        for i in range(num_scallops + 1):
            x_pos = self.x - w//2 + (w * i / num_scallops)
            y_pos = self.y - layer1_h + 5 * math.sin(i * 2)
            frosting_points.append((x_pos, y_pos))
        frosting_points.append((self.x + w//2, self.y - layer1_h - 8))
        frosting_points.append((self.x - w//2, self.y - layer1_h - 8))
        pygame.draw.polygon(screen, (255, 182, 193), frosting_points)

        # Middle layer
        w2 = int(w * 0.75)
        layer2_h = int(40 * self.scale)
        layer2_y = self.y - layer1_h
        pygame.draw.rect(screen, (139, 90, 43),
                       (self.x - w2//2, layer2_y - layer2_h, w2, layer2_h))
        # Shading
        pygame.draw.rect(screen, (110, 70, 30),
                       (self.x - w2//2, layer2_y - layer2_h, 6, layer2_h))
        pygame.draw.rect(screen, (160, 110, 55),
                       (self.x + w2//2 - 6, layer2_y - layer2_h, 6, layer2_h))

        # Frosting on middle layer
        frosting_points2 = []
        for i in range(num_scallops + 1):
            x_pos = self.x - w2//2 + (w2 * i / num_scallops)
            y_pos = layer2_y - layer2_h + 4 * math.sin(i * 2)
            frosting_points2.append((x_pos, y_pos))
        frosting_points2.append((self.x + w2//2, layer2_y - layer2_h - 8))
        frosting_points2.append((self.x - w2//2, layer2_y - layer2_h - 8))
        pygame.draw.polygon(screen, (255, 192, 203), frosting_points2)

        # Top layer
        w3 = int(w * 0.5)
        layer3_h = int(35 * self.scale)
        layer3_y = layer2_y - layer2_h
        pygame.draw.rect(screen, (160, 100, 50),
                       (self.x - w3//2, layer3_y - layer3_h, w3, layer3_h))
        # Shading
        pygame.draw.rect(screen, (130, 80, 40),
                       (self.x - w3//2, layer3_y - layer3_h, 5, layer3_h))
        pygame.draw.rect(screen, (180, 120, 60),
                       (self.x + w3//2 - 5, layer3_y - layer3_h, 5, layer3_h))

        # Frosting on top layer
        frosting_points3 = []
        for i in range(8):
            x_pos = self.x - w3//2 + (w3 * i / 8)
            y_pos = layer3_y - layer3_h + 3 * math.sin(i * 2.5)
            frosting_points3.append((x_pos, y_pos))
        frosting_points3.append((self.x + w3//2, layer3_y - layer3_h - 8))
        frosting_points3.append((self.x - w3//2, layer3_y - layer3_h - 8))
        pygame.draw.polygon(screen, (255, 200, 220), frosting_points3)

        # Decorative details (sprinkles/dots on frosting)
        sprinkle_colors = [(255, 0, 0), (0, 255, 0), (0, 100, 255), (255, 255, 0), (255, 0, 255)]
        random.seed(42)
        for _ in range(20):
            sx = self.x - w//2 + random.randint(5, w - 5)
            sy = self.y - layer1_h + random.randint(-5, 5)
            pygame.draw.circle(screen, random.choice(sprinkle_colors), (sx, sy), 2)
        random.seed()

        # Candles (22 candles, but we'll show 7 visible ones in a nice arrangement)
        num_candles = 7
        candle_spacing = w3 // (num_candles + 1)
        for i in range(num_candles):
            candle_x = self.x - w3//2 + candle_spacing * (i + 1)
            candle_y = layer3_y - layer3_h - 5

            candle_colors = [(255, 182, 193), (173, 216, 230), (255, 255, 200),
                           (255, 200, 200), (200, 255, 200)]
            candle_color = candle_colors[i % len(candle_colors)]

            # Candle body with stripes
            pygame.draw.rect(screen, candle_color,
                           (candle_x - 4, candle_y, 8, 30))
            # Candle shine
            pygame.draw.rect(screen, (255, 255, 255),
                           (candle_x - 3, candle_y + 2, 2, 26))
            # Spiral stripe
            for j in range(6):
                stripe_y = candle_y + j * 5
                pygame.draw.line(screen, (200, 150, 150),
                               (candle_x - 4, stripe_y), (candle_x + 4, stripe_y), 1)

            # Wick
            pygame.draw.rect(screen, (50, 50, 50),
                           (candle_x - 1, candle_y - 5, 2, 5))

            # Flame (animated)
            flame_y = candle_y + self.flame_offset
            # Outer glow
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 200, 0, 80), (10, 10), 8)
            screen.blit(s, (candle_x - 10, int(flame_y - 18)))

            # Flame shape (teardrop)
            flame_points = [
                (candle_x, int(flame_y - 18)),
                (candle_x - 4, int(flame_y - 10)),
                (candle_x - 3, int(flame_y - 6)),
                (candle_x, int(flame_y - 8)),
                (candle_x + 3, int(flame_y - 6)),
                (candle_x + 4, int(flame_y - 10)),
            ]
            pygame.draw.polygon(screen, (255, 200, 0), flame_points)
            # Inner flame
            inner_flame_points = [
                (candle_x, int(flame_y - 16)),
                (candle_x - 2, int(flame_y - 10)),
                (candle_x, int(flame_y - 9)),
                (candle_x + 2, int(flame_y - 10)),
            ]
            pygame.draw.polygon(screen, (255, 255, 100), inner_flame_points)

        # Sparkles on frosting (animated)
        if self.sparkle_timer % 20 < 10:
            for _ in range(3):
                sx = self.x - w//2 + random.randint(10, w - 10)
                sy = self.y - layer1_h + random.randint(-5, 5)
                pygame.draw.circle(screen, (255, 255, 255), (sx, sy), 2)


class ImagePopup:
    """Animated image popup that appears and fades away"""
    def __init__(self, image, screen_width, screen_height):
        self.original_image = image
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Random size between 200-400 pixels
        self.size = random.randint(200, 400)

        # Scale the image
        aspect_ratio = image.get_width() / image.get_height()
        if aspect_ratio > 1:
            new_width = self.size
            new_height = int(self.size / aspect_ratio)
        else:
            new_height = self.size
            new_width = int(self.size * aspect_ratio)

        self.image = pygame.transform.scale(image, (new_width, new_height))

        # Random position (avoid edges)
        self.x = random.randint(100, screen_width - new_width - 100)
        self.y = random.randint(100, screen_height - new_height - 100)

        # Animation properties
        self.lifetime = 180  # 3 seconds at 60 FPS
        self.max_lifetime = 180
        self.scale = 0.1
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.lifetime -= 1

        # Scale up quickly at start
        if self.scale < 1.0:
            self.scale += 0.05

        # Rotate
        self.rotation += self.rotation_speed

    def draw(self, screen):
        if self.lifetime <= 0:
            return

        # Calculate alpha based on lifetime
        if self.lifetime < 30:  # Fade out in last 0.5 seconds
            alpha = int((self.lifetime / 30) * 255)
        else:
            alpha = 255

        # Scale and rotate image
        scaled_size = (int(self.image.get_width() * self.scale),
                      int(self.image.get_height() * self.scale))
        scaled_image = pygame.transform.scale(self.image, scaled_size)
        rotated_image = pygame.transform.rotate(scaled_image, self.rotation)

        # Apply alpha
        rotated_image.set_alpha(alpha)

        # Center the image at position
        rect = rotated_image.get_rect(center=(self.x + self.image.get_width() // 2,
                                               self.y + self.image.get_height() // 2))

        # Add a glow effect
        glow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 255, 255, min(alpha // 3, 80)), glow_surface.get_rect(), border_radius=10)
        screen.blit(glow_surface, (rect.x - 10, rect.y - 10))

        screen.blit(rotated_image, rect)

    def is_alive(self):
        return self.lifetime > 0


class BirthdayApp:
    """Main birthday celebration application"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Happy 22nd Birthday Rubi! 🎂🎉")
        self.clock = pygame.time.Clock()
        self.running = True

        self.fireworks = []
        self.cakes = [
            BirthdayCake(300, 650, 1.2),
            BirthdayCake(900, 650, 1.2),
        ]

        self.firework_timer = 0
        self.firework_interval = 15  # Launch firework every 15 frames (more frequent!)

        # Image popup system
        self.firework_count = 0
        self.image_popup = None
        self.special_image = None
        self.load_special_image()

        # Fonts
        self.title_font = pygame.font.Font(None, 100)
        self.subtitle_font = pygame.font.Font(None, 50)
        self.info_font = pygame.font.Font(None, 30)

        # Music setup
        self.music_loaded = False
        self.load_music()

    def load_special_image(self):
        """Load the special image that will popup"""
        try:
            image_path = "/Users/sami.sabbagh/PycharmProjects/rubisbirthday/1000028077.jpg"
            self.special_image = pygame.image.load(image_path)
            print(f"Loaded special image: {image_path}")
        except Exception as e:
            print(f"Could not load special image: {e}")

    def load_music(self):
        """Load background music if available"""
        # Look for music files in the current directory
        music_files = [f for f in os.listdir('.') if f.endswith(('.mp3', '.wav', '.ogg'))]

        if music_files:
            try:
                pygame.mixer.music.load(music_files[0])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.music_loaded = True
                print(f"Loaded music: {music_files[0]}")
            except Exception as e:
                print(f"Could not load music: {e}")
        else:
            print("No music files found. Place an MP3, WAV, or OGG file in the directory.")

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Manual firework launch
                    x = random.randint(100, WIDTH - 100)
                    self.fireworks.append(Firework(x, HEIGHT))
                elif event.key == pygame.K_m:
                    # Toggle music
                    if self.music_loaded:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Launch firework at mouse position
                self.fireworks.append(Firework(event.pos[0], HEIGHT))

    def update(self):
        """Update all game objects"""
        # Auto-launch fireworks
        self.firework_timer += 1
        if self.firework_timer >= self.firework_interval:
            self.firework_timer = 0
            x = random.randint(100, WIDTH - 100)
            self.fireworks.append(Firework(x, HEIGHT))
            self.firework_count += 1

            # Show image popup every 15 fireworks
            if self.firework_count % 15 == 0 and self.special_image:
                self.image_popup = ImagePopup(self.special_image, WIDTH, HEIGHT)
                print(f"Image popup triggered! (Firework #{self.firework_count})")

        # Update fireworks
        for firework in self.fireworks[:]:
            firework.update()
            if not firework.is_alive():
                self.fireworks.remove(firework)

        # Update cakes
        for cake in self.cakes:
            cake.update()

        # Update image popup
        if self.image_popup:
            self.image_popup.update()
            if not self.image_popup.is_alive():
                self.image_popup = None

    def draw(self):
        """Draw everything"""
        # Background gradient (night sky)
        for y in range(HEIGHT):
            color_value = int(10 + (y / HEIGHT) * 30)
            pygame.draw.line(self.screen, (color_value, color_value, color_value * 2),
                           (0, y), (WIDTH, y))

        # Draw stars
        random.seed(42)  # Fixed seed for consistent star positions
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT // 2)
            size = random.randint(1, 2)
            pygame.draw.circle(self.screen, WHITE, (x, y), size)
        random.seed()  # Reset seed

        # Draw fireworks
        for firework in self.fireworks:
            firework.draw(self.screen)

        # Draw cakes
        for cake in self.cakes:
            cake.draw(self.screen)

        # Draw birthday message
        title_text = self.title_font.render("Happy 22nd Birthday!", True, GOLD)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))

        # Add glow effect
        glow_surface = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        glow_text = self.title_font.render("Happy 22nd Birthday!", True, (255, 215, 0, 100))
        for offset in [(0, 0), (2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_surface.blit(glow_text, (10 + offset[0], 10 + offset[1]))
        self.screen.blit(glow_surface, (title_rect.x - 10, title_rect.y - 10))
        self.screen.blit(title_text, title_rect)

        name_text = self.subtitle_font.render("RUBI", True, (255, 105, 180))
        name_rect = name_text.get_rect(center=(WIDTH // 2, 180))
        self.screen.blit(name_text, name_rect)

        # Instructions
        instructions = [
            "Click anywhere to launch fireworks!",
            "Press SPACE for random firework",
            "Press M to pause/play music",
            "Press ESC to exit"
        ]

        y_offset = HEIGHT - 120
        for instruction in instructions:
            text = self.info_font.render(instruction, True, (200, 200, 200))
            text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

        # Draw image popup (on top of everything)
        if self.image_popup:
            self.image_popup.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    app = BirthdayApp()
    app.run()
