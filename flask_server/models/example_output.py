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
