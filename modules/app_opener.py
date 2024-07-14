import AppOpener as Ao

file = "config2.txt"
with open(f"./configs/{file}") as f:
    for line in f:
        Ao.open(line, match_closest=True)