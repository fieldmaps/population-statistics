import subprocess

funcs = ['meta', 'boundaries.inputs', 'boundaries.data', 'meta_fb.inputs',
         'worldpop.data', 'meta_fb.data', 'cod.data',
         'worldpop.outputs', 'meta_fb.outputs', 'cod.outputs']

if __name__ == '__main__':
    for func in funcs:
        subprocess.run(['python3', '-m', f'processing.{func}'])
    subprocess.run(['python3', 'sync.py'])
