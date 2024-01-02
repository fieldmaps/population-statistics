import subprocess
import xml.etree.ElementTree as ET

from .utils import cwd, data_types, logging

logger = logging.getLogger(__name__)
data = cwd / "../../../inputs/meta_fb"


def download_data(name):
    vrt = data / f"hrsl_{name}/hrsl_{name}-latest.vrt"
    get_vrt(name, vrt)
    tree = ET.parse(vrt)
    files = [x.text for x in tree.iter("SourceFilename")]
    include = [["--include", x] for x in files]
    include = [i for l in include for i in l]
    get_tif(name, include)
    for file in (data / f"hrsl_{name}").rglob("*.tif*"):
        if file.name not in ",".join(files):
            file.unlink()


def get_vrt(name, vrt):
    subprocess.run(
        [
            *["aws", "s3", "cp"],
            f"s3://dataforgood-fb-data/hrsl-cogs/hrsl_{name}/hrsl_{name}-latest.vrt",
            vrt,
        ]
    )


def get_tif(name, include):
    subprocess.run(
        [
            *["aws", "s3", "sync"],
            *["--exclude", "*"],
            *include,
            f"s3://dataforgood-fb-data/hrsl-cogs/hrsl_{name}/",
            data / f"hrsl_{name}",
        ]
    )


def main():
    data.mkdir(parents=True, exist_ok=True)
    vrt_latest = data / "hrsl_general-latest.vrt"
    get_vrt("general", vrt_latest)
    for name in data_types:
        download_data(name)
    logger.info("finished")
