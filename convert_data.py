import sys


fn = sys.argv[1]
out = sys.argv[2]
first_line = True
header = None
with open(fn) as fin:
    with open(out, "w") as fout:
        for line in fin:
            if first_line:
                first_line = False
            else:
                clean = line.strip().replace("{", "").replace("}", "").replace("'", "").split(",")
                if header is None:
                    header = []
                    for c in clean:
                        header.append(c.split(":")[0])
                    fout.write(",".join(header) + "\n")
                data = []
                for c in clean:
                    data.append(c.split(":")[1])
                fout.write(",".join(data) + "\n")


