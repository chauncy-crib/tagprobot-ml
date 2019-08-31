import pygame
from typing import List

from world_state.ball import Ball
from world_state.flag import Flag
from world_state.worldstate import WorldState


def main():

    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    done = False

    ego_ball = Ball(0, 0, (0, 128, 255))
    flag = Flag(100, 100)

    world_state = WorldState([], [], ego_ball, flag, screen)

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #     is_blue = not is_blue

        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_UP]: y -= 3
        # if pressed[pygame.K_DOWN]: y += 3
        # if pressed[pygame.K_LEFT]: x -= 3
        # if pressed[pygame.K_RIGHT]: x += 3

        screen.fill((0, 0, 0))
        world_state.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
