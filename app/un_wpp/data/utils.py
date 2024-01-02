import logging
from datetime import date
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

DATA_NAME = "WPP2022_TotalPopulationBySex.csv"
YEAR = date.today().year
