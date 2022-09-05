import numpy as np
import pandas as pd
from processing.cod.outputs.utils import logging, cwd, grps, dests, get_ids, get_cols

logger = logging.getLogger(__name__)
data = cwd / '../../../data'
outputs = cwd / '../../../outputs'


def main():
    df1 = pd.read_excel(data / 'cod.xlsx')
    df2 = pd.read_excel(outputs / 'un_wpp.xlsx', sheet_name='adm4_id')
    for grp in grps:
        for dest in dests:
            if not f'{grp}_{dest}' in df2.columns:
                df2[f'{grp}_{dest}'] = np.nan
    df2 = df2[get_ids() + get_cols()]
    for _, r1 in df1.iterrows():
        id_col = 'adm' + r1['ps_lvl'] + '_id'
        for i, r2 in df2.iterrows():
            if r2[id_col] == r1[id_col]:
                for col in get_cols():
                    df2.loc[i, col] = 1
    with pd.ExcelWriter(outputs / 'cod.xlsx') as w:
        for l in range(4, 3, -1):
            df2 = df2.groupby(get_ids(l), dropna=False).sum(
                min_count=1).reset_index()
            sheet_name = f'adm{l}_id' if l >= 0 else 'iso_3'
            df2.to_excel(w, sheet_name=sheet_name, index=False)
