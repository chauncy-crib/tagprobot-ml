from typing import List

class Ball:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

l: List[int] = []
ball = Ball(1, 2)
l.append(ball.x)
