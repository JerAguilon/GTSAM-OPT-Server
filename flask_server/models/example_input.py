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

    @staticmethod
    def from_request(request):
        prior_noise = request['priorNoise']
        prior_noise = gtsam.noiseModel_Diagonal.Sigmas(
            np.array(prior_noise))

        odometry_noise = request['odometryNoise']
        odometry_noise = gtsam.noiseModel_Diagonal.Sigmas(
            np.array(odometry_noise))

        measurement_noise = request['measurementNoise']
        measurement_noise = gtsam.noiseModel_Diagonal.Sigmas(
            np.array(measurement_noise))

        symbols = request['symbols']

        unknowns = {}
        for symbol in symbols.keys():
            assert len(symbol) == 2
            var = gtsam.symbol(ord(symbol[0]), int(symbol[1]))
            unknowns[symbol] = var

        priors_request = request['priors']
        priors = []
        for key, value in priors_request.iteritems():
            priors.append(
                gtsam.PriorFactorPose2(unknowns[key], gtsam.Pose2(*value), prior_noise)
            )

        between_pose_factors_request = request['betweenPoseFactors']
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


        bearing_range_factors_request = request['bearingRangeFactors']
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
        for key, value in symbols.iteritems():
            variable = unknowns[key]
            if value['type'] == 'pose':
                estimate = gtsam.Pose2(*value['estimate'])
            elif value['type'] == 'point':
                estimate = gtsam.Point2(*value['estimate'])
            else:
                raise Exception("Invalid type")
            initial_estimates[variable] = estimate

        return SLAMRequest(
            unknowns,
            priors,
            between_pose_factors,
            bearing_range_factors,
            initial_estimates
        )

DEFAULT_ARGS_DICT = {
    'priorNoise': [.3, .3, .1],
    'odometryNoise': [.2, .2, .1],
    'measurementNoise': [.1, .2],
    'symbols': {
        'x1': {
            'estimate': [-.25, .20, .15],
            'type': 'pose'
        },
        'x2': {
            'estimate': [2.30, .10, -.20],
            'type': 'pose'
        },
        'x3': {
            'estimate': [4.10, .10, .10],
            'type': 'pose'
        },
        'l4': {
            'estimate': [1.80, 2.10],
            'type': 'point'
        },
        'l5': {
            'estimate': [4.10, 1.80],
            'type': 'point'
        }
    },
    'priors': { 'x1': [0, 0, 0] },
    'betweenPoseFactors': [
        {
            'connections': ['x1', 'x2'],
            'pose': [2, 0, 0]
        },
        {
            'connections': ['x2', 'x3'],
            'pose': [2, 0, 0]
        },
    ],
    'bearingRangeFactors': [
        {
            'connections': ['x1', 'l4'],
            'bearing': 45,
            'range': np.sqrt(4.0 + 4.0),
        },
        {
            'connections': ['x2', 'l4'],
            'bearing': 90,
            'range': 2,
        },
        {
            'connections': ['x3', 'l5'],
            'bearing': 90,
            'range': 2,
        },
    ]
}

DEFAULT_REQUEST = SLAMRequest.from_request(
    DEFAULT_ARGS_DICT
)
