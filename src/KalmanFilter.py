import numpy as np
from scipy.linalg import block_diag
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter

class FilterCoord:
    def __init__(self, x, y, dt=0.0333, Q_std=0.04, var=5.0):
        """
        :param x: x position
        :param y: y position
        :param dt: delta time
        :param var: sensor variance
        """
        self.tracker = KalmanFilter(dim_x=4, dim_z=2)
        self.dt = dt
        # state transition function F
        self.tracker.F = np.array([[1, dt, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, dt],
                                   [0, 0, 0, 1]])

        # Process Noise Matrix Q
        q = Q_discrete_white_noise(dim=2, dt=dt, var=Q_std**2)
        self.tracker.Q = block_diag(q, q)

        # Measurement Function H
        self.tracker.H = np.array([[1, 0, 0, 0],
                                   [0, 0, 1, 0]])
        # Measurement Noise Matrix R
        self.tracker.R = np.array([[var, 0],
                                   [0, var]])
        # Initial Conditions x
        self.tracker.x = np.array([[x, 0, y, 0]]).T

        # Covariance Mat P
        self.tracker.P = np.eye(4) * 500.

    def update_and_predict(self, x, y):
        self.tracker.predict()
        z = np.array([[x, y]]).T
        self.tracker.update(z)
        return self.tracker.x