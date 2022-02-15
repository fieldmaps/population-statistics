import logging
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'population_statistics'


def get_land_date():
    with open(cwd / '../../../../adm0-generator/data/land/README.txt') as f:
        return f.readlines()[21][25:35]


land_date = get_land_date()
