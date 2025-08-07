import os
import subprocess
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


class OpenBabelProcess:
    def __init__(self, fp_in):
        self.fn = os.path.basename(fp_in)
        self.fp_in = fp_in

    def convert(self, fp_out, l_options=[]):
        """run openbabel to convert ccd file to mol/mol2/sdf file
        file type to be converted is based on file extension

        Args:
            fp_out (_type_): filepath to output file, must have proper extension
            l_options (list, optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """        
        logger.info(f"To convert {self.fp_in} to {fp_out}.")     

        openbabel_cmd = os.getenv("OPENBABELCMD", "/usr/local/bin/obabel")
        l_command = [openbabel_cmd, self.fp_in, "-O", fp_out] + l_options
        logger.info(f"Running command: {' '.join(l_command)}")

        rt = subprocess.run(l_command, capture_output=True, text=True)
        if rt.returncode != 0:
            logger.error(f"Openbabel conversion failed with return code {rt.returncode}")
            logger.error(f"Error message: {rt.stderr}")
            return False
        else:
            logger.info(f"Openbabel conversion succeeded.")
            logger.debug(f"Standard output: {rt.stdout}")
            logger.debug(f"Standard error: {rt.stderr}")

        if os.path.isfile(fp_out):
            if os.path.getsize(fp_out) > 0:
                logger.info(f"Success! converted file to {fp_out}.")
                return True
            else:
                logger.error(f"Failure! File {fp_out} is empty after conversion.")
                return False
        else:
            logger.error(f"Failure! File {fp_out} does not exist after conversion.")
            return False

def main():
    fn_in = "GLC-ideal.cif"
    fp_in = os.path.join(DATA_DIR, fn_in)

    fn_out = fn_in.split('.')[0] + '.mol2'
    fp_out = os.path.join(DATA_DIR, fn_out)

    op = OpenBabelProcess(fp_in)
    op.convert(fp_out)

if __name__ == "__main__":
    main()
