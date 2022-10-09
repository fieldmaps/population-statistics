import subprocess

funcs = ['boundaries.inputs', 'meta_fb.inputs',
         'worldpop.data', 'meta_fb.data', 'un_wpp.data',
         'worldpop.outputs', 'meta_fb.outputs', 'un_wpp.outputs']

if __name__ == '__main__':
    for func in funcs:
        subprocess.run(['python3', '-m', f'processing.{func}'])
    subprocess.run(['python3', 'sync.py'])
