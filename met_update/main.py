from apscheduler.schedulers.blocking import BlockingScheduler
from met_update.api.met.update import update_taf, update_metar
from met_update.config import icao_codes, update_rate
import logging

logging.basicConfig(format='[%(asctime)s] - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': 60 * 5
}

scheduler = BlockingScheduler(job_defaults=job_defaults, timezone='utc')


for airport_icao_code in icao_codes:
    scheduler.add_job(update_metar,
                      trigger='cron',
                      minute=f'*/{update_rate}',
                      kwargs={'airport': airport_icao_code})
    scheduler.add_job(update_taf,
                      trigger='cron',
                      minute=f'*/{update_rate}',
                      kwargs={'airport': airport_icao_code})


if __name__ == '__main__':
    logger.info("Forcing an update")
    for airport_icao_code in icao_codes:
        update_metar(airport_icao_code)
        update_taf(airport_icao_code)

    logger.info(f"Starting scheduler...")
    logger.info(f"Updating every */{update_rate} minutes")
    scheduler.start()
