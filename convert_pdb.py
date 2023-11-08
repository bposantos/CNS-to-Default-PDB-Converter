#!/usr/bin/env python3

import re

# Load input PDB file
input_pdb_file = input("Digite o nome do arquivo pdb (com o caminho): ")
caminho = input_pdb_file.split("/")[:-1]
caminho = "/".join(caminho)

with open(input_pdb_file, 'r') as infile:
    lines = infile.readlines()

def modify_nh2(lines):
    for i in range(len(lines)):
        if "H   NH2    " in lines[i]:
            lines[i] = lines[i].replace("H   NH2    ", "HN1 NH2    ")
        elif "H'  NH2    " in lines[i]:
            lines[i] = lines[i].replace("H'  NH2    ", "HN2 NH2    ")

    return lines

def atoms(lines):
    for i in range(len(lines)):
        # Modify atom lines as needed
        if "0.00         A H" in lines[i]:
            lines[i] = lines[i].replace("0.00         A H", "0.00           H")
        elif "0.00         A O" in lines[i]:
            lines[i] = lines[i].replace("0.00         A O", "0.00           O")
        elif "0.00         A N" in lines[i]:
            lines[i] = lines[i].replace("0.00         A N", "0.00           N")
        elif "0.00         A C" in lines[i]:
            lines[i] = lines[i].replace("0.00         A C", "0.00           C")

    return lines

def chain(lines):
    modified_lines = []

    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            # Modify chain as needed
            residue_name = line[17:20]
            if len(residue_name) == 3 or (residue_name == "NH2"):
                line = line[:21] + "A" + line[22:]

        modified_lines.append(line)

    return modified_lines

def add_ter(lines):
    modified_lines = []
    in_model = False

    for line in lines:
        if line.startswith("MODEL"):
            in_model = True
        elif line.strip() == "ENDMDL":
            in_model = False

        modified_lines.append(line)

        if not in_model and line.strip() == "ENDMDL":
            # Add the "TER" line before "ENDMDL"
            #modified_lines.insert(-1, "TER\n")
            prev_line = modified_lines[-2]
            match = re.search(r"(ATOM|HETATM)\s+(\d+)\s+\S+\s+(\S{3})\s+(\S)\s+(\d+)", prev_line)            
            # Add the "TER" line with extracted information
            ter_line = f"TER     {int(match.group(2))+1}      {match.group(3)} {match.group(4)}  {match.group(5)}\n"
            modified_lines.insert(-1, ter_line)

    return modified_lines


def remove_remark_lines(lines):
    filtered_lines = [line for line in lines if not line.startswith("REMARK")]
    return filtered_lines

def remove_conect_lines_except_last_model(lines):
    model_indices = [i for i, line in enumerate(lines) if line.startswith("MODEL")]

    if len(model_indices) < 2:
        return lines

    for i in range(len(model_indices) - 1):
        start_index = model_indices[i]
        end_index = model_indices[i + 1]
        for j in range(start_index, end_index):
            if lines[j].startswith("CONECT"):
                lines[j] = ""

    return lines

# Apply modifications in the desired sequence
lines = modify_nh2(lines)
lines = atoms(lines)
lines = chain(lines)
lines = add_ter(lines)
lines = remove_remark_lines(lines)
lines = remove_conect_lines_except_last_model(lines)

# Write the filtered content to the output file
with open(caminho+"/output.pdb", 'w') as outfile:
    outfile.writelines(lines)
