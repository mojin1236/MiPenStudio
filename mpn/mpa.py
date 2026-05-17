class Invalid_instruction(Exception):
    pass

print("=====================================================================")
print("============== MPA    The assembly compiler for MiPen ===============")
print("=====================================================================")
print("================= Version 1.0.1a ========= MPS's subprogram =========")
print("=====================================================================\n\n")

path = input("Enter the path of the code file: ")

tbl = {
        "add":"0000",
        "min":"0001",
        "rit":"0010",
        "lft":"0011",
        "pull":"0100",
        "pop":"0101",
        "push":"0110",
        "ac":"0111",
        "int":"1000",
        "prt":"1001",
        "inp":"1010",
        "jmp":"1011",
        "cmp":"1100",
        "do":"1101",
        "loop":"1110",
        "null":"1111"
    }

with open(path, "r",encoding='utf-8') as f:
    code = [i.strip() for i in f.readlines()]
    byte = open(path.split('/')[-1].replace('.mpa', '.mpb'), "w",encoding='utf-8')
    for i in code:
        if i.startswith(";"):
            continue
        elif i not in tbl.keys():
            byte.close()
            raise Invalid_instruction(f"Error: Invalid instruction '{i}'")
        else:
            byte.write(tbl[i]+';')
    byte.close()

