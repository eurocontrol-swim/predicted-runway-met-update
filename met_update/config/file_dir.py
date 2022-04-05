from pathlib import Path
from os import getenv
import logging


logging.basicConfig(format='[%(asctime)s] - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

meteo_dir = Path('/data')
metar_dir = meteo_dir.joinpath('metar')
if not metar_dir.exists():
    logger.debug("METAR directory does not exist")
    metar_dir.mkdir()
    logger.info(f"Created {metar_dir}")
taf_dir = meteo_dir.joinpath('taf')
if not taf_dir.exists():
    logger.debug("TAF directory does not exist")
    taf_dir.mkdir()
    logger.info(f"Created {taf_dir}")
