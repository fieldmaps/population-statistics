import logging
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

DATA_URL = "https://population.un.org/wpp/Download/Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_TotalPopulationBySex.csv.gz"
DATA_FILE = cwd / "../../../inputs/un_wpp/WPP2024_TotalPopulationBySex.csv"
ADM0_URL = "https://data.fieldmaps.io/adm0/osm/intl/adm0_polygons.xlsx"
