from psycopg2 import connect
from psycopg2.sql import SQL, Identifier
from .utils import DATABASE, logging

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS {table_out};
    CREATE TABLE {table_out} AS
    SELECT
        a.*,
        b.f,
        c.m,
        d.t_00_04,
        e.t_15_24,
        f.t_60_plus,
        g.f_15_49
    FROM meta_fb_pop_t_out AS a
    JOIN meta_fb_pop_f_out AS b
    ON a.adm4_id = b.adm4_id
    JOIN meta_fb_pop_m_out AS c
    ON a.adm4_id = c.adm4_id
    JOIN meta_fb_pop_t_00_04_out AS d
    ON a.adm4_id = d.adm4_id
    JOIN meta_fb_pop_t_15_24_out AS e
    ON a.adm4_id = e.adm4_id
    JOIN meta_fb_pop_t_60_plus_out AS f
    ON a.adm4_id = f.adm4_id
    JOIN meta_fb_pop_f_15_49_out AS g
    ON a.adm4_id = g.adm4_id
    ORDER BY adm4_id;
"""


def main():
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(query_1).format(
        table_out=Identifier(f'meta_fb_pop_out'),
    ))
    cur.close()
    con.close()
    logger.info('finished')
