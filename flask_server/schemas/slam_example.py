from marshmallow import Schema, fields, validate

from models.example_input import SymbolType


def _validate_symbol_type(type):
    try:
        SymbolType(type)
        return True
    except:
        return False

class BetweenPoseFactorSchema(Schema):
    connections = fields.List(
        fields.String,
        validate=validate.Length(equal=2),
        required=True
    )
    pose = fields.List(
        fields.Float,
        validate=validate.Length(equal=3),
        required=True
    )

    class Meta:
        strict=True


class BearingRangeFactorSchema(Schema):
    connections = fields.List(
        fields.String,
        validate=validate.Length(equal=2),
        required=True
    )
    bearing = fields.Float(
        required=True
    )
    range = fields.Float(
        required=True
    )

    class Meta:
        strict=True


class PriorSchema(Schema):
    key = fields.String(
        validate=validate.Length(equal=2),
        required=True
    )
    prior = fields.List(
        fields.Float,
        validate=validate.Length(equal=3),
        required=True,
    )

    class Meta:
        strict=True


class SymbolSchema(Schema):
    key = fields.String(
        validate=validate.Length(equal=2),
        required=True
    )
    estimate = fields.List(
        fields.Float,
        validate=validate.Length(min=2, max=3),
        required=True,
    )
    type = fields.String(
        validate=_validate_symbol_type,
        required=True,
    )

    class Meta:
        strict=True


class PostSlamSchema(Schema):
    prior_noise = fields.List(
        fields.Float,
        load_from='priorNoise',
        validate=validate.Length(equal=3),
        required=True
    )

    odometry_noise = fields.List(
        fields.Float,
        load_from='odometryNoise',
        validate=validate.Length(equal=3),
        required=True
    )

    measurement_noise = fields.List(
        fields.Float,
        load_from='measurementNoise',
        validate=validate.Length(equal=2),
        required=True
    )

    symbols = fields.List(
        fields.Nested(SymbolSchema),
        required=True
    )

    priors = fields.List(
        fields.Nested(PriorSchema),
        required=True
    )

    between_pose_factors = fields.List(
        fields.Nested(BetweenPoseFactorSchema),
        load_from='betweenPoseFactors',
        required=True
    )

    bearing_range_factors = fields.List(
        fields.Nested(BearingRangeFactorSchema),
        load_from='bearingRangeFactors',
        required=True
    )

    class Meta:
        strict=True
