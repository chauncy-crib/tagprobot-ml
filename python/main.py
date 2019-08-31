import pygame
from typing import List

from world_state.ball import Ball, Team
from world_state.flag import Flag
from world_state.worldstate import WorldState


def main():

    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    done = False

    foe_ball = Ball(200, 200, Team.FOE)
    friend_ball = Ball(100, 200, Team.FRIEND)
    ego_ball = Ball(0, 0, Team.EGO)
    flag = Flag(100, 100)

    world_state = WorldState([foe_ball], [friend_ball], ego_ball, flag)

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))
        world_state.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
