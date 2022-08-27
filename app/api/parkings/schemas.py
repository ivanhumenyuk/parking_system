from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields as f, validates_schema, ValidationError, validates
from marshmallow import post_dump

from app.config import HARDCODED_PARKING_ID


class ParkingFullSchema(SQLAlchemyAutoSchema):
    class Meta:
        from app.models import Parking

        model = Parking
        exclude = ("deleted_at",)

    total_places = f.Integer(allow_none=False, required=True)
    taken_places = f.Integer(allow_none=False, required=True)
    refresh_period = f.Integer(allow_none=False, required=True)


class ParkingResponseSchema(ParkingFullSchema):
    ...


class GetParkingArgsSchema(Schema):
    parking_id = f.Integer(
        allow_none=True, required=False, default=HARDCODED_PARKING_ID
    )
