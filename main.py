from game import PingPongAI
from agent import Agent
from helper import *
import numpy as np

LEARING_RATE = 0.01
GAMMA = 0.99
EPSILON = 1.0
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.01
EPISODES = 10000
BATCH_SIZE = 128

def train():
    game = PingPongAI()
    state_size = game.get_state().shape[0]
    action_size = 3

    agent1 = Agent(state_size, action_size, LEARING_RATE, GAMMA, EPSILON, EPSILON_DECAY, EPSILON_MIN)
    agent2 = Agent(state_size, action_size, LEARING_RATE, GAMMA, EPSILON, EPSILON_DECAY, EPSILON_MIN)

    scores1 = []
    scores2 = []

    fig, ax, line1, line2 = setup_plot()

    for episode in range(EPISODES):
        state = game.reset()
        state = np.reshape(state, [1, state_size])
        done = False

        while not done:
            action1 = agent1.act(state)
            action2 = agent2.act(state)

            next_state, reward1, reward2, done = game.step(action1, action2)
            next_state = np.reshape(next_state, [1, state_size])

            agent1.remember(state, action1, reward1, next_state, done)
            agent2.remember(state, action2, reward2, next_state, done)

            state = next_state

            if done:
                score1, score2 = game.get_scores()
                scores1.append(score1)
                scores2.append(score2)
                update_plot(ax, line1, line2, scores1, scores2)
                print("Episode: {}/{}, AI-1 Score: {}, AI-2 Score: {}".format(episode, EPISODES, score1, score2))
                break
        
        if len(agent1.memory) > BATCH_SIZE:
            agent1.replay(BATCH_SIZE)
        if len(agent2.memory) > BATCH_SIZE:
            agent2.replay(BATCH_SIZE)

        if episode % 50 == 0:
            agent1.save("models/ping-pong-ai1.weights.h5")
            agent2.save("models/ping-pong-ai2.weights.h5")
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    train()