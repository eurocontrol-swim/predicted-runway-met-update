import logging.config

from apscheduler.schedulers.blocking import BlockingScheduler

from met_update import config as cfg
from met_update.domain.updater import update_taf, update_metar
from met_update.utils import ensure_dirs

_logger = logging.getLogger(__name__)


def configure_logging():
    logging.config.dictConfig(cfg.LOGGING)


def configure_scheduler() -> BlockingScheduler:
    scheduler = BlockingScheduler(job_defaults=cfg.SCHEDULER_JOB_DEFAULTS, timezone='utc')

    for airport_icao in cfg.AIRPORT_ICAOS:
        scheduler.add_job(update_metar,
                          trigger='cron',
                          minute=f'*/{cfg.UPDATE_RATE}',
                          kwargs={'airport_icao': airport_icao})
        scheduler.add_job(update_taf,
                          trigger='cron',
                          minute=f'*/{cfg.UPDATE_RATE}',
                          kwargs={'airport_icao': airport_icao})

    return scheduler


def _init_setup():
    configure_logging()
    ensure_dirs()


def main():
    _init_setup()

    _logger.info("Forcing an update...")
    for airport_icao in cfg.AIRPORT_ICAOS:
        update_metar(airport_icao)
        update_taf(airport_icao)

    scheduler = configure_scheduler()
    _logger.info(f"Starting scheduler...")
    _logger.info(f"Updating every */{cfg.UPDATE_RATE} minutes")
    scheduler.start()


if __name__ == '__main__':
    main()
