import logging
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'population_statistics'
FILE_NAME = 'gpw_v4_population_count_rev11_2020_30_sec'
