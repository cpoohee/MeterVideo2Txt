import pytest
from src.KalmanFilter import FilterCoord
def test_kalman():
    kf = FilterCoord(x = 0, y = 1000)

    for i in range(0, 1000):
        x = i
        y = 1000 - i
        bar = kf.update_and_predict(x, y)

        assert x == pytest.approx(bar[0], rel=2)
        assert y == pytest.approx(bar[2], rel=2)
