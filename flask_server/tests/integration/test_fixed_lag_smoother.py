def test_fixed_lag_smoother(client):
    initial_request = {
        'lag': 2.0,
        'priorMean': [0, 0, 0],
        'priorNoise': [0.3, 0.3, 0.1],
    }

    odometry_measurements = [
        [0.61, -0.08, 0.02],
        [0.47, 0.03, 0.01],
    ]

    odometry_noise = [
        [0.1, 0.1, 0.05],
        [0.05, 0.05, 0.05],
    ]


    updates = [
        dict((
            ('previousKey', time - 25),
            ('currentKey', time),
            ('time', time/1000),
            ('odometryMeasurements', odometry_measurements),
            ('odometryNoise', odometry_noise)
        ))
        for time in range(25, 501, 25) # ranges from [0.25, 5.00]
    ]

    print(initial_request)
    print(updates)
    return
