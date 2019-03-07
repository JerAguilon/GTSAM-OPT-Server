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
            ('odometryNoise', odometry_noise),
            ('currentPose', [float(time * 2) / 1000, 0, 0])
        ))
        for time in range(25, 301, 25) # ranges from [0.25, 3.00]
    ]

    response = client.post(
        '/fixedLagSmoother/requests',
        json=initial_request
    )

    assert response.get_json() == {
        'key': 0
    }

    expected = [
        {u'estimate': {u'y': 0.007776576516727759, u'x': 0.4978233271916955, u'theta': 0.01499999999999999}, u'key': 25},
        {u'estimate': {u'y': 0.02301946898465096, u'x': 0.99547400419693, u'theta': 0.030000000000000183}, u'key': 50},
        {u'estimate': {u'y': 0.045725247818366024, u'x': 1.4928400614087929, u'theta': 0.04500000000000198}, u'key': 75},
        {u'estimate': {u'y': 0.07588880431714243, u'x': 1.9898095932586928, u'theta': 0.06000000000000861}, u'key': 100},
        {u'estimate': {u'y': 0.11350335181391077, u'x': 2.4862707833946924, u'theta': 0.07500000000002599}, u'key': 125},
        {u'estimate': {u'y': 0.15856042720157484, u'x': 2.982111929839782, u'theta': 0.09000000000006314}, u'key': 150},
        {u'estimate': {u'y': 0.21104989283631692, u'x': 3.4772214701244177, u'theta': 0.10500000000013307}, u'key': 175},
        {u'estimate': {u'y': 0.27095993881746233, u'x': 3.971488006387691, u'theta': 0.12000000000025371}, u'key': 200},
        {u'estimate': {u'y': 0.3382770856433916, u'x': 4.46480033044146, u'theta': 0.13500000000044726}, u'key': 225},
        {u'estimate': {u'y': 0.4129861872429267, u'x': 4.957047448791828, u'theta': 0.15000000000074293}, u'key': 250},
        {u'estimate': {u'y': 0.4950704343814752, u'x': 5.448118607612305, u'theta': 0.16500000000117562}, u'key': 275},
        {u'estimate': {u'y': 0.5845113584412137, u'x': 5.937903317663095, u'theta': 0.18000000000178742}, u'key': 300},
    ]

    for i, update in enumerate(updates):
        response = client.post(
            '/fixedLagSmoother/observations',
            json=update
        )
        assert response.get_json() == expected[i]
