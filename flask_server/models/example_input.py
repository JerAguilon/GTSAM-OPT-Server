from enum import Enum

import gtsam

class SymbolType(Enum):
    POSE = "pose"
    POINT = "point"

class SymbolRequest(object):
    def __init__(self, estimate, type):
        self.type = type
        self.estimate = estimate

    def get_estimate(self):
        if self.type == SymbolType.POSE:
            return gtsam.Pose2(*self.estimate)
        if self.type == SymbolType.POINT:
            return gtsam.Point2(*self.estimate)

class BetweenFactorRequest(object):
    def __init__(self, var1, var2, pose, odometry_noise):
        self.var1 = var1
        self.var2 = var2
        self.pose = pose
        self.odometry_noise = odometry_noise

    def get_factor(self):
        return gtsam.BetweenFactorPose2(
            self.var1,
            self.var2,
            gtsam.Pose2(*self.pose),
            self.odometry_noise,
        )

class BearingFactorRequest(object):
    def __init__(self, var1, var2, bearing, range, measurement_noise):
        self.var1 = var1
        self.var2 = var2
        self.bearing = bearing
        self.range = range
        self.measurement_noise = measurement_noise

    def get_factor(self):
        return gtsam.BearingRangeFactor2D(
            self.var1,
            self.var2,
            gtsam.Rot2.fromDegrees(self.bearing),
            self.range,
            self.measurement_noise,
        )

class SLAMRequest(object):
    def __init__(
        self,
        prior_noise,
        odometry_noise,
        measurement_noise,
        symbols,
        priors,
        between_pose_factors,
        bearing_range_factors,
    ):
        self.prior_noise = prior_noise
        self.odometry_noise = odometry_noise
        self.measurement_noise = measurement_noise,
        self.symbols = symbols
        self.prior = priors
        self.between_pose_factors = between_pose_factors
        self.bearing_range_factors = bearing_range_factors

    @staticmethod
    def from_request(request):
        pass
