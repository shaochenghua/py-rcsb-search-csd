# reading a molecule from the CSD
from ccdc import io
csd_reader = io.EntryReader('CSD')
mol_abebuf = csd_reader.molecule('ABEBUF')
mol_abebuf.components
print(mol_abebuf.heaviest_component.smiles)

# Writing the molecule to a file
file_name = 'abebuf.mol2'
with io.MoleculeWriter(file_name) as mol_writer:
    mol_writer.write(mol_abebuf)

# Reading the molecule from the file
file_name = 'abebuf.mol2'
mol_reader =  io.MoleculeReader(file_name)
mol = mol_reader[0]
print(mol.smiles)

# Performing similarity searches
from ccdc.search import SimilaritySearch
sim_search = SimilaritySearch(mol_abebuf.heaviest_component)
hits = sim_search.search()
len(hits)
for h in hits:
    print('%8s %.3f %s' % (h.identifier, h.similarity, h.crystal.spacegroup_symbol)) 

# Performing substructure searches
from ccdc.search import SubstructureSearch, MoleculeSubstructure
mol_substructure = MoleculeSubstructure(mol_abebuf.heaviest_component)
substructure_search = SubstructureSearch()
sub_id = substructure_search.add_substructure(mol_substructure)
hits = substructure_search.search(max_hits_per_structure=1)
len(hits)
for h in hits:
    print('%s: (%s)' % (h.identifier, ', '.join('%d' % i for i in h.match_atoms(indices=True))))

# get input from SMARTS string
ar_methoxy_sub = ccdc.search.SMARTSSubstructure('[CH3:1][O:2][c:3]1[cH:4]ccc[cH:5]1')
ar_methoxy_search = ccdc.search.SubstructureSearch()
ar_methoxy_sub_id = ar_methoxy_search.add_substructure(ar_methoxy_sub)
ar_methoxy_hits = ar_methoxy_search.search(max_hit_structures=200, max_hits_per_structure=1)
len(ar_methoxy_hits)

filepath = 'ABEBUI.mol'
reader = ccdc.io.MoleculeReader(filepath)
mol = reader[0]
mol_substructure = MoleculeSubstructure(mol)
sub_search = SubstructureSearch()
sub_search.add_substructure(mol_substructure)
hits = sub_search.search()