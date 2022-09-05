import filecmp
import subprocess
from processing.meta_fb.inputs.utils import DATABASE, cwd, logging, run_process, data_types

logger = logging.getLogger(__name__)
data = cwd / f'../../../inputs/meta_fb'


def input_data(name):
    query = (data / f'{name}.sql').resolve()
    query.unlink(missing_ok=True)
    with open(query, 'w') as f:
        subprocess.run([
            'raster2pgsql',
            '-d', '-C', '-I', '-R', '-Y',
            '-t', '512x512',
            (data / f'hrsl_{name}/hrsl_{name}-latest.vrt').resolve(),
            f'meta_fb_pop_{data_types[name]}',
        ], stdout=f, stderr=subprocess.DEVNULL)
    subprocess.run([
        'psql',
        '--quiet',
        '-d', DATABASE,
        '-f', query,
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    query.unlink(missing_ok=True)
    logger.info(name)


def main():
    vrt_imported = data / 'hrsl-imported.vrt'
    vrt_latest = data / 'hrsl_general-latest.vrt'
    if not vrt_imported.is_file():
        run_process(input_data)
    elif not filecmp.cmp(vrt_imported, vrt_latest):
        run_process(input_data)
    vrt_latest.rename(vrt_imported)
