import utils.silent_pygame  # noqa: F401
import pygame

import copy
from uuid import uuid4

from state.state import State
from state.flag import Flag
from state.ball import Ball, Team

from input.input import Keys, Input

import state.heuristic_scores as score


def main():

    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    done = False

    foe_ball = Ball(200, 200, uuid4(), Team.FOE, 50, 50)
    friend_ball = Ball(100, 200, uuid4(), Team.FRIEND, 50, -50)
    ego_ball = Ball(100, 150, uuid4(), Team.EGO, 50, 50)
    flag = Flag(100, 100)

    world_state = State([foe_ball] + [friend_ball] + [ego_ball], flag)

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))
        clock.tick(60)  # tagpro runs at 60hz
        delta_t_ms: int = clock.get_time()

        pygame_pressed = pygame.key.get_pressed()
        if pygame_pressed[pygame.K_SPACE]:
            # While space is pressed, we try to random walk to the flag.
            # If randomly generated diagnonal keypresses are worse than doing nothing, do nothing.
            current_input = Input({ego_ball.id: Keys()})
            current_score = score.naive_ego_to_flag(world_state)
            possible_keys = Keys.random_keys()
            future_ball = ego_ball.simulate_input(possible_keys)
            future_ball.update(delta_t_ms)
            possible_world = copy.deepcopy(world_state)
            possible_world.balls[ego_ball.id] = future_ball
            possible_score = score.naive_ego_to_flag(possible_world)
            if possible_score < current_score:
                current_input = Input({ego_ball.id: possible_keys})
        else:
            current_input = Input({ego_ball.id: Keys.from_pygame_pressed(pygame_pressed)})

        world_state.handle_input(current_input)
        world_state.next_state(delta_t_ms)
        world_state.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
