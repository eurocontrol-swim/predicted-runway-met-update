import os
from pathlib import Path

LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG"
        }
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "class": "logging.Formatter"
        }
    },
    "disable_existing_loggers": False,
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console"
        ]
    },
    "loggers": {
        "requests": {
            "level": "INFO"
        },
    }
}


UPDATE_RATE = int(os.getenv('UPDATE_RATE', 30))

AIRPORT_ICAOS = os.getenv('ICAO_CODES', 'EHAM,LEMD,LFPO,LOWW').split(',')

AVWX_TOKEN = os.getenv('AVWX_TOKEN')

METEO_DIR = Path('/data')

METAR_DIR = METEO_DIR.joinpath('metar')

TAF_DIR = METEO_DIR.joinpath('taf')

SCHEDULER_JOB_DEFAULTS = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': 60 * 5
}
