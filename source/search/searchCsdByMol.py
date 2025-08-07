import os
import sys
import logging
from ccdc.io import MoleculeReader
from ccdc.search import SubstructureSearch, MoleculeSubstructure, SimilaritySearch

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(THIS_DIR)
UTIL_DIR = os.path.join(SRC_DIR, 'util')
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
LOG_DIR = os.path.join(ROOT_DIR, 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

sys.path.insert(0, SRC_DIR)

# log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s')
# fp_log = os.path.join(LOG_DIR, f"{os.path.basename(__file__).split('.')[0]}.log")
# f_handler = logging.FileHandler(fp_log)
# f_handler.setLevel(logging.DEBUG)
# f_handler.setFormatter(log_format)

# c_handler = logging.StreamHandler()
# c_handler.setLevel(logging.DEBUG)
# c_handler.setFormatter(log_format)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(f_handler)
# logger.addHandler(c_handler)


class CsdSearch:
    def __init__(self):
        self.mol = None
        self.hits = None
        self.fp_mol = None

    def readMolFile(self, fp_mol):
        """Read a molecule file and return a Molecule object."""
        self.fp_mol = fp_mol
        reader = MoleculeReader(fp_mol)
        if not reader:
            logger.error(f"Failed to read molecule file: {filepath}")
            return None
        self.mol = reader[0]

    def search_substructure(self):
        """Search for a substructure in the CSD file."""
        try:
            mol_substructure = MoleculeSubstructure(self.mol)
        except TypeError as e:
            print(f"\n!!! Search Failed !!! Check {self.fp_mol} file for missing bond specification which indicates failed Open Babel conversion. Error in creating MoleculeSubstructure: {e}\n")
            self.hits = []
            return
        except Exception as e:
            logger.error(f"Error creating MoleculeSubstructure: {e}")
            self.hits = []
            return
        sub_search = SubstructureSearch()
        sub_search.add_substructure(mol_substructure)
        try:
            self.hits = sub_search.search(max_hits_per_structure=1)
        except Exception as e:
            logger.error(f"Error during substructure search: {e}")
            self.hits = []
            return

    def search_similarity(self):
        """Search for similar structure in the CSD file."""
        sim_search = SimilaritySearch(self.mol)
        self.hits = sim_search.search(max_hits_per_structure=1)

    def reportHits(self, fp_out, search_type="substructure"):
        """Report the hits found in the search."""
        if not self.hits:
            print("\nNo hits found.\n")
        else:
            print(f"\n{len(self.hits)} hits written in {fp_out}\n")
            with open(fp_out, 'w') as f_out:
                for hit in self.hits:
                    f_out.write(f"{hit.identifier}\t")
                    if search_type == "similarity":
                        f_out.write(f"{round(hit.similarity, 2)}\t")
                    f_out.write(f"{hit.molecule.formula}\t")
                    f_out.write(f"{hit.molecule.smiles}\n")


def main():
    csd_search = CsdSearch()
    fn_mol = "SF4_ideal.sdf"
    fp_mol = os.path.join(DATA_DIR, fn_mol)
    csd_search.readMolFile(fp_mol)
    if csd_search.mol:
        csd_search.search_substructure()
        fn_out = fn_mol.split(".")[0] + '_results.tsv'
        fp_out = os.path.join(DATA_DIR, fn_out)
        csd_search.reportHits(fp_out)
    else:
        logger.error("No molecule was read from the file.")


if __name__ == "__main__":
    main()

# filepath = 'GLC.mol2'
# reader = MoleculeReader(filepath)
# mol = reader[0]
# mol_substructure = MoleculeSubstructure(mol)
# sub_search = SubstructureSearch()
# sub_search.add_substructure(mol_substructure)
# hits = sub_search.search()
# for hit in hits:
#     print(hit.identifier)
#     print(hit.molecule.smiles)
#     print(hit.molecule.name)
