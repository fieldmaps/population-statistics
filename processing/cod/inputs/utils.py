import requests
import pandas as pd
from pathlib import Path

cwd = Path(__file__).parent
COD_URL = cwd / '../../../config/cod_meta.csv'

fieldmap = {
    'ISO 3166-1 Alpha 3-Codes': 'iso_3',
    'Country name': 'name',
    'Country category': 'status',
    'COD-PS URL': 'src_url',
}


def get_cod_meta():
    df = pd.read_csv(COD_URL)
    df = df[fieldmap.keys()]
    df = df.rename(columns=fieldmap)
    return df.to_dict('records')


def get_hdx_metadata(url):
    id = url[33:]
    url = f'https://data.humdata.org/api/3/action/package_show?id={id}'
    data = requests.get(url).json().get('result')
    return data


def join_hdx_meta(row, hdx):
    row['src_date'] = hdx['dataset_date'][1:11]
    row['src_update'] = hdx['last_modified'][:10]
    row['src_name'] = hdx['dataset_source']
    row['src_name1'] = hdx['organization']['title']
    row['src_lic'] = hdx['license_title']
    return row
