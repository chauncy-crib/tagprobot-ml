import utils.silent_pygame  # noqa: F401
import pygame

from uuid import uuid4

from state.state import State
from state.flag import Flag
from state.ball import Ball, Team

from strategies import myopic

from input.input import Keys, Input


def main():

    black = (0, 0, 0)

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    done = False

    foe_ball = Ball(200, 200, uuid4(), Team.FOE, 50, 50)
    friend_ball = Ball(100, 200, uuid4(), Team.FRIEND, 50, -50)
    ego_ball = Ball(500, 500, uuid4(), Team.EGO, 50, 50)
    flag = Flag(100, 100)

    world_state = State([foe_ball] + [friend_ball] + [ego_ball], flag)

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(black)  # reset the screen before we redraw the state
        clock.tick(60)  # tagpro runs at 60hz
        delta_t_ms: int = clock.get_time()

        pygame_pressed = pygame.key.get_pressed()
        if pygame_pressed[pygame.K_k]:
            ego_ball.handle_pop()
        elif pygame_pressed[pygame.K_r]:
            ego_ball.is_popped = False
        elif pygame_pressed[pygame.K_SPACE]:
            # Of all sensible keypress combinations, choose the one with the lowest score in dt.
            best_keypresses = myopic.best_keypresses(world_state, delta_t_ms)
            current_input = Input({ego_ball.id: best_keypresses})
        else:
            current_input = Input({ego_ball.id: Keys.from_pygame_pressed(pygame_pressed)})

        world_state = world_state.handle_input(current_input)
        world_state = world_state.next_state(delta_t_ms)
        world_state.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
