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
    symbols = {
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
    priors = { 'x1': [0, 0, 0] },
    between_pose_factors = [
        {
            'connections': ['x1', 'x2'],
            'pose': [2, 0, 0]
        },
        {
            'connections': ['x2', 'x3'],
            'pose': [2, 0, 0]
        },
    ],
    bearing_range_factors = [
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

):
    prior_noise = gtsam.noiseModel_Diagonal.Sigmas(np.array(prior_noise))
    odometry_noise = gtsam.noiseModel_Diagonal.Sigmas(np.array(odometry_noise))
    measurement_noise = gtsam.noiseModel_Diagonal.Sigmas(np.array(measurement_noise))

    graph = gtsam.NonlinearFactorGraph()

    # Create the keys corresponding to unknown variables in the factor graph
    unknowns = {}
    for symbol in symbols.keys():
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
    for factor in between_pose_factors:
        var1 = unknowns[factor['connections'][0]]
        var2 = unknowns[factor['connections'][1]]
        graph.add(gtsam.BetweenFactorPose2(
            var1, var2, gtsam.Pose2(*factor['pose']), odometry_noise))

    for factor in bearing_range_factors:
        var1 = unknowns[factor['connections'][0]]
        var2 = unknowns[factor['connections'][1]]
        bearing = factor['bearing']
        range = factor['range']
        graph.add(gtsam.BearingRangeFactor2D(
            var1, var2, gtsam.Rot2.fromDegrees(bearing), range, measurement_noise))

    # Print graph
    print("Factor Graph:\n{}".format(graph))

    # Create (deliberately inaccurate) initial estimate
    initial_estimate = gtsam.Values()
    for key, value in symbols.iteritems():
        variable = unknowns[key]
        if value['type'] == 'pose':
            pose = gtsam.Pose2(*value['estimate'])
        elif value['type'] == 'point':
            pose = gtsam.Point2(*value['estimate'])
        else:
            raise Exception("Invalid type")
        initial_estimate.insert(variable, pose)

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

