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

import logging
from typing import Protocol

from met_update_db import repo

from met_update import config as cfg
from met_update.adapters import avwx

_logger = logging.getLogger(__name__)


class Updater(Protocol):
    def get_avwx_data(self, airport_icao: str) -> dict:
        ...

    def store(self, avwx_data: dict, airport_icao: str) -> None:
        ...


class TafUpdater:
    def get_avwx_data(self, airport_icao: str) -> dict:
        return avwx.get_taf(airport_icao)

    def store(self, avwx_data: dict, airport_icao: str) -> None:
        repo.add_taf(taf_data=avwx_data, airport_icao=airport_icao)


class MetarUpdater:
    def get_avwx_data(self, airport_icao: str) -> dict:
        return avwx.get_metar(airport_icao)

    def store(self, avwx_data: dict, airport_icao: str) -> None:
        repo.add_metar(metar_data=avwx_data, airport_icao=airport_icao)


def update_met(updater: Updater, airport_icao: str) -> None:
    if airport_icao not in cfg.AIRPORT_ICAOS:
        _logger.error(f"{airport_icao} is not supported. "
                      f"Please choose one of {', '.join(cfg.AIRPORT_ICAOS)}")
        return

    try:
        avwx_data = updater.get_avwx_data(airport_icao=airport_icao)
    except Exception as e:
        _logger.error(f"Error while trying to retrieve data from AVWX: {str(e)}")
        avwx_data = None

    if avwx_data is not None:
        updater.store(avwx_data=avwx_data, airport_icao=airport_icao)
        _logger.info(f"Stored AVWX data in DB for airport {airport_icao}")
