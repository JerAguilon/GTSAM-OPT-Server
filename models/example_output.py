def X(i):
    """Create key for pose i."""
    return int(gtsam.symbol(ord('x'), i))


def L(j):
    """Create key for landmark j."""
    return int(gtsam.symbol(ord('l'), j))


class PlanarSlamOutput(object):
    def __init__(self, result, covariance):
        self.result = result
        self.covariance = dict(
            ((k, v.tolist()) for k, v in covariance.iteritems())
        )

    def serialize(self):
        return {
            'result': str(self.result),
            'covariance': self.covariance
        }
