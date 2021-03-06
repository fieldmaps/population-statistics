from psycopg2 import connect
from psycopg2.sql import SQL, Identifier
from .utils import DATABASE, logging, data_types, run_process

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
        (ST_SummaryStatsAgg(rast, 1, true)).count::INTEGER AS count,
        (ST_SummaryStatsAgg(rast, 1, true)).sum::INTEGER AS {col}
    FROM x
    GROUP BY adm4_id, adm3_id, adm2_id, adm1_id, adm0_id, iso_3
    ORDER BY adm4_id;
"""


def data_stats(name):
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(query_1).format(
        table_in=Identifier(f'meta_fb_pop_{data_types[name]}'),
        col=Identifier(data_types[name]),
        table_out=Identifier(f'meta_fb_pop_{data_types[name]}_out'),
    ))
    cur.close()
    con.close()
    logger.info(name)


def main():
    run_process(data_stats)
