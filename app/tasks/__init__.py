import os
from datetime import datetime
from os import listdir
from os.path import isfile, join

import requests
from procrastinate import AiopgConnector, App
from sqlalchemy.exc import IntegrityError

from app import db
from app.config import POSTGRES_DB, POSTGRES_PW, POSTGRES_URL, POSTGRES_USER,  PARKING_EXTERNAL_API_ENDPOINT


DB = f"postgres://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"
task_manager: App = App(connector=AiopgConnector(dsn=DB), import_paths=["scripts"])


def update_parking_data(refresh_period: int, parking_id):
    @task_manager.periodic(cron=f"*/{refresh_period} * * * *")
    @task_manager.task(queue="updating_parking_data_task")
    def updating_parking_data_task():
        """Next year US holidays adding"""
        from app.models import Parking

        try:
            if parking := Parking.query.get(parking_id):
                res = requests.get(
                    f"{PARKING_EXTERNAL_API_ENDPOINT}{parking_id}"
                )
                parking_data = res.json()
                properties = parking_data.get("properties", {})
                parking.total_places = properties.get("total_num_of_places")
                parking.taken_places = properties.get("num_of_taken_places")
                db.session.commit()
        except (TypeError, ValueError, ConnectionError, IntegrityError):
            pass
