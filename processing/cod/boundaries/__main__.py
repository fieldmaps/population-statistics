from psycopg2 import connect
from . import inputs, dissolve, concat
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    inputs.main()
    # dissolve.main(cur)
    # concat.main(cur)
    cur.close()
    con.close()
