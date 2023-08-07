
L = []
with open("full.csv", "r",encoding='utf-8') as f:
    i = -1
    for l in f.readlines():
        i+=1
        if i < 9:
            continue
        
        t = l.strip().replace("\"","").replace(" ","").split(",")
        if len(t) < 7:
            break
        if t[6] == "elf": # len(t) >=6 and 
            L += [t]
with open("elf.csv", "w") as f:
    for x in L:
        t = ",".join(x)
        f.write(t+"\n")
 