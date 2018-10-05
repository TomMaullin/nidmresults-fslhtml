#!/usr/bin/env python3
import os
import shutil
import unittest
import sys
import string
from nidmviewerfsl import viewer
import glob
import urllib.request
import json
import zipfile
import urllib.parse


class general_tests(unittest.TestCase):

    # Run viewer.py on all turtle files in data folder
    # Checks for errors (program crashes)
    def test_error(self):

        script = os.path.dirname(os.path.abspath(__file__))
        dataFolder = os.path.join(script, "data")
        globData = os.path.join(dataFolder, "*.zip")
        data = glob.glob(globData)

        for i in data:  # Loop over all nidm zip files in data
            print(i)
            # Run viewer on zip file
            viewer.main(
                i, i.replace(".nidm.zip", "") + "_test_err", overwrite=True)


if __name__ == "__main__":

    scriptDir = os.path.dirname(os.path.abspath(__file__))
    dataDir = os.path.join(scriptDir, "data")

    if not os.path.isdir(dataDir):  # Data folder does not exist

        os.makedirs(dataDir)

    dataNames = ["ex_spm_conjunction", "ex_spm_contrast_mask",
                 "ex_spm_default", "ex_spm_full_example001",
                 "ex_spm_group_ols", "ex_spm_group_wls",
                 "ex_spm_HRF_informed_basis", "ex_spm_partial_conjunction",
                 "ex_spm_temporal_derivative", "ex_spm_thr_clustfwep05",
                 "ex_spm_thr_clustunck10", "ex_spm_thr_voxelfdrp05",
                 "ex_spm_thr_voxelfwep05", "ex_spm_thr_voxelunct4",
                 "fsl_con_f", "fsl_contrast_mask",
                 "fsl_default", "fsl_full_examples001",
                 "fsl_gamma_basis", "fsl_gaussian",
                 "fsl_group_btw", "fsl_group_ols",
                 "fsl_group_wls", "fsl_hrf_fir",
                 "fsl_hrf_gammadiff", "fsl_thr_clustfwep05",
                 "fsl_thr_voxelfwep05"]

    local = True
    for dataName in dataNames:  # Checks if data is on local machine

        # Data not found on local machine
        if not os.path.isfile(os.path.join(dataDir, dataName + ".nidm.zip")):

            local = False
            break

    if not local:  # Data not on local machine

        print("Downloading data")
        # Request from neurovault api
        req = urllib.request.Request(
            "http://neurovault.org/api/collections/4249/nidm_results")
        resp = urllib.request.urlopen(req)
        readResp = resp.read()
        data = json.loads(readResp.decode('utf-8'))

        for nidmResult in data["results"]:

            print(nidmResult["zip_file"])

            zipUrl = nidmResult["zip_file"]  # Url of zip file
            dataName = nidmResult["name"]  # Name of data (e.g. fsl_con_f.nidm)
            dataNameFile = os.path.join(dataDir, dataName + ".zip")

            if not os.path.isfile(dataNameFile):

                # copy zip file to local machine
                zipFileRequest = urllib.request.urlretrieve(zipUrl,
                                                            dataNameFile)

            dataPath = os.path.join(dataDir, dataName + ".zip")

    unittest.main()  # Tests
