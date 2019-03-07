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

import numpy as np

import gtsam
import gtsam_unstable


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


def BatchFixedLagSmootherExample():
    """
    Runs a batch fixed smoother on an agent with two odometry
    sensors that is simply moving along the x axis in constant
    speed.
    """

    # Define a batch fixed lag smoother, which uses
    # Levenberg-Marquardt to perform the nonlinear optimization
    lag = 2.0
    smoother_batch = gtsam_unstable.BatchFixedLagSmoother(lag)

    # Create containers to store the factors and linearization points
    # that will be sent to the smoothers
    new_factors = gtsam.NonlinearFactorGraph()
    new_values = gtsam.Values()
    new_timestamps = gtsam_unstable.FixedLagSmootherKeyTimestampMap()

    # Create  a prior on the first pose, placing it at the origin
    prior_mean = gtsam.Pose2(0, 0, 0)
    prior_noise = gtsam.noiseModel_Diagonal.Sigmas(np.array([0.3, 0.3, 0.1]))
    X1 = 0
    new_factors.push_back(gtsam.PriorFactorPose2(X1, prior_mean, prior_noise))
    new_values.insert(X1, prior_mean)
    new_timestamps.insert(_timestamp_key_value(X1, 0.0))

    global SMOOTHER_BATCH
    SMOOTHER_BATCH = smoother_batch

    # Update the smoothers with the new factors
    SMOOTHER_BATCH.update(new_factors, new_values, new_timestamps)

    new_timestamps.clear()
    new_values.clear()
    new_factors.resize(0)

def cont():
    new_factors = gtsam.NonlinearFactorGraph()
    new_values = gtsam.Values()
    new_timestamps = gtsam_unstable.FixedLagSmootherKeyTimestampMap()

    delta_time = 0.25
    time = 0.25

    # Iterates from 0.25s to 3.0s, adding 0.25s each loop
    # In each iteration, the agent moves at a constant speed
    # and its two odometers measure the change.
    while time <= 3.0:
        previous_key = 1000 * (time - delta_time)
        current_key = 1000 * time

        # assign current key to the current timestamp
        new_timestamps.insert(_timestamp_key_value(current_key, time))

        # Add a guess for this pose to the new values
        # Assume that the robot moves at 2 m/s. Position is time[s] * 2[m/s]
        current_pose = gtsam.Pose2(time * 2, 0, 0)
        new_values.insert(current_key, current_pose)

        # Add odometry factors from two different sources with different error
        # stats
        odometry_measurement_1 = gtsam.Pose2(0.61, -0.08, 0.02)
        odometry_noise_1 = gtsam.noiseModel_Diagonal.Sigmas(
            np.array([0.1, 0.1, 0.05]))
        new_factors.push_back(gtsam.BetweenFactorPose2(
            previous_key, current_key, odometry_measurement_1, odometry_noise_1
        ))

        odometry_measurement_2 = gtsam.Pose2(0.47, 0.03, 0.01)
        odometry_noise_2 = gtsam.noiseModel_Diagonal.Sigmas(
            np.array([0.05, 0.05, 0.05]))
        new_factors.push_back(gtsam.BetweenFactorPose2(
            previous_key, current_key, odometry_measurement_2, odometry_noise_2
        ))

        # Update the smoothers with the new factors
        SMOOTHER_BATCH.update(new_factors, new_values, new_timestamps)

        print("Timestamp = " + str(time) + ", Key = " + str(current_key))
        print(SMOOTHER_BATCH.calculateEstimatePose2(current_key))

        new_timestamps.clear()
        new_values.clear()
        new_factors.resize(0)

        time += delta_time

if __name__ == '__main__':
    BatchFixedLagSmootherExample()
    cont()
