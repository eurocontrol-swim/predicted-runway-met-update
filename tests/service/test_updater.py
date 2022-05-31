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
from unittest import mock

from met_update.service.updater import update_met


def test_update_met__invalid_airport__logs_error_and_returns(caplog):
    caplog.set_level(logging.DEBUG)

    mock_updater = mock.Mock()
    mock_updater.get_avwx_data = mock.Mock()
    mock_updater.store = mock.Mock()

    invalid_airport_icao = 'EBBR'
    update_met(updater=mock_updater, airport_icao=invalid_airport_icao)

    mock_updater.get_avwx_data.assert_not_called()
    mock_updater.store.assert_not_called()

    expected_log_message = 'EBBR is not supported. Please choose one of EHAM, LEMD, LFPO, LOWW'
    assert caplog.messages[0] == expected_log_message


def test_update_met__avwx_raises_exception__data_is_not_stored(caplog):
    caplog.set_level(logging.DEBUG)

    mock_updater = mock.Mock()
    mock_updater.get_avwx_data = mock.Mock(side_effect=Exception('AVWX error'))
    mock_updater.store = mock.Mock()

    update_met(updater=mock_updater, airport_icao='EHAM')

    mock_updater.get_avwx_data.assert_called_once_with(airport_icao='EHAM')
    mock_updater.store.assert_not_called()

    expected_log_message = 'Error while trying to retrieve data from AVWX: AVWX error'
    assert caplog.messages[0] == expected_log_message


def test_update_met__no_errors__data_is_stored__and_logged(caplog):
    caplog.set_level(logging.DEBUG)

    airport_icao = 'EHAM'
    avwx_data = {'data': {}}

    mock_updater = mock.Mock()
    mock_updater.get_avwx_data = mock.Mock(return_value=avwx_data)
    mock_updater.store = mock.Mock()

    update_met(updater=mock_updater, airport_icao='EHAM')

    mock_updater.get_avwx_data.assert_called_once_with(airport_icao=airport_icao)
    mock_updater.store.assert_called_once_with(avwx_data=avwx_data, airport_icao=airport_icao)

    expected_log_message = "Stored AVWX data in DB for airport EHAM"
    assert caplog.messages[0] == expected_log_message
