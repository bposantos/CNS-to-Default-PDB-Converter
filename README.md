# Convert CNS PDB Files Into the Default Format

A code to convert the PDB coordinate file originated by the structure calculation software, CNS, into a format accepted by most tools, such as Molprobity and pyRAMA.

-- Works in one chain proteins.

## Usage
Export the code path, adding a line to `~/.bashrc` or `~/.bash_profile`:
```bash
export PATH="/caminho/do/seu/diretorio:$PATH"
```
After that:
```bash
source ./bashrc
```
Make the code executable:
```bash
chmod +x convert_pdb.py
```
And execute the code:
```python
convert_pdb.py file_name.pdb
```
## Suggestion
Open the CNS .pdb file in Chimera and export as PDB before beggining.
