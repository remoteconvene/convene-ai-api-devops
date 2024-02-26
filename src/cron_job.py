import time

import schedule

from src.core.config.settings import settings


def call_vectorization_service():
    print("Executing vectorization...")  # TODO Call the vectorization service


def configure_cron_job():
    schedule.every().day.at(settings.VECTORIZATION_CRON_TRIGGER_TIME).do(
        call_vectorization_service
    )


def cron_job():
    while True:
        schedule.run_pending()
        time.sleep(1)
