
from pathlib import Path
from typing import Dict
from json import dump
from datetime import datetime, timezone
import logging

from met_update.config import avwx_token
from met_update.config.file_dir import taf_dir, metar_dir
from met_update.api.met.avwx import get_taf, get_metar

logging.basicConfig(format='[%(asctime)s] - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



def _write_json(json: Dict, path: Path) -> None:
    parent_dir = path.parent
    if not parent_dir.exists():
        parent_dir.mkdir(exist_ok=True)
    with path.open('w', encoding="utf-8") as o:
        dump(json, o)
    logger.info(f"Wrote file {path}")
    return


def update_taf(airport: str):
    taf = get_taf(airport, token=avwx_token)
    filename = f"{int(datetime.now(tz=timezone.utc).timestamp())}_taf.json"
    _write_json(taf, taf_dir.joinpath(airport.upper()).joinpath(filename))
    return


def update_metar(airport: str):
    metar = get_metar(airport, token=avwx_token)
    filename = f"{int(datetime.now(tz=timezone.utc).timestamp())}_metar.json"
    _write_json(metar, metar_dir.joinpath(airport.upper()).joinpath(filename))
    return

