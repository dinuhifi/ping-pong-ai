import pygame
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
PADDLE_SPEED = 30
BALL_SIZE = 20
BALL_SPEED = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

class PingPongAI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.paddle1_score = 0
        self.paddle2_score = 0

        self.paddle1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.paddle2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

        self.ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2

        self.ball_vel_x = BALL_SPEED if np.random.rand() < 0.5 else -BALL_SPEED
        self.ball_vel_y = BALL_SPEED if np.random.rand() < 0.5 else -BALL_SPEED

        self.frame = 0

        return self.get_state()
    
    def step(self, action1, action2):
        self.frame += 1
        reward1, reward2, done = 0, 0, False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move_paddle(action1, "paddle1")
        self.move_paddle(action2, "paddle2")

        self.ball_x += self.ball_vel_x
        self.ball_y += self.ball_vel_y

        if self.ball_y <= 0 or self.ball_y >= SCREEN_HEIGHT - BALL_SIZE:
            self.ball_vel_y = -self.ball_vel_y
        
        if self.ball_hits_paddle("paddle1"):
            self.ball_vel_x = -self.ball_vel_x
            self.paddle1_score += 1
            reward1 = 50
        elif self.ball_hits_paddle("paddle2"):
            self.ball_vel_x = -self.ball_vel_x
            self.paddle2_score += 1
            reward2 = 50
        
        if self.ball_x <= 0:
            reward1 = -30
            done = True
        elif self.ball_x >= SCREEN_WIDTH - BALL_SIZE:
            reward2 = -30
            done = True
        
        self.render()
        self.update_display()
        
        return self.get_state(), reward1, reward2, done

    def get_state(self):
        return np.array(
            [self.paddle1_y, self.paddle2_y,
             self.ball_x, self.ball_y]
        )

    def render(self):
        self.screen.fill(BLACK)

        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
        pygame.draw.rect(self.screen, WHITE, (0, self.paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH - PADDLE_WIDTH, self.paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(self.screen, WHITE, (self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE))
        
    def move_paddle(self, action, paddle):
        if paddle == "paddle1":
            if action == 1:
                self.paddle1_y = max(self.paddle1_y - PADDLE_SPEED, 0)
            elif action == 2:
                self.paddle1_y = min(self.paddle1_y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)
        elif paddle == "paddle2":
            if action == 1:
                self.paddle2_y = max(self.paddle2_y - PADDLE_SPEED, 0)
            elif action == 2:
                self.paddle2_y = min(self.paddle2_y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)

    def ball_hits_paddle(self, paddle):
        if paddle == "paddle1":
            return self.ball_x <= PADDLE_WIDTH and self.paddle1_y <= self.ball_y <= self.paddle1_y + PADDLE_HEIGHT
        elif paddle == "paddle2":
            return self.ball_x >= SCREEN_WIDTH - PADDLE_WIDTH - BALL_SIZE and self.paddle2_y <= self.ball_y <= self.paddle2_y + PADDLE_HEIGHT

    def get_scores(self):
        return self.paddle1_score, self.paddle2_score
    
    def update_display(self):
        pygame.display.flip()
        self.clock.tick(60)
