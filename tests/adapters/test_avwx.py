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

from unittest import mock

import pytest
from requests import Session, HTTPError, Response

from met_update.adapters import avwx
from met_update import config


def test_get_session__avwx_token_not_set__raises_error(monkeypatch):
    monkeypatch.setattr(config, 'AVWX_TOKEN', None)

    with pytest.raises(ValueError) as e:
        avwx.get_session()

    assert str(e.value) == 'AVWX_TOKEN not set'


def test_get_session__no_errors__returns_session_object(monkeypatch):
    monkeypatch.setattr(config, 'AVWX_TOKEN', 'some_token')

    result = avwx.get_session()

    assert isinstance(result, Session)
    assert result.headers == {'Authorization': f'BEARER some_token'}


@mock.patch('met_update.adapters.avwx.get_session')
def test_call_api__response_with_error__raises(mock_get_session):
    mock_response = Response()
    mock_response.status_code = 400

    mock_session = mock.Mock()
    mock_session.get = mock.Mock(return_value=mock_response)

    mock_get_session.return_value = mock_session

    with pytest.raises(HTTPError):
        avwx._call_api('')


@mock.patch('met_update.adapters.avwx.get_session')
def test_call_api__no_errors__returns_response_data(mock_get_session):
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b'{"data": {}}'

    mock_session = mock.Mock()
    mock_session.get = mock.Mock(return_value=mock_response)

    mock_get_session.return_value = mock_session

    result = avwx._call_api('')

    assert result == {'data': {}}


@mock.patch('met_update.adapters.avwx._call_api')
def test_get_taf(mock_call_api):
    airport_icao = 'EHAM'
    avwx.get_taf(airport_icao)

    expected_called_url = f'https://avwx.rest/api/taf/EHAM'

    mock_call_api.assert_called_once_with(url=expected_called_url)


@mock.patch('met_update.adapters.avwx._call_api')
def test_get_metar(mock_call_api):
    airport_icao = 'EHAM'
    avwx.get_metar(airport_icao)

    expected_called_url = f'https://avwx.rest/api/metar/EHAM'

    mock_call_api.assert_called_once_with(url=expected_called_url)
