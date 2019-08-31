from typing import List
from ball import Ball


def main():
    l: List[int] = []
    ball = Ball(1, 2)
    l.append(ball.x)
    print(l)


if __name__ == "__main__":
    main()
