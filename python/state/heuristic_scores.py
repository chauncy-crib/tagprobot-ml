from uuid import UUID

from utils import math

from state.state import State


# TODO: Decide if all of these should move into State

def naive_ego_to_flag(state: State) -> float:
    ego_ball = state.get_ego_ball()

    combined_radius = ego_ball.radius + state.flag.radius
    combined_radius_sq = combined_radius * combined_radius
    flag_ego_sq_dist = math.sq_dist(ego_ball.x, ego_ball.y, state.flag.x, state.flag.y)
    return max(0, flag_ego_sq_dist - combined_radius_sq)


def naive_ego_to_ball(state: State, target_ball_id: UUID) -> float:
    ego_ball = state.get_ego_ball()
    target_ball = next(ball for ball in state.balls.values() if ball.id == target_ball_id)

    combined_radius = ego_ball.radius + target_ball.radius
    combined_radius_sq = combined_radius * combined_radius
    target_ego_sq_dist = math.sq_dist(ego_ball.x, ego_ball.y, target_ball.x, target_ball.y)
    return max(0, target_ego_sq_dist - combined_radius_sq)
