import pandas as pd

from .utils import DATA_NAME, YEAR, cwd, logging

logger = logging.getLogger(__name__)
inputs = cwd / "../../../inputs/un_wpp"
data = cwd / "../../../data"


def main():
    data.mkdir(exist_ok=True, parents=True)
    file = inputs / DATA_NAME
    df = pd.read_csv(file, low_memory=False)
    df = df[df["VarID"] == 2]
    df = df[df["Time"] == YEAR]
    df = df[df["LocID"] < 900]
    df = df[["iso_3", "PopTotal"]]
    df = df.rename(columns={"PopTotal": "t"})
    df["t"] = df["t"].apply(lambda x: x * 1000).astype(int)
    df = df.sort_values("iso_3")
    df.to_parquet(data / "un_wpp.parquet", index=False)
    df.to_csv(data / "un_wpp.csv.zip", index=False, encoding="utf-8-sig")
    logger.info("finished")
