from requests import get, HTTPError
from opnieuw import retry
from typing import Dict


base_url = 'https://avwx.rest'

def _get_metar(airport: str, token: str) -> Dict:
    resource = f'/api/metar/{airport}'
    metar_response = get(url=base_url + resource, headers={'Authorization': f'BEARER {token}'})
    metar_response.raise_for_status()
    return metar_response.json()


@retry(
    retry_on_exceptions=(ConnectionError, HTTPError),
    max_calls_total=5,
    retry_window_after_first_call_in_seconds=60,
)
def get_metar(airport: str, token: str) -> Dict:
    return _get_metar(airport=airport, token=token)


def _get_taf(airport: str, token: str) -> Dict:
    resource = f'/api/taf/{airport}'
    taf_response = get(url=base_url + resource, headers={'Authorization': f'BEARER {token}'})
    taf_response.raise_for_status()
    return taf_response.json()


@retry(
    retry_on_exceptions=(ConnectionError, HTTPError),
    max_calls_total=5,
    retry_window_after_first_call_in_seconds=60,
)
def get_taf(airport: str, token: str) -> Dict:
    return _get_taf(airport=airport, token=token)



