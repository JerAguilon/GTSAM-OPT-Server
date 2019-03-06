class PlanarSlamOutput(object):
    def __init__(self, result, covariance):
        self.result = result
        self.covariance = dict(
            ((k, v.tolist()) for k, v in covariance.iteritems())
        )

    def serialize(self):
        return {
            'result': self.result,
            'covariance': self.covariance
        }

class FixedLagSmootherOutput(object):
    def __init__(self, key, estimate):
        self.key = key
        self.estimate = estimate

    def serialize(self):
        return {
            'key': self.key,
            'estimate': {
                'x': self.estimate.x(),
                'y': self.estimate.y(),
                'theta': self.estimate.theta(),
            }
        }

