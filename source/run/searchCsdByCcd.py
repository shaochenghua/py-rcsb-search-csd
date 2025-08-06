import os
import sys
import logging
# import mmcif

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(THIS_DIR)
UTIL_DIR = os.path.join(SRC_DIR, 'util')
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'log')

sys.path.insert(0, SRC_DIR)

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s')
fp_log = os.path.join(LOG_DIR, f"{os.path.basename(__file__).split('.')[0]}.log")
f_handler = logging.FileHandler(fp_log)
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(log_format)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(log_format)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(f_handler)
logger.addHandler(c_handler)

from ccdc.io import MoleculeReader
from ccdc.search import SubstructureSearch, MoleculeSubstructure
from search.searchCsdByMol import CsdSearch
from file_process.modifyCcdForConversion import FileModify
from file_process.convertCcdToMol import OpenBabelProcess


def main():
    choose_coordinates = "ideal"  # or "model"
    fp_in = os.path.join(DATA_DIR, "GLC.cif")
    fn_in = os.path.basename(fp_in)

    fm = FileModify(fp_in)
    fm.modify(on=choose_coordinates)

    fn_mod = fn_in.replace('.cif', f'-{choose_coordinates}.cif')
    fp_mod = os.path.join(DATA_DIR, fn_mod)

    fn_mol = fn_mod.split('.')[0] + '.mol2'
    fp_mol = os.path.join(DATA_DIR, fn_mol)

    op = OpenBabelProcess(fp_mod)
    op.convert(fp_mol)

    csd_search = CsdSearch()
    fn_mol = "GLC-ideal.mol2"
    fp_mol = os.path.join(DATA_DIR, fn_mol)
    csd_search.readMolFile(fp_mol)
    if csd_search.mol:
        csd_search.search_substructure()
        fn_out = os.path.basename(fp_mol).replace('.mol2', '_results.tsv')
        fp_out = os.path.join(DATA_DIR, fn_out)
        csd_search.reportHits(fp_out)
    else:
        logger.error("No molecule was read from the file.")


if __name__ == "__main__":
    main()
