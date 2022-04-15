from os import getenv

update_rate = int(getenv('UPDATE_RATE', 30))
icao_codes = getenv('ICAO_CODES', 'EHAM,LFPO,LFBO').split(',')
avwx_token = getenv('AVWX_TOKEN')
