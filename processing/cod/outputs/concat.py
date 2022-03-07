from psycopg2.sql import SQL, Identifier
from .utils import logging, get_ids, get_ps_ids

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS adm4_polygons_pop_03;
    CREATE TABLE adm4_polygons_pop_03 AS
    SELECT {ids}, geom FROM adm4_polygons_pop_02
    UNION ALL
    SELECT {ids}, geom FROM adm3_polygons_pop_02
    UNION ALL
    SELECT {ids}, geom FROM adm2_polygons_pop_02
    UNION ALL
    SELECT {ids}, geom FROM adm1_polygons_pop_02
    UNION ALL
    SELECT {ids}, geom FROM adm0_polygons_pop_02
    ORDER BY adm4_id;
"""


def main(cur):
    cur.execute(SQL(query_1).format(
        ids=SQL(',').join(map(Identifier, get_ids(4) + get_ps_ids())),
    ))
    logger.info('finished')
