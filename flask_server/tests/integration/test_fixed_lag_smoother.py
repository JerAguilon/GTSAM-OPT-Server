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
            ('time', float(time)/100),
            ('odometryMeasurements', odometry_measurements),
            ('odometryNoise', odometry_noise),
            ('currentPose', [float(time * 2) / 100, 0, 0])
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
        {u'estimate': {u'y': 0.0078020171132018225, u'x': 0.4979168193861158, u'theta': 0.014999997922399554}, u'key': 25},
        {u'estimate': {u'y': 0.02301925031902335, u'x': 0.9954740029957757, u'theta': 0.029999999999997987}, u'key': 50},
        {u'estimate': {u'y': 0.04572473759644762, u'x': 1.4928400548497507, u'theta': 0.04499999999999025}, u'key': 75},
        {u'estimate': {u'y': 0.07588788123063221, u'x': 1.9898095745143463, u'theta': 0.05999999999996915}, u'key': 100},
        {u'estimate': {u'y': 0.11350189469107361, u'x': 2.4862707429157163, u'theta': 0.07499999999992327}, u'key': 125},
        {u'estimate': {u'y': 0.15855831508856758, u'x': 2.9821118553519637, u'theta': 0.08999999999983689}, u'key': 150},
        {u'estimate': {u'y': 0.21104700505401455, u'x': 3.4772213466336948, u'theta': 0.10499999999968901}, u'key': 175},
        {u'estimate': {u'y': 0.270956155019242, u'x': 3.971487816186471, u'theta': 0.11999999999945327}, u'key': 200},
        {u'estimate': {u'y': 0.33827228587404296, u'x': 4.464800053116308, u'theta': 0.13499999999909668}, u'key': 225},
        {u'estimate': {u'y': 0.41298025199914384, u'x': 4.957047061232569, u'theta': 0.14999999999858046}, u'key': 250},
        {u'estimate': {u'y': 0.49506324467313556, u'x': 5.448118084022714, u'theta': 0.1649999999978575}, u'key': 275},
        {u'estimate': {u'y': 0.5845027958547945, u'x': 5.937902629573156, u'theta': 0.17999999999687336}, u'key': 300},
    ]

    for i, update in enumerate(updates):
        response = client.post(
            '/fixedLagSmoother/observations',
            json=update
        )
        assert response.get_json() == expected[i]
