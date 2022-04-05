from os import getenv

update_rate = int(getenv('UPDATE_RATE', 30))
icao_codes = getenv('ICAO_CODES').split(',') or ['EHAM', 'LFPO', 'LFBO']
avwx_token = getenv('AVWX_TOKEN')
