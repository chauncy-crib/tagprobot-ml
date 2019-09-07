from collections import deque
from keras import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from state.state import State
import random
import numpy as np
import math
from input.input import input_choices, Input

from copy import deepcopy

def model_input(state: State) -> np.ndarray:
    """
    :return ndarray: (x, y, vx, vy) of ego ball relative to the flag (ie, flag
                     is at 0, 0)
    """
    ego = state.get_ego_ball()
    flag = state.flag
    return np.array([[
        ego.x - flag.x,
        ego.y - flag.y,
        ego.vx,
        ego.vy,
        state.time
    ]])  # want this to be shaped (1, 4) so we have two layers of lists


# copy paste from https://keon.io/deep-q-learning/
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 1
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(8, input_dim=self.state_size,
                        kernel_initializer='zeros',
                        activation='softmax'))
        model.add(Dense(8,
                        kernel_initializer='zeros',
                        activation='softmax'))
        model.add(Dense(self.action_size, input_dim=self.state_size,
                        kernel_initializer='zeros',
                        activation='linear'))
        # model.add(Dense(24, activation='linear'))
        # model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: State) -> int:
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(model_input(state))
        # print(act_values)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size, td_model, dt, ego):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target_f = self.model.predict(model_input(state))
            if not done:
                for i in range(9):
                    action = input_choices[i]
                    next_state = deepcopy(state)
                    next_state.handle_input(Input({ego.id: action}))
                    next_state.next_state(dt)
                    pred = np.amax(td_model.predict(model_input(next_state))[0])
                    target = reward + self.gamma * pred
                    target_f[0][i] = target
                    self.model.fit(model_input(state), target_f, epochs=1, verbose=0)
            else:
                target = reward
                target_f[0][action] = target
            print("targetF: {}".format(target_f))
            self.model.fit(model_input(state), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            # raise ValueError()
