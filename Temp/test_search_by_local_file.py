# reading a molecule from the CSD
from ccdc.io import MoleculeReader
from ccdc.search import SubstructureSearch, MoleculeSubstructure

filepath = 'GLC.mol2'
reader = MoleculeReader(filepath)
mol = reader[0]
mol_substructure = MoleculeSubstructure(mol)
sub_search = SubstructureSearch()
sub_search.add_substructure(mol_substructure)
hits = sub_search.search()
for hit in hits:
    print(hit.identifier)
    print(hit.molecule.smiles)
    print(hit.molecule.name)
