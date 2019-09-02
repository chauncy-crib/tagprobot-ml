import copy

from input.input import Keys
from state.state import State
import state.heuristic_scores as score


def best_keypresses(state: State, dt: int) -> Keys:
    keypress_options = {
        Keys(): 0.0,  # it's important that no action be first in case of uniform cost
        Keys(left_pressed=True): 0.0,
        Keys(right_pressed=True): 0.0,
        Keys(up_pressed=True): 0.0,
        Keys(down_pressed=True): 0.0,
        Keys(left_pressed=True, up_pressed=True): 0.0,
        Keys(right_pressed=True, up_pressed=True): 0.0,
        Keys(left_pressed=True, down_pressed=True): 0.0,
        Keys(right_pressed=True, down_pressed=True): 0.0
    }

    for keypress in keypress_options.keys():
        keypress_options[keypress] = evaluate_keys(state, keypress, dt)

    return min(keypress_options.keys(), key=(lambda k: keypress_options[k]))


def evaluate_keys(state: State, keypresses: Keys, dt: int) -> float:
    ego_ball = state.get_ego_ball()
    future_ball = ego_ball.simulate_input(keypresses)
    future_ball.update(dt)  # todo this seems wrong
    possible_world = copy.deepcopy(state)
    possible_world.balls[ego_ball.id] = future_ball
    return score.naive_ego_to_flag(possible_world)
