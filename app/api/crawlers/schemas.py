from flask_marshmallow import Schema
from marshmallow import fields as f, validates_schema, ValidationError, validates

from app.api.parkings.schemas import ParkingResponseSchema


class ChangeParkingRefreshPeriodArgSchema(Schema):
    refresh_period = f.Integer(
        allow_none=False, required=True, validate=lambda x: x in range(1, 11)
    )


class ChangeParkingRefreshPeriodResponseSchema(ParkingResponseSchema):
    class Meta:
        fields = ("id", "refresh_period", "updated_at", "created_at")
