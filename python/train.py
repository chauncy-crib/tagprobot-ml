from random import randrange

from keras import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from uuid import uuid4
import pygame
from time import time

from state.ball import Ball, Team
from state.flag import Flag
from state.state import State

from input.input import input_choices, Input
from copy import deepcopy

from numpy import ndarray, array
import numpy as np

from model.dqn_agent import DQNAgent
from state.heuristic_scores import naive_ego_to_flag, linear_ego_to_flag


def random_state(episide) -> State:
    x_flag, y_flag = 400, 400
    x_ego, y_ego = 600, 500
    # x_flag, y_flag = randrange(300, 700), randrange(300, 700)
    # x_ego, y_ego = randrange(300, 700), randrange(300, 700)
    ego_ball = Ball(x=x_ego, y=y_ego, id=uuid4(), team=Team.EGO)
    flag = Flag(x=x_flag, y=y_flag)
    return State([ego_ball], flag)


def reward(state: State) -> float:
    # reward is 100 if we touch the flag, 0 if we are 300 pixels away.
    # negative if we are >300 pixels away
    cost = linear_ego_to_flag(state) / 3
    return 100 - cost


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1000,1000))
    black = (0, 0, 0)
    # our x, y, vx, vy relative to the flag
    input_size = 2
    # we have 9 choices of action to take.
    # 4 cardinal directions, 4 45 degree directions, and do nothing
    action_space = 9

    episodes = 5000
    dt = 17  # milliseconds
    game_length = 10000  # 10 seconds in millis

    # initialize gym environment and the agent
    agent = DQNAgent(input_size, action_space)
    # Iterate the game
    for e in range(episodes):
        start = time()
        # reset state in the beginning of each game
        state = random_state(e)
        ego = state.get_ego_ball()
        # time_t represents each frame of the game
        # Our goal is to keep the pole upright as long as possible until score of 500
        # the more time_t the more score
        copy_time = 0
        for frame_num in range(0, int(game_length / dt)):
            if e % 10 == 0:
                screen.fill(black)
                state.draw(screen)
                pygame.display.flip()
            action = agent.act(state)
            user_input = Input({ego.id: input_choices[action]})
            copy_start = time()
            next_state = deepcopy(state)
            copy_time += time()-copy_start
            next_state.handle_input(user_input)
            next_state.next_state(dt)
            curr_reward = reward(state)
            next_reward = reward(next_state)
            reward_val = next_reward - curr_reward
            done = next_reward == 100
            if done:
                reward_val = 100
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
        replay_start = time()
        agent.replay(32)
        replay_time = time() - replay_start
        total_time = time()-start
        # print("% time spent copying: {}".format(copy_time/total_time))
        # print("% time spent replaying: {}".format(replay_time/total_time))


if __name__ == "__main__":
    main()
