from zipfile import ZipFile

import pandas as pd
import requests

from .utils import ADM0_URL, DATA_URL, cwd, logging

logger = logging.getLogger(__name__)
data = cwd / "../../../inputs/un_wpp"


def download_file(url):
    data.mkdir(parents=True, exist_ok=True)
    file = data / url.split("/")[-1]
    r = requests.get(url)
    with open(file, "wb") as f:
        f.write(r.content)
    if url.endswith(".zip"):
        with ZipFile(file, "r") as z:
            data_file = data / z.namelist()[0]
            z.extractall(data)
        file.unlink()
        return data_file
    return file


def main():
    un_wpp = download_file(DATA_URL)
    adm0 = download_file(ADM0_URL)
    df = pd.read_csv(un_wpp, low_memory=False)
    df1 = pd.read_excel(adm0)
    df1 = df1[["iso_cd", "iso_3"]].drop_duplicates()
    df1 = df1.rename(columns={"iso_cd": "LocID"})
    df = df.merge(df1, on="LocID")
    df.to_csv(un_wpp, index=False)
    adm0.unlink(missing_ok=True)
    logger.info("finished")
