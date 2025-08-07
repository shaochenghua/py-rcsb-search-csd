import os
import sys
import logging
import argparse
# import mmcif

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(THIS_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
LOG_DIR = os.path.join(ROOT_DIR, 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

sys.path.insert(0, SRC_DIR)

from ccdc.io import MoleculeReader
from ccdc.search import SubstructureSearch, MoleculeSubstructure
from search.searchCsdByMol import CsdSearch
from file_process.modifyCcdForConversion import FileModify
from file_process.convertCcdToMol import OpenBabelProcess
from util.downloadFile import downloadFile

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s')
fp_log = os.path.join(LOG_DIR, f"{os.path.basename(__file__).split('.')[0]}.log")
f_handler = logging.FileHandler(fp_log)
f_handler.setLevel(logging.WARNING)
f_handler.setFormatter(log_format)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)
c_handler.setFormatter(log_format)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(f_handler)
logger.addHandler(c_handler)


def run(fp_in, choose_coordinates="model", mol_type="mol2", use_existing_sdf=False, search_type="substructure"):
    """run the search of CSD by a CCD file

    Args:
        fp_in (_type_): file path of the input CCD file
        choose_coordinates (str, optional): _description_. Defaults to "ideal".
    """
    fn_in = os.path.basename(fp_in)
    id = fn_in.split('.')[0].split('_')[0]
    extension = fn_in.split('.')[-1].lower()

    if use_existing_sdf:
        choose_coordinates = "ideal"
        fp_mol = fp_in
    else:
        if extension in ['mol', 'mol2', 'sdf']:
            fp_mol = fp_in
        else:
            # prepare the input file
            fp_mod = os.path.join(DATA_DIR, id, f'{id}-{choose_coordinates}.cif')
            fm = FileModify(fp_in)
            fm.modify(on=choose_coordinates, fp_out=fp_mod)

            # convert to mol2 file
            fp_mol = os.path.join(DATA_DIR, id, f'{id}-{choose_coordinates}.{mol_type}')
            op = OpenBabelProcess(fp_mod)
            op.convert(fp_mol)

    # search CSD by the mol2 file
    csd_search = CsdSearch()
    csd_search.readMolFile(fp_mol)
    if csd_search.mol:
        if search_type == "substructure":
            csd_search.search_substructure()
        elif search_type == "similarity":
            csd_search.search_similarity()
        else:
            logger.error(f"Unknown search type: {search_type}")
            return

        fp_out = os.path.join(DATA_DIR, id, f'{id}-{choose_coordinates}-{search_type}.tsv')
        csd_search.reportHits(fp_out, search_type=search_type)
    else:
        logger.error("No molecule was read from the file.")


def main():
    parser = argparse.ArgumentParser(description="Run search of CSD by a CCD file")

    # add mutually exclusive group for NMR and EM, default is XRAY
    group_source = parser.add_mutually_exclusive_group(required=False)
    group_source.add_argument('-l', '--local_filepath', dest='local',
                              help="provide filepath of a local CCD mmCIF file")
    group_source.add_argument('-i', '--http_id', dest='http',
                              help="provide CCD ID to retrieve file from HTTP server")

    # add mutually exclusive group for -iPDB and -iCIF
    parser.add_argument('-c', '--choose_coordinates', dest='choose_coordinates', choices=['ideal', 'model'], default='model',
                        help="choose coordinates to use, 'ideal' or 'model' (default: model)")

    parser.add_argument('-t', '--type_for_conversion', dest='mol_type', choices=['mol2', 'mol', 'sdf'], default='mol2',
                        help="choose type to use for performing search, i.e. to convert CIF to: 'mol2', 'mol' or 'sdf' (default: mol2)")
    
    parser.add_argument('-u', '--use_http_sdf', action='store_true',
                        help="retrieve and use existing SDF file from HTTP archive for search")

    parser.add_argument('-s', '--search_type', dest='search_type', choices=['substructure', 'similarity'], default='substructure',
                        help="choose search type of 'substructure' or 'similarity' (default: substructure)")

    args = parser.parse_args()
    if args.local:
        if not os.path.exists(args.local):
            logger.error(f"File {args.local} does not exist.")
            sys.exit(1)
        fp_in = args.local
    elif args.http:
        folder = os.path.join(DATA_DIR, args.http)
        if not os.path.exists(folder):
            os.makedirs(folder)
        if args.use_http_sdf:
            fp_in = downloadFile(args.http, file_type="SDF", folder=folder)
        else:
            fp_in = downloadFile(args.http, file_type="CIF", folder=folder)
        if not fp_in:
            logger.error(f"Failed to retrieve file for CCD ID {args.http}.")
            sys.exit(1)
    else:
        logger.error("No input file provided. Use -local or -http to specify a CCD file.")
        sys.exit(1)  

    run(fp_in,
        args.choose_coordinates, 
        args.mol_type, 
        use_existing_sdf=args.use_http_sdf,
        search_type = args.search_type)


if __name__ == "__main__":
    main()
