import json
from pathlib import Path

import pandas as pd

from .utils import DATA_URL, dests, land_date, world_views

cwd = Path(__file__).parent
outputs = cwd / "../../outputs"


def main(name):
    outputs.mkdir(exist_ok=True, parents=True)
    data = []
    for dest in dests:
        for wld in world_views:
            for l in range(4, -1, -1):
                row = {
                    "id": f"{dest}_{wld}_adm{l}",
                    "grp": dest,
                    "wld": wld,
                    "adm": l,
                    "date": land_date,
                    "c_xlsx": f"{DATA_URL}/{name}/{dest}/{wld}/cod/adm{l}_population.xlsx",
                    "c_csv": f"{DATA_URL}/{name}/{dest}/{wld}/cod/adm{l}_population.csv.zip",
                    "c_json": f"{DATA_URL}/{name}/{dest}/{wld}/cod/adm{l}_population.json.zip",
                    "m_xlsx": f"{DATA_URL}/{name}/{dest}/{wld}/meta-fb/adm{l}_population.xlsx",
                    "m_csv": f"{DATA_URL}/{name}/{dest}/{wld}/meta-fb/adm{l}_population.csv.zip",
                    "m_json": f"{DATA_URL}/{name}/{dest}/{wld}/meta-fb/adm{l}_population.json.zip",
                    "w_xlsx": f"{DATA_URL}/{name}/{dest}/{wld}/worldpop/adm{l}_population.xlsx",
                    "w_csv": f"{DATA_URL}/{name}/{dest}/{wld}/worldpop/adm{l}_population.csv.zip",
                    "w_json": f"{DATA_URL}/{name}/{dest}/{wld}/worldpop/adm{l}_population.json.zip",
                }
                data.append(row)
    with open((outputs / f"{name}.json"), "w") as f:
        json.dump(data, f, separators=(",", ":"))
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.date
    df.to_csv(outputs / f"{name}.csv", index=False, encoding="utf-8-sig")
    df.to_excel(outputs / f"{name}.xlsx", index=False)
