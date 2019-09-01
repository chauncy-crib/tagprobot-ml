
from keras import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from uuid import uuid4

from state.ball import Ball, Team
from state.flag import Flag
from state.state import State


def main() -> None:
    # our x, y, vx, vy relative to the flag
    input_size = 4
    # we have 9 choices of action to take.
    # 4 cardinal directions, 4 45 degree directions, and do nothing
    action_space = 9

    learning_rate = 0.001  # who knows

    ego_ball = Ball(100, 150, uuid4(), Team.EGO, 50, 50)
    flag = Flag(400, 400)
    state = State([ego_ball], flag)

    # cargo cult from: https://keon.io/deep-q-learning/
    # should play with architecture later
    model = Sequential()
    model.add(Dense(24, input_dim=input_size, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(action_space, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=learning_rate))

    print(state)


if __name__ == "__main__":
    main()
