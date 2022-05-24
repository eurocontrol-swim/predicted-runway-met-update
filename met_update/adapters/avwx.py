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

from functools import lru_cache

from opnieuw import retry
from requests import Session, HTTPError

from met_update.config import AVWX_TOKEN

BASE_URL = 'https://avwx.rest'


def _get_metar_url(airport_icao: str) -> str:
    return f"{BASE_URL}/api/metar/{airport_icao}"


def _get_taf_url(airport_icao: str) -> str:
    return f"{BASE_URL}/api/taf/{airport_icao}"


@lru_cache
def _get_session(avwx_token: str) -> Session:
    session = Session()
    session.headers = {'Authorization': f'BEARER {avwx_token}'}

    return session


def get_session() -> Session:

    if not AVWX_TOKEN:
        raise ValueError('AVWX_TOKEN not set')

    return _get_session(AVWX_TOKEN)


def _call_api(url: str) -> dict:
    session = get_session()

    response = session.get(url)

    response.raise_for_status()

    return response.json()


@retry(
    retry_on_exceptions=(ConnectionError, HTTPError),
    max_calls_total=5,
    retry_window_after_first_call_in_seconds=60,
)
def get_taf(airport_icao: str) -> dict:
    return _call_api(url=_get_taf_url(airport_icao))


@retry(
    retry_on_exceptions=(ConnectionError, HTTPError),
    max_calls_total=5,
    retry_window_after_first_call_in_seconds=60,
)
def get_metar(airport_icao: str) -> dict:
    return _call_api(url=_get_metar_url(airport_icao))
