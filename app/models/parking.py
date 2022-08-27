from typing import Optional

import requests

from sqlalchemy.event import listens_for
from sqlalchemy.exc import IntegrityError

from app import db
from app.config import (
    PARKING_EXTERNAL_API_ENDPOINT,
    DEFAULT_REFRESH_PERIOD,
)
from app.types.db import FullTimestampsMixin, MarketQueryWithSoftDelete
from app.types.exceptions import (
    ParkingGettingError,
)


class Parking(FullTimestampsMixin, db.Model):
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    total_places = db.Column(db.Integer, nullable=False)
    taken_places = db.Column(db.Integer, nullable=False)
    refresh_period = db.Column(
        db.Integer, nullable=False, default=DEFAULT_REFRESH_PERIOD
    )

    @classmethod
    def get_by_id_or_insert(cls, parking_id: int) -> Optional["Parking"]:
        """
        @param parking_id: 'parking' table primary_key
        @return: an instance of Parking class or None or raises error
        """
        try:
            if not (parking := cls.query.get(parking_id)):
                res = requests.get(f"{PARKING_EXTERNAL_API_ENDPOINT}{parking_id}")
                parking_data = res.json()
                properties = parking_data.get("properties")
                total_places = properties.get("total_num_of_places")
                taken_places = properties.get("num_of_taken_places")
                if total_places and taken_places:
                    db.session.add(
                        parking := cls(
                            id=parking_id,
                            total_places=total_places,
                            taken_places=taken_places,
                        )
                    )
                    db.session.commit()
                    print(parking)
            return parking
        except (TypeError, ValueError, IntegrityError) as err:
            raise ParkingGettingError(err)

    @classmethod
    def change_refresh_period(
        cls, parking_id: int, refresh_period: int
    ) -> Optional["Parking"]:
        """

        @param parking_id: 'parking' table primary_key
        @param refresh_period: time in mins befor next request
        to third party parking API
        @return: an instance of Parking class or None or raises error
        """
        try:

            if not (parking := Parking.query.get(parking_id)):
                raise ParkingGettingError(f"Parking {parking_id} doesn't exists")
            parking.refresh_period = refresh_period
            db.session.commit()
            return parking
        except (TypeError, ValueError, IntegrityError) as err:
            raise ParkingGettingError(err)


@listens_for(Parking, "before_update")
def receive_before_update(mapper, connection, target) -> None:
    """Before update listener of Parking model
    and corresponding table"""
    from app.tasks import update_parking_data

    parking = Parking.query.get(target.id)
    if target.refresh_period != parking.refresh_period:
        update_parking_data(parking_id=target.id, refresh_period=target.refresh_period)


@listens_for(Parking, "after_insert")
def receive_after_insert(mapper, connection, target) -> None:
    """On refresh listener of Shop model instances
    for is_default field"""
    from app.tasks import update_parking_data

    if Parking.query.get(target.id):
        update_parking_data(parking_id=target.id, refresh_period=target.refresh_period)
