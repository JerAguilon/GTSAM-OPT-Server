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

import gtsam

from models.example_output import PlanarSlamOutput
from models.example_input import DEFAULT_REQUEST


# Create an empty nonlinear factor graph
def run(slam_request=DEFAULT_REQUEST):
    graph = gtsam.NonlinearFactorGraph()

    # Create the keys corresponding to unknown variables in the factor graph
    unknowns = slam_request.symbols

    # Add a prior on pose X1 at the origin. A prior factor consists of a mean and a noise model
    for prior in slam_request.priors:
        graph.add(prior)

    # Add odometry factors between X1,X2 and X2,X3, respectively
    for factor in slam_request.between_pose_factors:
        graph.add(factor)

    for factor in slam_request.bearing_range_factors:
        graph.add(factor)

    # Print graph
    print("Factor Graph:\n{}".format(graph))

    # Create (deliberately inaccurate) initial estimate
    initial_estimate = gtsam.Values()
    for variable, estimate in slam_request.initial_estimates.iteritems():
        initial_estimate.insert(variable, estimate)

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

    for (string, variable) in unknowns.iteritems():
        covariance = marginals.marginalCovariance(variable)
        print("{} covariance:\n{}\n".format(string, covariance))
        covariance_dict[string] = covariance

    return PlanarSlamOutput(
        result=result,
        covariance=covariance_dict,
    )

