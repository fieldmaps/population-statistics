import subprocess

funcs = [
    "meta",
    "boundaries.inputs",
    # "un_wpp.inputs",
    # "worldpop.inputs",
    "un_wpp.data",
    "worldpop.data",
    "worldpop.outputs",
]

if __name__ == "__main__":
    for func in funcs:
        subprocess.run(["python", "-m", f"app.{func}"])
    subprocess.run(["python", "sync.py"])
