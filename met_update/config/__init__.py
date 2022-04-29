from os import getenv

update_rate = int(getenv('UPDATE_RATE', 30))
icao_codes = getenv('ICAO_CODES', 'EHAM,LEMD,LFPO,LOWW').split(',')
avwx_token = getenv('AVWX_TOKEN')
