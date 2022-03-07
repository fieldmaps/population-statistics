import requests
from .utils import DATA_URL, cwd, logging

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/un_wpp'


def main():
    file = data / DATA_URL.split('/')[-1]
    r = requests.get(DATA_URL)
    with open(data / file, 'wb') as f:
        f.write(r.content)
    logger.info('finished')
