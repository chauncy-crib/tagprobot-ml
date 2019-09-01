import pygame
from uuid import uuid4

from state.ball import Ball, Team
from state.flag import Flag
from state.state import State


def main():

    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    done = False

    foe_ball = Ball(200, 200, uuid4(), Team.FOE, 50, 50)
    friend_ball = Ball(100, 200, uuid4(), Team.FRIEND, 50, -50)
    ego_ball = Ball(0, 0, uuid4(), Team.EGO, 50, 50)
    flag = Flag(100, 100)

    world_state = State([foe_ball], [friend_ball], ego_ball, flag)

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))
        clock.tick(10)
        delta_t_ms: int = clock.get_time()
        world_state.next_state(delta_t_ms)
        world_state.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
