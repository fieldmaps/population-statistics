import json
import pandas as pd
from pathlib import Path
from processing.meta.utils import DATA_URL, dests, world_views, land_date

cwd = Path(__file__).parent
outputs = cwd / '../../outputs'


def main(name):
    outputs.mkdir(exist_ok=True, parents=True)
    data = []
    for dest in dests:
        for wld in world_views:
            for l in range(4, -1, -1):
                row = {
                    'id': f'{dest}_{wld}_adm{l}',
                    'grp': dest,
                    'wld': wld,
                    'adm': l,
                    'date': land_date,
                    'u_xlsx': f'{DATA_URL}/{name}/{dest}/{wld}/un-wpp/adm{l}_population.xlsx',
                    'u_csv': f'{DATA_URL}/{name}/{dest}/{wld}/un-wpp/adm{l}_population.csv.zip',
                    'u_json': f'{DATA_URL}/{name}/{dest}/{wld}/un-wpp/adm{l}_population.json.zip',
                    'm_xlsx': f'{DATA_URL}/{name}/{dest}/{wld}/meta-fb/adm{l}_population.xlsx',
                    'm_csv': f'{DATA_URL}/{name}/{dest}/{wld}/meta-fb/adm{l}_population.csv.zip',
                    'm_json': f'{DATA_URL}/{name}/{dest}/{wld}/meta-fb/adm{l}_population.json.zip',
                    'w_xlsx': f'{DATA_URL}/{name}/{dest}/{wld}/worldpop/adm{l}_population.xlsx',
                    'w_csv': f'{DATA_URL}/{name}/{dest}/{wld}/worldpop/adm{l}_population.csv.zip',
                    'w_json': f'{DATA_URL}/{name}/{dest}/{wld}/worldpop/adm{l}_population.json.zip',
                }
                data.append(row)
    with open((outputs / f'{name}.json'), 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    df.to_csv(outputs / f'{name}.csv', index=False)
    df.to_excel(outputs / f'{name}.xlsx', index=False)