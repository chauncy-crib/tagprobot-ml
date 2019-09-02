from collections import deque
from keras import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from state.state import State
import random
import numpy as np


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
        ego.vy
    ]])  # want this to be shaped (1, 4) so we have two layers of lists


# copy paste from https://keon.io/deep-q-learning/
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.01    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: State) -> int:
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(model_input(state))
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            # print(reward)
            target = reward
            if not done:
                pred = np.amax(self.model.predict(model_input(next_state))[0])
                # print(pred)
                target = reward + self.gamma * pred
            target_f = self.model.predict(model_input(state))
            # print("target: {}".format(target))
            # print("target_f: {}".format(target_f))
            target_f[0][action] = target
            self.model.fit(model_input(state), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
