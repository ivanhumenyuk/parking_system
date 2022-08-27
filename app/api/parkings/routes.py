from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint, abort

from app.api.parkings.schemas import ParkingResponseSchema, GetParkingArgsSchema
from app.models import Parking
from app.types.exceptions import ParkingGettingError
from app.utils.uni_responses import success_response, invalid_id_response

blp = Blueprint(
    "parkings",
    "parkings",
    url_prefix="/api/parkings",
    description="Working with parkings",
)


@blp.route("/", methods=["GET"], strict_slashes=False)
@blp.arguments(GetParkingArgsSchema, location="query", as_kwargs=True)
@blp.response(200, ParkingResponseSchema)
@blp.doc(description="Getting products scope")
def get_products(parking_id: int):
    try:
        parking = Parking.get_by_id_or_insert(parking_id=parking_id)
        return (
            parking if parking else invalid_id_response(cls="Parking", _id=parking_id)
        )
    except ParkingGettingError as err:
        return abort(400, errors=[str(err)])
