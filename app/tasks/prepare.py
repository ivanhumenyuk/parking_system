import asyncio
import subprocess
from os import getcwd, popen

from flask import Flask

from app.config import PROCRASTINATE_SCRIPT_PATH
from app.tasks import task_manager

ETSY_IMPORT_WORKER_CMD = (
    f"procrastinate --app=som.tasks.task_manager worker "
    f"--name=etsy-import-worker --concurrency=3 --wait\n"
)


def create_task_manager_script():
    with open(PROCRASTINATE_SCRIPT_PATH, "w+") as script:
        script.write(
            f"#!/bin/bash\n"
            f"cd {getcwd()}\n"
            f"source venv/bin/activate\n"
            f"{ETSY_IMPORT_WORKER_CMD}"
        )
        script.close()


def init_app_tasks(app: Flask):
    create_task_manager_script()
    task_manager.open()

    async def run_tasks():
        from . import task_manager
        with app.app_context():
            # initialize task manager and run initial task(s)
            await task_manager.open_async()
            await task_manager.run_worker_async(
                    wait=True,  # don't stop the worker
                    # delete_jobs="successful",  # delete entries from DB if job succeeded
            )

    def loop_in_thread(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_tasks())

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    import threading
    t = threading.Thread(target=loop_in_thread, args=(loop,), name="FRED", daemon=True)
    t.start()
