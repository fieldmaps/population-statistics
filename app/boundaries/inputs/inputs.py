import subprocess

from .utils import DATABASE, cwd, logging

logger = logging.getLogger(__name__)


def main():
    file = (
        cwd
        / "../../../../admin-boundaries/data/edge-matched/humanitarian/intl/adm4_polygons.gpkg"
    )
    subprocess.run(
        [
            "ogr2ogr",
            "-overwrite",
            *["-lco", "FID=fid"],
            *["-lco", "GEOMETRY_NAME=geom"],
            *["-nln", "adm4_polygons"],
            *["-f", "PostgreSQL", f"PG:dbname={DATABASE}"],
            file,
        ]
    )
    logger.info("finished")
