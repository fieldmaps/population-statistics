import subprocess

from .utils import YEAR, cwd, logging

logger = logging.getLogger(__name__)
data = cwd / "../../../inputs/worldpop"


def main():
    if (data / "unconstrained.vrt").is_file():
        subprocess.run(
            [
                "gdal_translate",
                *["--config", "GDAL_NUM_THREADS", "ALL_CPUS"],
                *["-co", "BIGTIFF=YES"],
                *["-co", "TILED=YES"],
                *["-co", "COMPRESS=ZSTD"],
                *["-co", "PREDICTOR=2"],
                (data / "unconstrained.vrt"),
                (data / f"ppp_{YEAR}_unconstrained.tif"),
            ]
        )
    logger.info("finished")
