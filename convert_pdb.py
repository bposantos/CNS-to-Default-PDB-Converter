#!/usr/bin/env python3

import argparse
import os
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert CNS PDB files to default.')
    parser.add_argument('pdbfile', help='PDB file to be converted')
    return parser.parse_args()

def main():
    # Get the current working directory
    current_directory = os.getcwd()

    args = parse_arguments()

    with open(args.pdbfile, 'r') as infile:
        lines = infile.readlines()

    def modify_nh2(lines):
        for i, line in enumerate(lines):
            lines[i] = line.replace("H   NH2    ", "HN1 NH2    ").replace("H'  NH2    ", "HN2 NH2    ")

        return lines

    def correct_model_endmdl(lines):
        num_models = 0
        has_endmdl = False
        has_model_before_atom = False
        corrected_lines = []

        for line in lines:
            if line.startswith('MODEL'):
                num_models += 1
                has_endmdl = False  # Reset the flag when a new model starts
                has_model_before_atom = True  # Assume there is a MODEL line before 'ATOM 1'
                corrected_lines.append(line)
            elif line.startswith('ATOM      1'):
                # If 'ATOM 1' line is found, check if there is a MODEL line before it
                if not has_model_before_atom:
                    num_models += 1
                    has_endmdl = False  # Reset the flag when a new model starts
                    corrected_lines.append('MODEL     {:>4}\n'.format(num_models))
                corrected_lines.append(line)
                has_model_before_atom = True
            elif line.startswith('ENDMDL'):
                has_endmdl = True
                corrected_lines.append(line)
                has_model_before_atom = False  # Reset the flag when a new model ends
            elif line.startswith('END') and not has_endmdl:
                # Replace each line 'END' with 'ENDMDL' if a preceding ENDMDL line is not present
                corrected_lines.append('ENDMDL\n')
            else:
                corrected_lines.append(line)

        return corrected_lines

    def insert_atoms(lines):
        for i, line in enumerate(lines):
            if "1.00  0.00         A" in line:
                atom_name = line[12:16].strip()  # Third column (ATOM name)
                last_column = line[75]  # Last column (last character of the line)
                # Get the first letter of the third column
                first_letter = atom_name[0]
                # Substitute the last column
                lines[i] = line[:75] + "  " + first_letter + line[76:]

        return lines

    def atoms_from_chimera(lines):
        for i, line in enumerate(lines):
            # Modify atom lines as needed
            if "0.00         A H" in line:
                lines[i] = line.replace("0.00         A H", "0.00           H")
            elif "0.00         A O" in line:
                lines[i] = line.replace("0.00         A O", "0.00           O")
            elif "0.00         A N" in line:
                lines[i] = line.replace("0.00         A N", "0.00           N")
            elif "0.00         A C" in line:
                lines[i] = line.replace("0.00         A C", "0.00           C")

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
                prev_line = modified_lines[-2]
                match = re.search(r"(ATOM|HETATM)\s+(\d+)\s+\S+\s+(\S{3})\s+(\S)\s+(\d+)", prev_line)
                # Add the "TER" line with extracted information
                ter_line = f"TER     {int(match.group(2))+1}      {match.group(3)} {match.group(4)}  {match.group(5)}\n"
                modified_lines.insert(-1, ter_line)

        return modified_lines

    def remove_remark_lines(lines):
        return [line for line in lines if not line.startswith("REMARK")]

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
    lines = correct_model_endmdl(lines)
    lines = insert_atoms(lines)
    lines = atoms_from_chimera(lines)
    lines = chain(lines)
    lines = add_ter(lines)
    lines = remove_remark_lines(lines)
    lines = remove_conect_lines_except_last_model(lines)

    # Write the filtered content to the output file
    with open(current_directory + "/output.pdb", 'w') as outfile:
        outfile.writelines(lines)

if __name__ == "__main__":
    main()
