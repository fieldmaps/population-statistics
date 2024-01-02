import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

cwd = Path(__file__).parent
grps = ["t", "f", "m"]
dests = [
    "00_04",
    "05_09",
    "10_14",
    "15_19",
    "20_24",
    "25_29",
    "30_34",
    "35_39",
    "40_44",
    "45_49",
    "50_54",
    "55_59",
    "60_plus",
]
special = ["t_15_24", "f_15_49"]
cols_meta = ["iso_3", "pop_lvl", "pop_year"]


def get_cols():
    cols = [*grps]
    for grp in grps:
        for dest in dests:
            cols.append(f"{grp}_{dest}")
    cols = cols + special
    return cols


def get_col_map():
    col_map = {}
    for dest in dests:
        start, end = dest.split("_")
        if end == "plus":
            end = "200"
        for i in range(int(start), int(end) + 1):
            col_map[i] = dest
    col_map[999] = "999"
    return col_map


def get_all_meta():
    dtypes = {"cod_lvl": "Int8", "cod_lvl_max": "Int8", "cod_year": "Int16"}
    df = pd.read_csv(
        cwd / "../../../config/meta.csv",
        dtype=dtypes,
        keep_default_na=False,
        na_values=["", "#N/A"],
    )
    df = df.rename(
        columns={
            "cod_lvl": "pop_lvl",
            "cod_lvl_max": "pop_lvl_max",
            "cod_year": "pop_year",
        }
    )
    df["id"] = df["iso_3"].str.lower()
    df["pop_lvl_max"] = df["pop_lvl_max"].combine_first(df["pop_lvl"])
    df = df[["id", "iso_3", "pop_lvl", "pop_lvl_max", "pop_year"]]
    return df[df["pop_lvl"] >= 0]


def get_ids(lvl, simple=False, reverse=False):
    result = []
    if reverse:
        for l in range(0, lvl + 1):
            result.extend([f"adm{l}_id"])
    else:
        for l in range(lvl, -1, -1):
            if simple:
                result.extend([f"adm{l}_id"])
            else:
                result.extend([f"adm{l}_id", f"adm{l}_src"])
    return result


def get_srcs(lvl):
    return [f"adm{l}_src" for l in range(lvl, -1, -1)]


def get_src_meta():
    df = pd.read_csv(
        cwd / "../../../config/cod.csv", keep_default_na=False, na_values=["", "#N/A"]
    )
    return df


def join_meta(df1, df2):
    df = df1.merge(df2, on="iso_3")
    return df.to_dict("records")


meta_local = get_all_meta()
meta_src = get_src_meta()
adm0_list = join_meta(meta_local, meta_src)
cols = get_cols()
col_map = get_col_map()
