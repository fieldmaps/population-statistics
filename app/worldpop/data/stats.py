from psycopg import connect
from psycopg.sql import SQL, Identifier

from .utils import DATABASE, logging

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS {table_out};
    CREATE TABLE {table_out} AS
    WITH x AS (
        SELECT
            a.adm4_id, a.adm3_id, a.adm2_id, a.adm1_id, a.adm0_id, a.iso_3,
            ST_Clip(b.rast, a.geom) AS rast
        FROM adm4_polygons AS a
        LEFT JOIN {table_in} as b
        ON ST_Intersects(a.geom, b.rast)
    )
    SELECT
        adm4_id, adm3_id, adm2_id, adm1_id, adm0_id, iso_3,
        (ST_SummaryStatsAgg(rast, 1, true)).count AS count,
        (ST_SummaryStatsAgg(rast, 1, true)).sum AS {col}
    FROM x
    GROUP BY adm4_id, adm3_id, adm2_id, adm1_id, adm0_id, iso_3
    ORDER BY adm4_id;
"""


def main():
    conn = connect(f"dbname={DATABASE}", autocommit=True)
    conn.execute(
        SQL(query_1).format(
            table_in=Identifier("worldpop_pop"),
            col=Identifier("t"),
            table_out=Identifier("worldpop_pop_out"),
        )
    )
    conn.close()
    logger.info("finished")
