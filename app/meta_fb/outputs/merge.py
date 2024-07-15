import pandas as pd

from .utils import cwd, get_attrs, logging

logger = logging.getLogger(__name__)
config = cwd / "../../../config"
data = cwd / "../../../data"
outputs = cwd / "../../../outputs/population/humanitarian/intl/meta-fb"

fields = ["t", "f", "m", "t_00_04", "t_15_24", "t_60_plus", "f_15_49"]


def get_ids(l):
    return [f"adm{x}_id" for x in range(l, -1, -1)] + ["iso_3"]


def apply_factor(df):
    df1 = pd.read_parquet(data / "un_wpp.parquet")
    dfx = (
        df.groupby(["iso_3"], dropna=False)
        .sum(numeric_only=True, min_count=1)
        .reset_index()
    )
    dfx = dfx.merge(df1, on="iso_3", how="left")
    dfx["factor"] = dfx["t_y"] / dfx["t_x"]
    dfx["factor"] = dfx["factor"].fillna(1)
    dfx = dfx[["iso_3", "factor"]]
    df = df.merge(dfx, on="iso_3")
    for field in fields:
        df[field] = df[field] * df["factor"]
        df[field] = df[field].round(0)
    df = df.drop(columns=["factor"])
    return df


def export_attrs(df):
    for l in range(4, -1, -1):
        df1 = (
            df.groupby(get_ids(l), dropna=False)
            .sum(numeric_only=True, min_count=1)
            .reset_index()
        )
        df2 = pd.read_excel(get_attrs(l))
        df2["pop_src"] = "meta-fb"
        df2 = df2.merge(df1, on=get_ids(l))
        if l > 0:
            df2["src_date"] = df2["src_date"].dt.date
            df2["src_update"] = df2["src_update"].dt.date
        df2["wld_date"] = df2["wld_date"].dt.date
        df2["wld_update"] = df2["wld_update"].dt.date
        df3 = pd.read_parquet(outputs / f"../worldpop/adm{l}_population.parquet")
        df3 = df3.merge(df2, on=df3.columns.tolist()[:-2], how="outer")
        df3["t_x"] = df3["t_y"].combine_first(df3["t_x"])
        df3["pop_src_x"] = df3["pop_src_y"].combine_first(df3["pop_src_x"])
        df3 = df3.rename(columns={"t_x": "t", "pop_src_x": "pop_src"})
        df3 = df3.drop(columns=["t_y", "pop_src_y"])
        df3.to_parquet(outputs / f"adm{l}_population.parquet", index=False)
        df3.to_excel(outputs / f"adm{l}_population.xlsx", index=False)
        df3.to_csv(
            outputs / f"adm{l}_population.csv.zip",
            index=False,
            float_format="%.0f",
            encoding="utf-8-sig",
        )
        if l > 0:
            df3["src_date"] = pd.to_datetime(df3["src_date"])
            df3["src_date"] = df3["src_date"].dt.strftime("%Y-%m-%d")
            df3["src_update"] = pd.to_datetime(df3["src_update"])
            df3["src_update"] = df3["src_update"].dt.strftime("%Y-%m-%d")
        df3["wld_date"] = pd.to_datetime(df3["wld_date"])
        df3["wld_date"] = df3["wld_date"].dt.strftime("%Y-%m-%d")
        df3["wld_update"] = pd.to_datetime(df3["wld_update"])
        df3["wld_update"] = df3["wld_update"].dt.strftime("%Y-%m-%d")
        df3.to_json(outputs / f"adm{l}_population.json.zip", orient="records")


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(data / "meta_fb.parquet")
    df2 = pd.read_csv(config / "meta_fb.csv")
    df = df.merge(df2, on="iso_3")
    df = df[df["valid"] == 1]
    df = df.drop(columns=["count", "valid"])
    df = apply_factor(df)
    export_attrs(df)
    logger.info("finished")
