from unittest import TestCase
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.searchstrategy.strategies import SearchStrategy

from state.ball import Ball, Team, radius


# strategy for generating a random position between -1M and 1M
st_ball_position: SearchStrategy[int] = st.integers(min_value=-1e6, max_value=1e6)

# hypothesis strategy for generating random balls
st_ball: SearchStrategy[Ball] = st.builds(Ball, x=st_ball_position,
                                          y=st_ball_position, team=st.sampled_from(Team))


class TestBall(TestCase):
    @given(st_ball)
    def test_draw_is_offset(self, ball: Ball):
        rect = ball.get_shape()[2]
        self.assertEqual(rect.left, ball.x - radius)
        self.assertEqual(rect.top, ball.y - radius)
