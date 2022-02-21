from psycopg2 import connect
from . import merge, inputs, stats, outputs
from .utils import DATABASE, logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    merge.main()
    inputs.main()
    stats.main(cur)
    outputs.main()
    cur.close()
    con.close()
