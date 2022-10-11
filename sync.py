import subprocess
from pathlib import Path

cwd = Path(__file__).parent
exts = ['json', 'csv', 'xlsx']

if __name__ == '__main__':
    for ext in exts:
        subprocess.run([
            's3cmd', 'sync',
            '--acl-public',
            cwd / f'outputs/population.{ext}',
            f's3://data.fieldmaps.io/population.{ext}',
        ])
    subprocess.run([
        's3cmd', 'sync',
        '--acl-public',
        '--delete-removed',
        '--rexclude', '\/\.',
        '--multipart-chunk-size-mb=5120',
        cwd / f'outputs/population/humanitarian',
        f's3://data.fieldmaps.io/population/',
    ])
