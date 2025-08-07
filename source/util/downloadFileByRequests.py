"""
download utility for CCD files
"""

import os
import gzip
import shutil
# import urllib.request
import requests


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

    response = requests.get(url)
    with open(filepath_local, "wb") as f:
        f.write(response.content)

    return filepath_local


    # try:
    #     urllib.request.urlretrieve(url, filepath_local)
    # except urllib.error.HTTPError as err_http:
    #     print(err_http)
    #     print("%s file doesn't exist for id %s, check id" % (file_type, id))
    #     return None
    # except OSError as err_os:
    #     print(err_os)
    #     print("cannot write file to the designated folder %s, check privilege" % folder)
    #     return None
    # except Exception as err_other:
    #     print(err_other)
    #     print("fail to download %s file for id %s" % (file_type, id))
    #     return None
    # else:
    #     if filepath_local.endswith(".gz"):
    #         filepath_local_unzipped = filepath_local.strip(".gz")
    #         try:
    #             with gzip.open(filepath_local, 'rb') as file_in:
    #                 with open(filepath_local_unzipped, 'wb') as file_out:
    #                     shutil.copyfileobj(file_in, file_out)
    #                     os.remove(filepath_local)
    #             return filepath_local_unzipped
    #         except Exception as err_unzip:
    #             print(err_unzip)
    #             print("cannot unzip %s, check file format or privilege in the folder" % filepath_local)
    #             return None
    #     else:
    #         return filepath_local


def main():
    print(downloadFile("ATP", file_type="CIF", folder="/Users/chenghua/Projects/CSD_CCD/py-rcsb-search-csd/data"))
    print(downloadFile("ATP", file_type="SDF"))


if __name__ == "__main__":
    main()
