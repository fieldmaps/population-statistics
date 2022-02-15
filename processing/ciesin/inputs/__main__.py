from psycopg2 import connect
from . import inputs, stats, outputs
from .utils import DATABASE, logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    inputs.main()
    stats.main(cur)
    outputs.main()
    cur.close()
    con.close()
