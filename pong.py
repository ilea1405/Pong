import pygame, sys

# General setup
pygame.init()

# Setting up the main window
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255,255,255)

class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, WHITE)
 
    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, WHITE)
        display.blit(self.text, (600, 690))

class BALL: 
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.radius = 10
        self.speed_x = 5
        self.speed_y = 5
        self.color = WHITE

    def check_paddle_collision(self, paddle):
        if (self.x - self.radius <= paddle.x + paddle.width and
            self.x + self.radius >= paddle.x and
            self.y + self.radius >= paddle.y and
            self.y - self.radius <= paddle.y + paddle.height):
            self.speed_x *= -1

    def update(self, player1, player2, score):
        if not paused:
            self.x += self.speed_x
            self.y += self.speed_y

            # Collision detection with player1 (left paddle)
            self.check_paddle_collision(player1)

            # Collision detection with player2 (right paddle)
            self.check_paddle_collision(player2)

            # Ball hits the top or bottom boundary
            if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
                self.speed_y *= -1

            # Ball goes beyond the left or right boundary
            if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
                # Handle scoring or reset the ball's position, for example:
                score.update(self)
                self.x = WIDTH / 2
                self.y = HEIGHT / 2

    def render(self, display):
        pygame.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)

class PADDLE:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 5
        self.width = 0
        self.width = 20
        self.height = 100
        self.color = WHITE

    def update(self):
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height

    def render(self, display):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.height))

class SCORE:
    def __init__(self):
        self.player1 = 0
        self.player2 = 0
        self.font = pygame.font.SysFont("Verdana", 40)

    def update(self, ball):
        if ball.x - ball.radius <= 0:
            self.player2 += 1
        elif ball.x + ball.radius >= WIDTH:
            self.player1 += 1
    
    def render(self, display):
        text = self.font.render(str(self.player1), True, WHITE)
        display.blit(text, (WIDTH // 2 - text.get_width() - 40, 10))
        text = self.font.render(str(self.player2), True, WHITE)
        display.blit(text, (WIDTH // 2 - text.get_width() + 40, 10))

fps = FPS()
ball = BALL()
player1 = PADDLE()
player1.x = 20
player1.y = 320
player2 = PADDLE()
player2.x = 1240
player2.y = 320
score = SCORE()

# Initialize dictionary to track key states for player 1 and player 2
key_states = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_w: False, pygame.K_s: False}
paused = False

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
        # Track key presses and releases
        if event.type == pygame.KEYDOWN:
            if event.key in key_states:
                key_states[event.key] = True
        if event.type == pygame.KEYUP:
            if event.key in key_states:
                key_states[event.key] = False

    if not paused:  # Check if the game is not paused
        # Move the paddles based on key states
        if key_states[pygame.K_UP]:
            player2.y -= player2.speed
        if key_states[pygame.K_DOWN]:
            player2.y += player2.speed
        if key_states[pygame.K_w]:
            player1.y -= player1.speed
        if key_states[pygame.K_s]:
            player1.y += player1.speed


    # Updating the window
    screen.fill((0, 0, 0))
    
    # Render game elements
    fps.render(screen)
    player1.render(screen)
    player2.render(screen)
    player1.update()
    player2.update()
    ball.render(screen)
    ball.update(player1, player2, score)
    score.render(screen)
    
    if paused:
        # Display 'Paused' text when the game is paused
        font = pygame.font.SysFont("Verdana", 40)
        text = font.render("Paused", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    
    pygame.display.flip()
    fps.clock.tick(60)