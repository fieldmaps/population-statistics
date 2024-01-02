import shutil

from .utils import cwd, logging

logger = logging.getLogger(__name__)
data = cwd / "../../../inputs/worldpop"


def main():
    (data / "unconstrained.vrt").unlink(missing_ok=True)
    shutil.rmtree(data / "unconstrained", ignore_errors=True)
    logger.info("finished")
