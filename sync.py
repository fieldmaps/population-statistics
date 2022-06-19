from pathlib import Path
import subprocess

cwd = Path(__file__).parent

if __name__ == '__main__':
    subprocess.run([
        's3cmd', 'sync',
        '--acl-public',
        '--delete-removed',
        '--rexclude', '\/\.',
        '--multipart-chunk-size-mb=5120',
        cwd / f'outputs/',
        's3://data.fieldmaps.io/population/',
    ])
