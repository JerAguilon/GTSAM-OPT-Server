"""
GTSAM Copyright 2010-2018, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved
Authors: Frank Dellaert, et al. (see THANKS for the full author list)

See LICENSE for the license information

Simple robotics example using odometry measurements and bearing-range (laser) measurements
Author: Alex Cunningham (C++), Kevin Deng & Frank Dellaert (Python)
"""
# pylint: disable=invalid-name, E1101

from __future__ import print_function

import numpy as np

import gtsam

from models.example_output import PlanarSlamOutput


# Create an empty nonlinear factor graph
def run(
    prior_noise=[.3, .3, .1],
    odometry_noise=[.2, .2, .1],
    measurement_noise=[.1, .2],
    symbols = { 'x1', 'x2', 'x3', 'l4', 'l5' },
    priors = { 'x1': [0, 0, 0] },

):
    prior_noise = gtsam.noiseModel_Diagonal.Sigmas(np.array(prior_noise))
    odometry_noise = gtsam.noiseModel_Diagonal.Sigmas(np.array(odometry_noise))
    measurement_noise = gtsam.noiseModel_Diagonal.Sigmas(np.array(measurement_noise))

    graph = gtsam.NonlinearFactorGraph()

    # Create the keys corresponding to unknown variables in the factor graph
    unknowns = {}
    for symbol in symbols:
        assert len(symbol) == 2
        var = gtsam.symbol(ord(symbol[0]), int(symbol[1]))
        unknowns[symbol] = var

    X1 = gtsam.symbol(ord('x'), 1)
    X2 = gtsam.symbol(ord('x'), 2)
    X3 = gtsam.symbol(ord('x'), 3)
    L1 = gtsam.symbol(ord('l'), 4)
    L2 = gtsam.symbol(ord('l'), 5)

    # Add a prior on pose X1 at the origin. A prior factor consists of a mean and a noise model
    for key, value in priors.iteritems():
        graph.add(gtsam.PriorFactorPose2(unknowns[key], gtsam.Pose2(*value), prior_noise))

    # Add odometry factors between X1,X2 and X2,X3, respectively
    graph.add(gtsam.BetweenFactorPose2(
        X1, X2, gtsam.Pose2(2.0, 0.0, 0.0), odometry_noise))
    graph.add(gtsam.BetweenFactorPose2(
        X2, X3, gtsam.Pose2(2.0, 0.0, 0.0), odometry_noise))

    # Add Range-Bearing measurements to two different landmarks L1 and L2
    graph.add(gtsam.BearingRangeFactor2D(
        X1, L1, gtsam.Rot2.fromDegrees(45), np.sqrt(4.0+4.0), measurement_noise))
    graph.add(gtsam.BearingRangeFactor2D(
        X2, L1, gtsam.Rot2.fromDegrees(90), 2.0, measurement_noise))
    graph.add(gtsam.BearingRangeFactor2D(
        X3, L2, gtsam.Rot2.fromDegrees(90), 2.0, measurement_noise))

    # Print graph
    print("Factor Graph:\n{}".format(graph))

    # Create (deliberately inaccurate) initial estimate
    initial_estimate = gtsam.Values()
    initial_estimate.insert(X1, gtsam.Pose2(-0.25, 0.20, 0.15))
    initial_estimate.insert(X2, gtsam.Pose2(2.30, 0.10, -0.20))
    initial_estimate.insert(X3, gtsam.Pose2(4.10, 0.10, 0.10))
    initial_estimate.insert(L1, gtsam.Point2(1.80, 2.10))
    initial_estimate.insert(L2, gtsam.Point2(4.10, 1.80))

    # Print
    print("Initial Estimate:\n{}".format(initial_estimate))

    # Optimize using Levenberg-Marquardt optimization. The optimizer
    # accepts an optional set of configuration parameters, controlling
    # things like convergence criteria, the type of linear system solver
    # to use, and the amount of information displayed during optimization.
    # Here we will use the default set of parameters.  See the
    # documentation for the full set of parameters.
    params = gtsam.LevenbergMarquardtParams()
    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial_estimate, params)
    result = optimizer.optimize()
    print("\nFinal Result:\n{}".format(result))

    # Calculate and print marginal covariances for all variables
    marginals = gtsam.Marginals(graph, result)
    covariance_dict = {}

    for (key, string) in [(X1, "X1"), (X2, "X2"), (X3, "X3"), (L1, "L1"), (L2, "L2")]:
        covariance = marginals.marginalCovariance(key)
        print("{} covariance:\n{}\n".format(string, covariance))
        covariance_dict[string] = covariance

    return PlanarSlamOutput(
        result=result,
        covariance=covariance_dict,
    )

