# CNS PDB to Default PDB Converter
![Logo da Minha Aplicação](https://github.com/bposantos/CNS-to-Default-PDB-Converter/blob/823a8308be454263a8bb707c0f570be14e05da6b/logo_cns_pdb.png)

A code to correct the coordinate file (.pdb), originated by CNS (structure calculation software), into the standard format.

-- Works in one chain proteins.

## Usage
Export the code path, adding a line to `~/.bashrc` or `~/.bash_profile`:
```bash
export PATH="/caminho/do/seu/diretorio:$PATH"
```
Alternatively, move the 'cns_pdb_converter' file to /usr/local/bin/
```bash
sudo mv cns_pdb_converter /usr/local/bin/
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
cns_pdb_converter file_name.pdb
```
