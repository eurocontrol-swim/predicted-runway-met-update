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

import json
import logging
from datetime import datetime
from pathlib import Path

from met_update.adapters.avwx import get_taf, get_metar
from met_update.config import TAF_DIR, METAR_DIR

_logger = logging.getLogger(__name__)


def _write_json_data(json_data: dict, path: Path) -> None:
    with path.open('w', encoding="utf-8") as f:
        json.dump(json_data, f)
    _logger.info(f"Created file {path}")


def _get_current_timestamp() -> int:
    return int(datetime.utcnow().timestamp())


def _get_taf_filepath(airport_icao: str) -> Path:
    filename = f"{_get_current_timestamp()}_taf.json"

    return TAF_DIR.joinpath(airport_icao.upper()).joinpath(filename)


def _get_metar_filepath(airport_icao: str) -> Path:
    filename = f"{_get_current_timestamp()}_metar.json"

    return METAR_DIR.joinpath(airport_icao.upper()).joinpath(filename)


def update_taf(airport_icao: str):
    taf_data = get_taf(airport_icao)

    _write_json_data(json_data=taf_data, path=_get_taf_filepath(airport_icao))


def update_metar(airport_icao: str):
    metar_data = get_metar(airport_icao)

    _write_json_data(json_data=metar_data, path=_get_metar_filepath(airport_icao))
