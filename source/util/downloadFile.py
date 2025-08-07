"""
download utility for CCD files
CCDC conda environment is incompatible with https retrieval by urllib, requests, and wget python package.
Must use subprocess to call curl command line tool
"""

import os
import subprocess


def downloadFile(id, file_type="CIF", folder="/tmp"):
    """download file from PDB

    Args:
        id (str): id
        file_type (str, optional): id type. Defaults to "CIF".
        folder (str, optional): local folder to save the file. Defaults to "/tmp".

    Returns:
        filepath_local: local filepath. None if download fails.
    """
    # https://files.rcsb.org/ligands/download/A1A06.cif
    # https://files.rcsb.org/ligands/download/ATP.cif
    # https://files.rcsb.org/ligands/download/ATP_ideal.sdf
    try:
        id = id.strip().upper()
        if file_type == "CIF":
            url = f"https://files.wwpdb.org/pub/pdb/refdata/chem_comp/{id[-1]}/{id}/{id}.cif"
        elif file_type == "SDF":
            url = f"https://files.wwpdb.org/pub/pdb/refdata/chem_comp/{id[-1]}/{id}/{id}_ideal.sdf"
        else:
            print("file_type argument %s is not supported", file_type)
            return None
    except IndexError:
        print("id %s is invalid" % id)
        return None

    filepath_local = os.path.join(folder, url.split('/')[-1])

    if os.path.exists(filepath_local):
        os.remove(filepath_local)

    try:
        subprocess.run(['curl', '-o', filepath_local, url])
        print(f"\nDownload successful: {filepath_local}")
        return filepath_local
    except Exception as e:
        print(f"\nDownload failed: {e}")
        return None

def main():
    print(downloadFile("ATP", file_type="CIF", folder="/Users/chenghua/Projects/CSD_CCD/py-rcsb-search-csd/data"))
    print(downloadFile("ATP", file_type="SDF"))


if __name__ == "__main__":
    main()
