import copy

from input.input import Keys
from state.state import State
import state.heuristic_scores as score


def best_keypresses(state: State, dt: int) -> Keys:
    keypress_options = [
        Keys(),  # it's important that no action be first in case of uniform cost
        Keys(left_pressed=True),
        Keys(right_pressed=True),
        Keys(up_pressed=True),
        Keys(down_pressed=True),
        Keys(left_pressed=True, up_pressed=True),
        Keys(right_pressed=True, up_pressed=True),
        Keys(left_pressed=True, down_pressed=True),
        Keys(right_pressed=True, down_pressed=True)
    ]

    keypress_scores = [evaluate_keys(state, keypress, dt) for keypress in keypress_options]

    return min(zip(keypress_options, keypress_scores), key=(lambda tup: tup[1]))[0]


def evaluate_keys(state: State, keypresses: Keys, dt: int) -> float:
    ego_ball = state.get_ego_ball()
    future_ball = ego_ball.simulate_input(keypresses)
    future_ball.update(dt)
    possible_world = copy.deepcopy(state)
    possible_world.balls[ego_ball.id] = future_ball
    return score.naive_ego_to_flag(possible_world)
