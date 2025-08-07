import os
import sys
import logging

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


class FileModify:
    def __init__(self, fp_in):
        self.fn = os.path.basename(fp_in)
        self.fp_in = fp_in

    def modify(self, on = "model", fp_out=None):
        """change _chem_comp_atom.model_Cartn_x 
        or _chem_comp_atom.pdbx_model_Cartn_x_ideal
        to _atom_site.Cartn_x
        to prepare for conversion to mol file by openbabel

        Args:
            on (str, optional): to convert model-coordinates or ideal-coordinates. Defaults to "model-coordinates".
        """
        if not fp_out:
            fn_out = self.fn.split('.')[0] + "-" + on + ".cif"
            fp_out = os.path.join(DATA_DIR, fn_out)

        logger.info(f"To modify {self.fp_in} to {fp_out} on {on}.")     
        with open(self.fp_in, 'r') as f_in, open(fp_out, 'w') as f_out:
            for line in f_in:
                if line.strip().startswith('_chem_comp_atom.'):
                    line = line.replace("_chem_comp_atom.", "_atom_site.")
                    if on == "model":
                        line = line.replace(".model_Cartn_x", ".Cartn_x")
                        line = line.replace(".model_Cartn_y", ".Cartn_y")
                        line = line.replace(".model_Cartn_z", ".Cartn_z")
                    elif on == "ideal":
                        line = line.replace(".pdbx_model_Cartn_x_ideal", ".Cartn_x")
                        line = line.replace(".pdbx_model_Cartn_y_ideal", ".Cartn_y")
                        line = line.replace(".pdbx_model_Cartn_z_ideal", ".Cartn_z")
                    else:
                        pass
                else:
                    pass
                f_out.write(line)
        if os.path.isfile(fp_out):
            if os.path.getsize(fp_out) > 0:
                logger.info(f"Success! modified file to {fp_out}.")
                return True
            else:
                logger.error(f"Failure! File {fp_out} is empty after modification.")
                return False
        else:
            logger.error(f"Failure! File {fp_out} does not exist after modification.")
            return False

def main():
    fp_in = "/Users/chenghua/Downloads/GLC.cif"
    fm = FileModify(fp_in)
    fm.modify(on="ideal")


if __name__ == "__main__":
    main()
