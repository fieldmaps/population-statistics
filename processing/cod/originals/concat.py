import pandas as pd
from pathlib import Path
from .utils import logging, adm0_list, get_srcs, get_cols, cols_meta

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / '../../../data/cod'
outputs = cwd / '../../../outputs/cod'


def main():
    frames = []
    outputs.mkdir(parents=True, exist_ok=True)
    output = (outputs / 'population.xlsx')
    output.unlink(missing_ok=True)
    for row in adm0_list:
        name = row['id']
        file = (data / f'{name}.xlsx')
        df = pd.read_excel(file, keep_default_na=False, na_values=['', '#N/A'])
        frames.append(df)
    df = pd.concat(frames)
    df = df[cols_meta[:1] + get_srcs(4) + cols_meta[1:] + get_cols()]
    df = df.sort_values(by=cols_meta[:1] + get_srcs(4))
    with pd.ExcelWriter(output) as w:
        df.to_excel(w, sheet_name='adm4', index=False)
        for lvl in range(3, -1, -1):
            df = df.groupby(cols_meta[:1] + get_srcs(lvl) + cols_meta[1:],
                            dropna=False).sum(min_count=1).reset_index()
            df.to_excel(w, sheet_name=f'adm{lvl}', index=False)
