import pandas as pd

from .utils import DATABASE, cwd, logging

logger = logging.getLogger(__name__)
outputs = cwd / "../../../data"
con = f"postgresql:///{DATABASE}"


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table("meta_fb_pop_out", con)
    df.to_parquet(outputs / "meta_fb.parquet", index=False)
    df.to_csv(
        outputs / "meta_fb.csv.zip",
        index=False,
        float_format="%.0f",
        encoding="utf-8-sig",
    )
    logger.info("finished")
