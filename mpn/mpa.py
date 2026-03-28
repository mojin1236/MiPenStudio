print("=====================================================================")
print("============== MPA    The assembly compiler for MiPen ===============")
print("=====================================================================")
print("================= Version 1.0.1a ========= MPS's subprogram =========")
print("=====================================================================\n\n")

path = input("Enter the path of the code file: ")

tbl = {
        "new":"0000",
        "add":"0001",
        "min":"0010",
        "lft":"0011",
        "rit":"0100",
        "pop":"0101",
        "push":"0110",
        "do":"0111",
        "loop":"1000",
        "prt":"1001",
        "inp":"1010",
        "int":"1011",
        "jmp":"1100",
        "cmp":"1101",
        "ifj":"1110",
        "pull":"1111"
    }

with open(path, "r") as f:
    code = f.readlines()
    code = [line.strip() for line in code if not line.startswith(";")]
    for line in code:
        if line.startswith(";"):
            code.pop(code.index(line))
        if line.startswith("sadd"):
            num = line.split()[1]
            p = code.index(line)
            code[p] = "add"
            for i in range(int(num)-1):
                code.insert(p+1, "add")
        if line.startswith("smin"):
            num = line.split()[1]
            p = code.index(line)
            code[p] = "min"
            for i in range(int(num)-1):
                code.insert(p+1, "min")
        if line.startswith("slft"):
            num = line.split()[1]
            p = code.index(line)
            code[p] = "lft"
            for i in range(int(num)-1):
                code.insert(p+1, "lft")
        if line.startswith("srit"):
            num = line.split()[1]
            p = code.index(line)
            code[p] = "rit"
            for i in range(int(num)-1):
                code.insert(p+1, "rit")
    r = '\n'.join(code)
    
"""code = f.readlines()
    ret = ''
    for line in code:
        line = line.strip()
        ret += tbl[line]"""