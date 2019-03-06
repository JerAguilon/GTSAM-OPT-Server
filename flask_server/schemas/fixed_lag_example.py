from marshmallow import Schema, fields, validate


class PostFixedLagSmootherRequestsSchema(Schema):
    lag = fields.Float(
        required=True
    )
    prior_mean = fields.List(
        fields.Float,
        validate=validate.Length(equal=3),
        required=True,
        load_from='priorMean',
    )
    prior_noise = fields.List(
        fields.Float,
        validate=validate.Length(equal=3),
        required=True,
        load_from='priorNoise',
    )

    class Meta:
        strict = True

class PostFixedLagSmootherObservationsSchema(Schema):
    time = fields.Float(required=True)
    previous_key = fields.Integer(
        load_from="previousKey",
        required=True,
    )
    current_key = fields.Integer(
        load_from="currentKey",
        required=True,
    )
    current_pose = fields.List(
        fields.Float,
        validate=validate.Length(equal=3),
        load_from="currentPose",
        required=True,
    )
    odometry_measurements = fields.List(
        fields.List(
            fields.Float,
            validate=validate.Length(equal=3),
            required=True,
        ),
        load_from="odometryMeasurements",
        required=True,
    )
    odometry_noise = fields.List(
        fields.List(
            fields.Float,
            validate=validate.Length(equal=3),
            required=True,
        ),
        load_from="odometryNoise",
        required=True,
    )

    class Meta:
        strict = True
