import logging
from pathlib import Path

DATA_URL = "https://data.fieldmaps.io"
cwd = Path(__file__).parent
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

dests = ["humanitarian"]
world_views = ["intl"]
pops = ["un-wpp", "meta-fb", "worldpop"]


def get_land_date():
    with open(cwd / "../../../adm0-generator/data/date.txt") as f:
        return f.readline()


land_date = get_land_date()
