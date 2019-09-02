from random import randrange

from keras import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from uuid import uuid4

from state.ball import Ball, Team
from state.flag import Flag
from state.state import State

from input.input import input_choices, Input
from copy import deepcopy

from numpy import ndarray, array
import numpy as np

from model.dqn_agent import DQNAgent
from state.heuristic_scores import naive_ego_to_flag


def random_state() -> State:
    x_flag, y_flag = randrange(0, 1000), randrange(0, 1000)
    x_ego, y_ego = randrange(0, 1000), randrange(0, 1000)
    ego_ball = Ball(x=x_ego, y=y_ego, id=uuid4(), team=Team.EGO)
    flag = Flag(x=x_flag, y=y_flag)
    return State([ego_ball], flag)


def reward(state: State) -> float:
    # make cost [0, 1], where we pay 1 if we are >= 1000 pixels away from the
    # goal
    cost = min(1, naive_ego_to_flag(state) / 1000 / 1000)
    return 1 - cost


def main() -> None:
    # our x, y, vx, vy relative to the flag
    input_size = 4
    # we have 9 choices of action to take.
    # 4 cardinal directions, 4 45 degree directions, and do nothing
    action_space = 9

    episodes = 5000
    dt = 200  # milliseconds
    game_length = 10000  # 10 seconds in millis

    # initialize gym environment and the agent
    agent = DQNAgent(input_size, action_space)
    # Iterate the game
    for e in range(episodes):
        # reset state in the beginning of each game
        state = random_state()
        ego = state.get_ego_ball()
        # time_t represents each frame of the game
        # Our goal is to keep the pole upright as long as possible until score of 500
        # the more time_t the more score
        for frame_num in range(0, int(game_length / dt)):
            action = agent.act(state)
            user_input = Input({ego.id: input_choices[action]})
            next_state = deepcopy(state)
            next_state.handle_input(user_input)
            next_state.next_state(dt)
            reward_val = reward(next_state)
            # print(reward_val)
            done = reward_val == 1
            # Remember the previous state, action, reward, and done
            agent.remember(state, action, reward_val, next_state, done)
            # make next_state the new current state for the next frame.
            state = next_state
            # done becomes True when the game ends
            # ex) The agent drops the pole
            if done:
                # print the score and break out of the loop
                print("episode: {}/{}, score: {}"
                      .format(e, episodes, frame_num * dt / 1000))
                break
        # train the agent with the experience of the episode
        agent.replay(32)

if __name__ == "__main__":
    main()
