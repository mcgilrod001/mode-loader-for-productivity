
def run_file(file):
    import AppOpener as Ao
    if file[-4:] != ".txt":
        file = file + ".txt"
    with open(f"./configs/{file}") as f:
        for line in f:
            Ao.open(line, match_closest=True)
    f.close()