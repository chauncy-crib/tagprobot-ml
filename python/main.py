import pygame
from uuid import uuid4

from state.ball import Ball, Team
from state.flag import Flag
from state.state import State

from input.input import Keys, Input


def main():

    black = (0, 0, 0)

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
        current_input = Input({ego_ball.id: Keys.from_pygame_pressed(pygame.key.get_pressed())})

        screen.fill(black) # reset the screen before we redraw the state
        clock.tick(60)  # tagpro runs at 60hz
        delta_t_ms: int = clock.get_time()
        world_state.handle_input(current_input)
        world_state.next_state(delta_t_ms)
        world_state.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
