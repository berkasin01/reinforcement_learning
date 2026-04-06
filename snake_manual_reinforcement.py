import pygame
import random
import numpy as np

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
SNAKE_SIZE = 20
SNAKE_SPEED = 15
ACTION_SPACE = 4  # Left, Right, Up, Down
EPISODES = 5000

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

###Sets up the initial state of the game
def reset_game():
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0
    snake = [(x, y)]
    food_x, food_y = random.randrange(0, WIDTH, SNAKE_SIZE), random.randrange(0, HEIGHT, SNAKE_SIZE)
    return x, y, dx, dy, snake, food_x, food_y


def get_state(x, y, dx, dy, snake, food_x, food_y):
    # Calculate whether there are obstacles in each direction
    danger_left = (x - SNAKE_SIZE < 0) or ((x - SNAKE_SIZE, y) in snake)
    danger_right = (x + SNAKE_SIZE >= WIDTH) or ((x + SNAKE_SIZE, y) in snake)
    danger_up = (y - SNAKE_SIZE < 0) or ((x, y - SNAKE_SIZE) in snake)
    danger_down = (y + SNAKE_SIZE >= HEIGHT) or ((x, y + SNAKE_SIZE) in snake)

    # Relative food position
    food_left = food_x < x
    food_right = food_x > x
    food_up = food_y < y
    food_down = food_y > y

    # Direction of movement
    moving_left = dx == -SNAKE_SIZE
    moving_right = dx == SNAKE_SIZE
    moving_up = dy == -SNAKE_SIZE
    moving_down = dy == SNAKE_SIZE

    # Return the state as a tuple of booleans
    return (
        danger_left, danger_right, danger_up, danger_down,
        food_left, food_right, food_up, food_down,
        moving_left, moving_right, moving_up, moving_down
    )


def game_step(action, x, y, dx, dy, snake, food_x, food_y):
    if action == 0 and not (dx == SNAKE_SIZE):  # Left
        dx, dy = -SNAKE_SIZE, 0
    elif action == 1 and not (dx == -SNAKE_SIZE):  # Right
        dx, dy = SNAKE_SIZE, 0
    elif action == 2 and not (dy == SNAKE_SIZE):  # Up
        dx, dy = 0, -SNAKE_SIZE
    elif action == 3 and not (dy == -SNAKE_SIZE):  # Down
        dx, dy = 0, SNAKE_SIZE

    x += dx
    y += dy
    snake.insert(0, (x, y))

    if x == food_x and y == food_y:
        food_x, food_y = random.randrange(0, WIDTH, SNAKE_SIZE), random.randrange(0, HEIGHT, SNAKE_SIZE)
        reward = 10
    else:
        snake.pop()
        reward = -0.1

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or len(snake) != len(set(snake)):
        game_over = True
        reward = -10
    else:
        game_over = False

    state = get_state(x, y, dx, dy, snake, food_x, food_y)
    return state, reward, game_over, x, y, dx, dy, snake, food_x, food_y


class QLearningAgent:
    def __init__(self, action_space, alpha=0.1, gamma=0.9, epsilon=1.0):
        # We now have 12 booleans in the state, leading to 2^12 states
        self.q_table = np.zeros((2 ** 12, action_space))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.action_space = action_space

    def state_to_index(self, state):
        # Convert state tuple of booleans to an index for Q-table
        return sum([2 ** i if state[i] else 0 for i in range(len(state))])

    def act(self, state):
        state_index = self.state_to_index(state)
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_space)
        else:
            return np.argmax(self.q_table[state_index])

    def update(self, state, action, reward, next_state):
        state_index = self.state_to_index(state)
        next_state_index = self.state_to_index(next_state)
        best_next_action = np.argmax(self.q_table[next_state_index])
        td_target = reward + self.gamma * self.q_table[next_state_index][best_next_action]
        td_error = td_target - self.q_table[state_index][action]
        self.q_table[state_index][action] += self.alpha * td_error


def train_agent(agent, episodes, render_episode=None):
    for episode in range(episodes):
        x, y, dx, dy, snake, food_x, food_y = reset_game()
        state = get_state(x, y, dx, dy, snake, food_x, food_y)
        total_reward = 0

        while True:
            action = agent.act(state)
            next_state, reward, game_over, x, y, dx, dy, snake, food_x, food_y = game_step(action, x, y, dx, dy, snake,
                                                                                           food_x, food_y)
            agent.update(state, action, reward, next_state)
            state = next_state
            total_reward += reward

            # If render_episode is set and matches the current episode, render the game
            if render_episode is not None and episode == render_episode:
                screen.fill(BLACK)
                for s in snake:
                    pygame.draw.rect(screen, GREEN, [s[0], s[1], SNAKE_SIZE, SNAKE_SIZE])
                pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
                pygame.display.update()
                clock.tick(SNAKE_SPEED)

            if game_over:
                break

        # Decay epsilon to reduce exploration over time
        agent.epsilon = max(agent.epsilon * 0.995, 0.01)

        if episode % 100 == 0:
            print(f"Episode {episode}: Total Reward: {total_reward}")


# Initialize agent and start training with rendering on episode 901
agent = QLearningAgent(ACTION_SPACE, alpha=0.1, gamma=0.9, epsilon=1.0)
train_agent(agent, episodes=EPISODES, render_episode=4901)` `   

pygame.quit()
