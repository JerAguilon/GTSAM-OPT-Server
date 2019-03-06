from enum import Enum

import gtsam
import numpy as np


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


class BearingRangeFactorRequest(object):
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
        symbols,
        priors,
        between_pose_factors,
        bearing_range_factors,
        initial_estimates,
    ):
        self.symbols = symbols
        self.priors = priors
        self.between_pose_factors = between_pose_factors
        self.bearing_range_factors = bearing_range_factors
        self.initial_estimates = initial_estimates

    @classmethod
    def from_request(cls, request):
        prior_noise = request['prior_noise']
        prior_noise = gtsam.noiseModel_Diagonal.Sigmas(
            np.array(prior_noise))

        odometry_noise = request['odometry_noise']
        odometry_noise = gtsam.noiseModel_Diagonal.Sigmas(
            np.array(odometry_noise))

        measurement_noise = request['measurement_noise']
        measurement_noise = gtsam.noiseModel_Diagonal.Sigmas(
            np.array(measurement_noise))

        symbols = request['symbols']

        unknowns = {}
        for symbol in symbols:
            key = symbol['key']
            assert len(key) == 2
            var = gtsam.symbol(ord(key[0]), int(key[1]))
            unknowns[key] = var

        priors_request = request['priors']
        priors = []
        for prior in priors_request:
            key = prior['key']
            prior_val = prior['prior']
            priors.append(
                gtsam.PriorFactorPose2(
                    unknowns[key],
                    gtsam.Pose2(
                        *prior_val),
                    prior_noise))

        between_pose_factors_request = request['between_pose_factors']
        between_pose_factors = []
        for factor in between_pose_factors_request:
            var1 = unknowns[factor['connections'][0]]
            var2 = unknowns[factor['connections'][1]]
            pose = factor['pose']
            factor = BetweenFactorRequest(
                var1=var1,
                var2=var2,
                pose=pose,
                odometry_noise=odometry_noise
            ).get_factor()
            between_pose_factors.append(factor)

        bearing_range_factors_request = request['bearing_range_factors']
        bearing_range_factors = []
        for factor in bearing_range_factors_request:
            var1 = unknowns[factor['connections'][0]]
            var2 = unknowns[factor['connections'][1]]
            bearing = factor['bearing']
            range = factor['range']
            factor = BearingRangeFactorRequest(
                var1=var1,
                var2=var2,
                bearing=bearing,
                range=range,
                measurement_noise=measurement_noise,
            ).get_factor()
            bearing_range_factors.append(factor)

        initial_estimates = {}
        for symbol in symbols:
            variable = unknowns[symbol['key']]
            if symbol['type'] == 'pose':
                estimate = gtsam.Pose2(*symbol['estimate'])
            elif symbol['type'] == 'point':
                estimate = gtsam.Point2(*symbol['estimate'])
            else:
                raise Exception("Invalid type")
            initial_estimates[variable] = estimate

        return cls(
            unknowns,
            priors,
            between_pose_factors,
            bearing_range_factors,
            initial_estimates
        )


class FixedLagSmootherRequest(object):
    def __init__(
        self,
        lag,
        prior_mean,
        prior_noise,
    ):
        self.lag = lag
        self.prior_mean = prior_mean
        self.prior_noise = prior_noise

    @classmethod
    def from_request(cls, request):
        lag = request['lag']
        prior_mean = request['prior_mean']
        prior_mean = gtsam.Pose2(
            *prior_mean
        )

        prior_noise = request['prior_noise']
        prior_noise = gtsam.noiseModel_Diagonal.Sigmas(
            np.array(prior_noise))
        return cls(lag, prior_mean, prior_noise)


class FixedLagSmootherObservation(object):
    def __init__(
        self,
        time,
        previous_key,
        current_key,
        current_pose,
        odometry_measurements,
        odometry_noise
    ):
        if len(odometry_measurements) != len(odometry_noise):
            raise ValueError(
                "Length of odometry measurements and noise must be equal")
        self.time = time
        self.previous_key = previous_key
        self.current_key = current_key
        self.current_pose = current_pose
        self.odometry_measurements = odometry_measurements
        self.odometry_noise = odometry_noise

    @classmethod
    def from_request(cls, request):
        time = request['time']
        previous_key = request['previous_key']
        current_key = request['current_key']

        current_pose = gtsam.Pose2(*request['current_pose'])

        odometry_measurements = []
        odometry_noise = []

        for m in request['odometry_measurements']:
            odometry_measurements.append(gtsam.Pose2(*m))

        for n in request['odometry_noise']:
            odometry_noise.append(
                gtsam.noiseModel_Diagonal.Sigmas(np.array(n))
            )
        return cls(
            time,
            previous_key,
            current_key,
            current_pose,
            odometry_measurements,
            odometry_noise,
        )


DEFAULT_ARGS_DICT = {
    "prior_noise": [.3, .3, .1],
    "odometry_noise": [.2, .2, .1],
    "measurement_noise": [.1, .2],
    "symbols": [
        {
            "key": "x1",
            "estimate": [-.25, .20, .15],
            "type": "pose"
        },
        {
            "key": "x2",
            "estimate": [2.30, .10, -.20],
            "type": "pose"
        },
        {
            "key": "x3",
            "estimate": [4.10, .10, .10],
            "type": "pose"
        },
        {
            "key": "l4",
            "estimate": [1.80, 2.10],
            "type": "point"
        },
        {
            "key": "l5",
            "estimate": [4.10, 1.80],
            "type": "point"
        }
    ],
    "priors": [
        {
            "key": "x1",
            "prior": [0, 0, 0]
        }
    ],
    "between_pose_factors": [
        {
            "connections": ["x1", "x2"],
            "pose": [2, 0, 0]
        },
        {
            "connections": ["x2", "x3"],
            "pose": [2, 0, 0]
        },
    ],
    "bearing_range_factors": [
        {
            "connections": ["x1", "l4"],
            "bearing": 45,
            "range": np.sqrt(4.0 + 4.0),
        },
        {
            "connections": ["x2", "l4"],
            "bearing": 90,
            "range": 2,
        },
        {
            "connections": ["x3", "l5"],
            "bearing": 90,
            "range": 2,
        },
    ]
}

DEFAULT_REQUEST = SLAMRequest.from_request(
    DEFAULT_ARGS_DICT
)
