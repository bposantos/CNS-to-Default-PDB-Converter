# Convert CNS PDB Files Into the Default Format

A code to convert the PDB coordinate file originated by CNS structure calculation software, into a format accepted by most tools, such as Molprobity.

-- Works in one chain proteins.

## Usage
export the code path, adding a line to `~/.bashrc` or `~/.bash_profile`:
```bash
export PATH="/caminho/do/seu/diretorio:$PATH"
```
After that:
```bash
source ./bashrc
```

```python
convert_pdb.py file_name.pdb
```
## Suggestion
Open the CNS .pdb file in Chimera and export as PDB before beggining.
