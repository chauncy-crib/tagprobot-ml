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

import time

from input.input import input_choices, Input
from copy import deepcopy

from numpy import ndarray, array
import numpy as np

from model.dqn_agent import DQNAgent
from state.heuristic_scores import naive_ego_to_flag, linear_ego_to_flag
from random import randrange
import random
import math


def random_state(episide) -> State:
    x_flag, y_flag = randrange(500, 700), randrange(500, 700)
    x_flag, y_flag = 600, 600
    angle = random.uniform(0, 2*math.pi)
    dist = 100
    x_ego = x_flag + 100 * math.sin(angle)
    y_ego = y_flag + 100 * math.cos(angle)
    ego_ball = Ball(x=x_ego, y=y_ego, id=uuid4(), team=Team.EGO)
    flag = Flag(x=x_flag, y=y_flag)
    return State([ego_ball], flag)

def reward(state: State, time_elapsed: float) -> float:
    # reward is 100 if we touch the flag, 0 if we are 300 pixels away.
    # negative if we are >300 pixels away
    cost = linear_ego_to_flag(state) / 3
    time_penalty = time_elapsed * 10 # every second, we lost 50 points
    return 100 - cost - time_penalty



def rewardTransition(state: State, t1: float, next_state: State, t2: float) -> float:
    return reward(next_state, t2) - reward(state, t1)

def is_done(state: State) -> bool:
    return linear_ego_to_flag(state) <= 0



def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1000,1000))
    black = (0, 0, 0)
    # our x, y, vx, vy relative to the flag
    input_size = 5
    # we have 9 choices of action to take.
    # 4 cardinal directions, 4 45 degree directions, and do nothing
    action_space = 9

    episodes = 5000
    dt = 100  # milliseconds
    game_length = 1500  # milliseconds

    # initialize gym environment and the agent
    agent = DQNAgent(input_size, action_space)
    td_model = deepcopy(agent.model)
    # Iterate the game
    for e in range(episodes):
        # reset state in the beginning of each game
        state = random_state(e)
        ego = state.get_ego_ball()
        frames = 0
        if (e % 100) == 0: # update the td model every 100 episodes
            print("Current epsilon: {}".format(agent.epsilon))
            td_model = deepcopy(agent.model)
        num_frames = int(game_length / dt)
        for frame_num in range(0, num_frames):
            frames += 1
            action = agent.act(state)
            user_input = Input({ego.id: input_choices[action]})
            next_state = deepcopy(state)
            next_state.handle_input(user_input)
            next_state.next_state(dt)
            win = is_done(next_state)
            done = win or frame_num == num_frames - 1
            if done:
                # TODO: should we get this reward even if we lose?
                reward_val = reward(next_state, next_state.time)
            else:
                reward_val = rewardTransition(state, state.time, next_state,
                                      next_state.time)
            agent.remember(state, action, reward_val, next_state, done)
            # make next_state the new current state for the next frame.
            state = next_state
            if e % 30 == 0:
                screen.fill(black)
                state.draw(screen)
                pygame.display.flip()
            if win:
                # print the score and break out of the loop
                print("episode: {}/{}, score: {}"
                      .format(e, episodes, frame_num * dt / 1000))
                break
        # train the agent with the experience of the episode
        agent.replay(min(25, frames), td_model, dt, ego)

    path = "trained_model_{}".format(uuid4().hex)
    print("Saving model to: {}".format(path))
    agent.model.save(path)


if __name__ == "__main__":
    main()
