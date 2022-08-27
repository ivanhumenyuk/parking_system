from flask_smorest import Blueprint, abort

from app.api.crawlers.schemas import (
    ChangeParkingRefreshPeriodArgSchema,
    ChangeParkingRefreshPeriodResponseSchema,
)
from app.config import HARDCODED_PARKING_ID
from app.models import Parking
from app.types.exceptions import ParkingGettingError
from app.utils.uni_responses import invalid_id_response

blp = Blueprint(
    "crawlers",
    "crawlers",
    url_prefix="/api/crawlers",
    description="Working with crawlers",
)


@blp.route(
    f"/<int:parking_id>",
    methods=["PUT"],
    strict_slashes=False,
)
@blp.arguments(ChangeParkingRefreshPeriodArgSchema, location="json", as_kwargs=True)
@blp.response(200, ChangeParkingRefreshPeriodResponseSchema)
@blp.doc(description="Updating parking refresh period")
def update_refresh_period(parking_id: int, refresh_period: int):
    try:
        parking = Parking.change_refresh_period(
            parking_id=parking_id, refresh_period=refresh_period
        )
        return (
            parking if parking else invalid_id_response(cls="Parking", _id=parking_id)
        )
    except ParkingGettingError as err:
        return abort(400, errors=[str(err)])
