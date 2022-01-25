import os, time, sys

os.system("cls")
f = sys.stdout

def count_json(path):
    x = 0
    for file in os.listdir(path):
        if file.endswith("json"):
            x += 1
    return x

f.write("Total: ")
while True:
    n = str(count_json("./data/"))
    f.write(n)
    f.flush()
    time.sleep(3)
    f.write("\b"*len(n))
    f.flush()