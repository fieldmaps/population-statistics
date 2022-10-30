from psycopg import connect
from psycopg.sql import SQL
from processing.boundaries.data.utils import logging, DATABASE

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS adm4_polygons_area;
    CREATE TABLE adm4_polygons_area AS
    SELECT
        adm4_id, adm3_id, adm2_id, adm1_id, adm0_id, iso_3,
        ST_Area(ST_Transform(geom, 6933)) as area
    FROM adm4_polygons;
"""


def main():
    conn = connect(f'dbname={DATABASE}', autocommit=True)
    conn.execute(SQL(query_1))
    conn.close()
    logger.info('finished')
