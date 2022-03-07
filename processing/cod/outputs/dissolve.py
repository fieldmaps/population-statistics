from psycopg2.sql import SQL, Identifier, Literal
from .utils import logging, get_ids, get_ps_ids

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS adm4_polygons_pop;
    CREATE TABLE adm4_polygons_pop AS
    SELECT
        a.*,
        b.ps_lvl
    FROM adm4_polygons AS a
    LEFT JOIN adm0_population AS b
    ON a.iso_3 = b.iso_3;
"""
query_2 = """
    DROP TABLE IF EXISTS {table_out};
    CREATE TABLE {table_out} AS
    SELECT
        {ids},
        ST_Multi(
            ST_Union(geom)
        )::GEOMETRY(MultiPolygon, 4326) AS geom
    FROM {table_in}
    WHERE ps_lvl = {lvl}
    GROUP BY {ids};
"""
query_3 = """
    DROP TABLE IF EXISTS adm0_polygons_pop_01;
    CREATE TABLE adm0_polygons_pop_01 AS
    SELECT
        {ids},
        geom
    FROM adm4_polygons_pop
    WHERE ps_lvl = 0 OR ps_lvl IS NULL;
"""
query_4 = """
    DROP TABLE IF EXISTS {table_out};
    CREATE TABLE {table_out} AS
    SELECT
        a.*,
        {ids}
    FROM {table_in1} AS a
    LEFT JOIN {table_in2} AS b
    ON {a_adm_src} = {b_adm_src};
"""
query_5 = """
    ALTER TABLE {table_out} ADD COLUMN IF NOT EXISTS {id} VARCHAR;
"""
query_6 = """
    UPDATE {table_out}
    SET
        adm4_id = COALESCE(adm4_id, adm3_id, adm2_id, adm1_id, adm0_id),
        adm3_id = COALESCE(adm3_id, adm2_id, adm1_id, adm0_id),
        adm2_id = COALESCE(adm2_id, adm1_id, adm0_id),
        adm1_id = COALESCE(adm1_id, adm0_id);
"""


def main(cur):
    cur.execute(SQL(query_1))
    for l in range(4, 0, -1):
        cur.execute(SQL(query_2).format(
            table_in=Identifier(f'adm4_polygons_pop'),
            ids=SQL(',').join(map(Identifier, get_ids(l))),
            lvl=Literal(l),
            table_out=Identifier(f'adm{l}_polygons_pop_01'),
        ))
    cur.execute(SQL(query_3).format(
        ids=SQL(',').join(map(Identifier, get_ids(4))),
    ))
    for l in range(4, -1, -1):
        cur.execute(SQL(query_4).format(
            table_in1=Identifier(f'adm{l}_polygons_pop_01'),
            table_in2=Identifier(f'adm4_population'),
            ids=SQL(',').join(map(lambda x: Identifier('b', x), get_ps_ids())),
            a_adm_src=Identifier('a', f'adm{l}_src'),
            b_adm_src=Identifier('b', f'adm{l}_src'),
            table_out=Identifier(f'adm{l}_polygons_pop_02'),
        ))
        for col in get_ids(4, attrs=False):
            cur.execute(SQL(query_5).format(
                table_out=Identifier(f'adm{l}_polygons_pop_02'),
                id=Identifier(col),
            ))
        cur.execute(SQL(query_6).format(
            table_out=Identifier(f'adm{l}_polygons_pop_02'),
        ))
    logger.info('finished')
