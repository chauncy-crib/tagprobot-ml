from unittest import TestCase
from hypothesis import given
import hypothesis.strategies as st


from state.ball import Ball, Team

# some random position between -1M and 1M
ball_position = st.integers(min_value=-1000000, max_value=1000000)

# hypothesis strategy for generating random balls
st_ball = st.builds(Ball, x=ball_position,
                    y=ball_position, team=st.sampled_from(Team))


class TestBall(TestCase):
    @given(st_ball)
    def test_draw_is_offset(self, ball):
        rect = ball.get_shape()[2]
        self.assertEqual(rect.left, ball.x - ball.radius)
        self.assertEqual(rect.top, ball.y - ball.radius)
