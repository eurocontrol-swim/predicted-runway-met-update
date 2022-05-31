"""
Copyright 2022 EUROCONTROL
==========================================

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions
   and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of
conditions
   and the following disclaimer in the documentation and/or other materials provided with the
   distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to
endorse
   or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF
THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

==========================================

Editorial note: this license is an instance of the BSD license template as provided by the Open
Source Initiative: http://opensource.org/licenses/BSD-3-Clause

Details on EUROCONTROL: http://www.eurocontrol.int
"""

__author__ = "EUROCONTROL (SWIM)"

import logging.config

from apscheduler.schedulers.blocking import BlockingScheduler
from mongoengine import connect

from met_update import config as cfg
from met_update.service.updater import update_taf, update_metar

_logger = logging.getLogger(__name__)


def configure_logging():
    logging.config.dictConfig(cfg.LOGGING)


def configure_mongo():
    connect(**cfg.MONGO)


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
    configure_mongo()


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
