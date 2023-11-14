# CNS to Default PDB Converter
![Logo da Minha Aplicação](https://github.com/bposantos/CNS-to-Default-PDB-Converter/blob/873933b5cf614fc3c5fcb0b86af4db92256bf56d/logo_cns_pdb.png)

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
chmod +x cns_pdb_converter.py
```
And execute the code:
```python
cns_pdb_converter.py file_name.pdb
```
