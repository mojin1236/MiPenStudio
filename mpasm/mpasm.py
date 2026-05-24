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
bth = {
        "0000":"0",
        "0001":"1",
        "0010":"2",
        "0011":"3",
        "0100":"4",
        "0101":"5",
        "0110":"6",
        "0111":"7",
        "1000":"8",
        "1001":"9",
        "1010":"A",
        "1011":"B",
        "1100":"C",
        "1101":"D",
        "1110":"E",
        "1111":"F"
    }

with open(path, "r",encoding='utf-8') as f:
    code = [i.strip() for i in f.readlines()]
    byte = open(path.split('/')[-1].replace('.mpa', '.mpb'), "w",encoding='utf-8')
    mcr = open(path.split('/')[-1].replace('.mpa', '.mpr'), "w",encoding='utf-8')
    for i in code:
        if i.startswith(";"):
            continue
        elif i not in tbl.keys():
            byte.close()
            mcr.close()
            raise Invalid_instruction(f"Error: Invalid instruction '{i}'")
        else:
            print(f"Compiling instruction: {i} -> {tbl[i]}")
            byte.write(tbl[i]+';')
            mcr.write(bth[tbl[i]])
    byte.close()
    mcr.close()
    print("Compilation successful!")

print("Should it be compiled into mcr?(y/n)")

if input().lower() == 'y':
    with open(path.split('/')[-1].replace('.mpa', '.mpr'), "r",encoding='utf-8') as f:
        mcr_code = f.read()
        with open(path.split('/')[-1].replace('.mpa', '.mcr'), "w",encoding='utf-8') as f2:
            f2.write('MCR')
            f2.write(mcr_code)
    print("MCR file created successfully!")