"""
GTSAM Copyright 2010-2018, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved
Authors: Frank Dellaert, et al. (see THANKS for the full author list)

See LICENSE for the license information

Demonstration of the fixed-lag smoothers using a planar robot example
and multiple odometry-like sensors
Author: Frank Dellaert (C++), Jeremy Aguilon (Python)
"""

import gtsam
import gtsam_unstable

from models.example_output import FixedLagSmootherOutput


SMOOTHER_BATCH = None


def _timestamp_key_value(key, value):
    """
    Creates a key value pair for a FixedLagSmootherKeyTimeStampMap
    """

    if (type(key) == float):
        key = int(key)
    return gtsam_unstable.FixedLagSmootherKeyTimestampMapValue(
        key, value
    )


def init_smoother(request):
    """
    Runs a batch fixed smoother on an agent with two odometry
    sensors that is simply moving along the x axis in constant
    speed.
    """
    global SMOOTHER_BATCH

    # Define a batch fixed lag smoother, which uses
    # Levenberg-Marquardt to perform the nonlinear optimization
    lag = request.lag
    smoother_batch = gtsam_unstable.BatchFixedLagSmoother(lag)

    new_factors = gtsam.NonlinearFactorGraph()
    new_values = gtsam.Values()
    new_timestamps = gtsam_unstable.FixedLagSmootherKeyTimestampMap()

    prior_mean = request.prior_mean
    prior_noise = request.prior_noise
    X1 = 0
    new_factors.push_back(gtsam.PriorFactorPose2(X1, prior_mean, prior_noise))
    new_values.insert(X1, prior_mean)
    new_timestamps.insert(_timestamp_key_value(X1, 0.0))

    SMOOTHER_BATCH = smoother_batch
    SMOOTHER_BATCH.update(new_factors, new_values, new_timestamps)

    return X1


def record_observation(observation):
    global SMOOTHER_BATCH

    factor_graph = gtsam.NonlinearFactorGraph()
    new_values = gtsam.Values()
    new_timestamps = gtsam_unstable.FixedLagSmootherKeyTimestampMap()

    time = observation.time
    previous_key = observation.previous_key
    current_key = observation.current_key
    current_pose = observation.current_pose

    new_timestamps.insert(_timestamp_key_value(current_key, time))
    new_values.insert(current_key, current_pose)

    # for measurement, noise in zip(
    #         observation.odometry_measurements, observation.odometry_noise):
    #     factor_graph.push_back(gtsam.BetweenFactorPose2(
    #         previous_key, current_key, measurement, noise

    import numpy as np
    odometry_measurement_1 = gtsam.Pose2(0.61, -0.08, 0.02)
    odometry_noise_1 = gtsam.noiseModel_Diagonal.Sigmas(
        np.array([0.1, 0.1, 0.05]))
    factor_graph.push_back(gtsam.BetweenFactorPose2(
        previous_key, current_key, odometry_measurement_1, odometry_noise_1
    ))

    odometry_measurement_2 = gtsam.Pose2(0.47, 0.03, 0.01)
    odometry_noise_2 = gtsam.noiseModel_Diagonal.Sigmas(
        np.array([0.05, 0.05, 0.05]))
    factor_graph.push_back(gtsam.BetweenFactorPose2(
        previous_key, current_key, odometry_measurement_2, odometry_noise_2
    ))

    # Update the smoothers with the new factors
    SMOOTHER_BATCH.update(factor_graph, new_values, new_timestamps)
    pose = SMOOTHER_BATCH.calculateEstimatePose2(current_key)

    output = FixedLagSmootherOutput(current_key, pose)
    return output

