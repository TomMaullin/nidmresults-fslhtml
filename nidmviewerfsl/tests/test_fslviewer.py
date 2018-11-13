#!/usr/bin/env python3
from nidmviewerfsl import viewer
import unittest
import sys
import os
import glob
import urllib.request
import json
from ddt import ddt, data


# This is the class of tests for testing specific features of datasets.
@ddt
class test_dataset_features(unittest.TestCase):


    # Create a structure for each test datapack. These structures consist
    # of information about each datapack that should be included in the
    # display produced by the viewer.
    fsl_con_f = {'Name': 'fsl_con_f',
                 'softwareName': 'FSL',
                 'version': '6.00',
                 'hThresh': 'P = 0.001 (uncorrected)',
                 'lowSliceVal': '3.09',
                 'highSliceVal': '7.4',
                 'numExc': 2,
                 'desMatExtract': 'dO9drThsTEyZMUHf83LmfX/mP/yVfAEAdAYA6A'
                                  'imqt7c32ksffPCBmj/PnTv3H43ZuTFXdN0333z'
                                  'j52cye/ZsdcePHz/+sTF7XN2Ym8eTLwCgjgBAH'
                                  'YHUdPHixYglJ0+eVLPojIwMEckY6p2+ceUcx2A'
                                  'rVqxQ97SlpUWfbmlp+ZOxvCV672NnP0S+AIA6A'
                                  'gB1BFLTjz/+aE6fPn1azasnT548eeAbEqWnp8d'
                                  '5IyUlJerehUKhUChUYSwJxd/L2NnkCwCoIwBQR'}

    fsl_contrast_mask = {'Name': 'fsl_contrast_mask',
                         'softwareName': 'FSL',
                         'matchConName': 'tone counting probe vs baseline',
                         'matchSliceImExtract': 'U8AKtFotcDQJAVgMgUAAz3c4'
                                                'HHD9LRZqgXmBdSAPhytdMgIs'
                                                'GZehf/Ep4HfQpK7rSALgcg8Y'
                                                'STKZLJfLiURCVVUQNol3wVBt'
                                                '8Cl8pJGREb/f7/V6KQcFOwW4'
                                                'C2YrkTqpBlI6HKUg2qYdsXfa'
                                                'diRVuFASDFl3OBzkWNPUyBbH'}

    fsl_thr_clustfwep05 = {'Name': 'fsl_thr_clustfwep05',
                           'softwareName': 'FSL',
                           'version': '6.00',
                           'hThresh': 'determined by Z > 2.3',
                           'eThresh': 'cluster significance of P = 0.05',
                           'sliceImExtract': 'oCaDieVMs7l8AnQVrJ6OiokBh'
                                             'AtVrFq5F3RX5wq9VSdoO09957'
                                             'bygUmpiYCIVCtVqt0Wi88847p'
                                             'VIJAXhYS9ya1GWpPZf43MQxWC'
                                             'sCnYXtHdn0CX+NRqPwRqCWBgY'
                                             'Gjh07ls1mZ2Zm0uk0Krxisdjt',
                           'lowSliceVal': '2.3',
                           'highSliceVal': '7.49',
                           'contrastName': 'tone counting vs baseline'}

    ex_spm_contrast_mask = {'Name': 'ex_spm_contrast_mask',
                            'softwareName': 'SPM',
                            'version': '12.6906',
                            'hThresh': 'P = 0.001 (uncorrected)',
                            'sliceImExtract': 'iiwq2wqlJgPVErKJI60sEFev'
                                              'BTjgm35DcCfbQMovFMKXCnps'
                                              'J9++unDh9XM8a8AACAASURBV'
                                              'A+0dcl0ciTIbbEjz8/PysJIE'
                                              'NYcKMDPjRVVyFNG122rtH1rl'
                                              'efwUpjLEALboR7935Wi3+9rL'
                                              '3766Scofc6A7AgqVFXVZrNBZ'
                                              'RVqo/14gtLGOGr9lbsh/0LUB',
                            'lowSliceVal': '3.18',
                            'highSliceVal': '7.92',
                            'contrastName': 'tone counting vs baseline'}

    fsl_gamma_basis = {'Name': 'fsl_gamma_basis',
                       'softwareName': 'FSL',
                       'numExc': 8,
                       'matchConName': 'tone counting vs baseline (1)&n'
                                       'bsp',
                       'matchSliceImExtract': 'mho6KWXXjp69CgC7fl8Hr1S6'
                                              'PthJLDsXXkgp5nNTk1NnTlzJ'
                                              'pFI9Pb2PvbYYw8++GA0Gv23y'
                                              '5dTqRQ8+9XVVYhQAuSqVnIV9'
                                              '508AqOzLQ/0AiqgadrZs2fn5'
                                              'uYef/zxubm5733ve1/72teOH'
                                              'z/+D//wD0B9fuXFF0tCPFCrH'}

    fsl_group_ols = {'Name': 'fsl_group_ols',
                     'softwareName': 'FSL',
                     'clusTabExtract': '4<td>399<td>0.000335<td>3.47<td'
                                       '>4.05<td>32<td>20<td>8',
                     'peakTabExtract': '<td>7<td>5.24<td>8.029e-08<'
                                       'td>7.10<td>-6<td>2<td>60'}

    fsl_group_wls = {'Name': 'fsl_group_wls',
                     'softwareName': 'FSL',
                     'clusTabExtract': '<td>7<td>1380<td>2.93e-10<td>9.'
                                       '53<td>5.32<td>-52<td>-2<td>54',
                     'peakTabExtract': '<td>7<td>5.32<td>5.188e-08<td>7'
                                       '.28<td>-52<td>-2<td>54'}

    fsl_default = {'Name': 'fsl_default',
                   'softwareName': 'FSL',
                   'clusTabExtract': '<td>149<td>795<td>7.47<td>40.625<'
                                     'td>25<td>15</tr>',
                   'peakTabExtract': '<td>149<td>7.47<td>4.008e-14<td>1'
                                     '3.40<td>40.625<td>25<td>15</tr>'}

    ex_spm_default = {'Name': 'ex_spm_default',
                      'softwareName': 'SPM',
                      'version': '12.6906',
                      'hThresh': 'P = 0.001 (uncorrected)',
                      'lowSliceVal': '3.18',
                      'highSliceVal': '7.92',
                      'numExc': 1,
                      'desMatExtract': 'fCRVgvijvXoD5oJzQy8G8URXMK1XZmy'
                                       'HMCzW0GjfX5WCcaRWM92adgjaEGQqaj'
                                       'aDSbO6pKyrAnFE/VIBxK3FYA8wudU1V'
                                       'MJVZYI+qdGinq18kwPhdHdYKphI0txI'
                                       'XcIBxug7N0JVms5gZumIEn1TFCIYwQ7'
                                       'ZmTKU8F4MZGjkqmM2aoTcLs5hMq9SNe'
                                       '1pl5LA3VmztgvqmAozv/pyLAcZtvhI0'
                                       'Y46pAON0rdiai68y3DoFdqgKphI0b/A',
                      'conVec': ['[1, 0, 0]'],
                      'conVecImEx': ['Ae9JREFUeJzt3UEKwkAQAEFH8v8vr1cjY'
                                     'uNBskjVLZDAXJthN7PWWjcAAIAP7lcPAA'
                                     'AA7E84AAAASTgAAADpeH6YmavmAAAANvJ'
                                     '6FNrGAQAASMIBAABIwgEAAEjCAQAASMIB'
                                     'AABIwgEAAEhHv3L2ei0T8F9cywwAvGPjA'
                                     'AAAJOEAAAAk4QAAACThAAAAJOEAAAAk4Q'
                                     'AAACThAAAAJOEAAAAk4QAAACThAAAAJOE'],
                      'clusTabExtract': '<td>3<td>5090<td>5.74<td>8<td>'
                                        '18<td>50',
                      'peakTabExtract': '<td>81<td>3.11<td>0.0009411<td'
                                        '>3.03<td>-44<td>-42<td>-36'}

    ex_spm_conjunction = {'Name': 'ex_spm_conjunction',
                          'softwareName': 'SPM',
                          'version': '12.6906',
                          'sliceImExtract': 'GdpFUAoggiMIM9AcHT02SmBVw4'
                                            'Z/WKI8/Li4urq6ukIK4WmQbJxq'
                                            'fUpbl4+NjURTL5fLl5UW8GgtO4'
                                            'E3gSmoJAwUIw+5B9qgUqbXX2wb'
                                            '2uxBEUZp4GMhkQVq0Sm5DsAg9J'
                                            'l8jb0cY11qvHasD8yk/h4ZtNpv'
                                            'lcrlarUAn6/UaJOVR4fsjPB9ro',
                          'lowSliceVal': '3.18',
                          'highSliceVal': '5.65',
                          'contrastName': ['tone counting probe vs baseline',
                                           'tone counting vs baseline'],
                          'numExc': 1,
                          'conVec': ['[0, 1, 0]', '[1, 0, 0]'],
                          'conVecImEx': ['Jzt3UEKwkAQAEFH8v8vr1cjYuNBskjVL'
                                         'ZDAXJthN7PWWjcAAIAP7lcPAAAA7E84A'
                                         'AAASTgAAADpeH6YmavmAAAANvJ6FNrGA'
                                         'QAASMIBAABIwgEAAEjCAQAASMIBAABIw'
                                         'gEAAEhHv3L2ei0T8F9cywwAvGPjAAAAJ'
                                         'OEAAAAk4QAAACThAAAAJOEAAAAk4QAAA'
                                         'CThAAAAJOEAAAAk4QAAACThAAAAJOEAA',
                                         'e5JREFUeJzt3TEKwzAQAMEo+P9fvrSJi'
                                         '2wpgWc6g4prl0Pympl5AQAA/PHePQAAA'
                                         'HA+4QAAACThAAAApOv7Y621aw4AAOAg9'
                                         '6vQNg4AAEASDgAAQBIOAABAEg4AAEASD'
                                         'gAAQBIOAABAuvoI8CT3p9eAZ/JEO3Bn4'
                                         'wAAACThAAAAJOEAAAAk4QAAACThAAAAJ'
                                         'OEAAAAk4QAAACThAAAAJOEAAAAk4QAAA'
                                         'CThAAAAJOEAAAAk4QAAACThAAAAJOEAA']}

    fsl_con_f_multiple = {'Name': 'fsl_con_f_multiple',
                          'softwareName': 'FSL',
                          'version': '6.00',
                          'numExc': 5,
                          'matchConName': 'tone counting vs baseline & to'
                                          'ne counting probe',
                          'matchSliceImExtract': 'JzxCCxFBgnLZTH4wEDwriEK'
                                                 'u31erZte71ejBbX0JqQ4gQt'
                                                 'ESXTyluW5fF4iJy4iKbxYK1'
                                                 'AfjQR0sEkITnBkLTE0/BGmG'
                                                 'Xdbtfr9fZ6vT0iDg8BnZDHi'
                                                 'AWEzNc0rdvtgkohWkF7YH+y'
                                                 'ojAMYmcaM1EspAqtcK/Xo9m'
                                                 'RxYCXgkqJDrlQ5fKk0+k4jo'
                                                 'ONAJHgIe12G88kncL5CEqHC'
                                                 'z3ir16vR69zuVyYNb9dMKfU'
                                                 'kUqKD55rhz3rQHIJRAK5hMl'}

    # Initiate a blank string.
    def setUp(self):
        self.testString = ""

    # Setup for individual data
    def get_file_path(self, structData):

        # Open the necessary file.
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "data",
                                structData["Name"] + "_test")
        return(fileName)

    # Test to see if the software name has been recorded correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default, ex_spm_conjunction, fsl_con_f_multiple)
    def test_software_name(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # Check for the software name.
        for line in postStatsFile:

            if "FMRI" in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the software name is what we expected.
        self.assertIn(structData["softwareName"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to see if the software version has been recorded correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default, ex_spm_conjunction, fsl_con_f_multiple)
    def test_software_num(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # Check for the software version.
        for line in postStatsFile:

            if "Version" in line:

                self.testString = line
                break

        # Verify the software version is what we expected.
        self.assertIn(structData["version"], line,
                      msg='Test failed on ' + structData["Name"])

        # Close the file
        postStatsFile.close()

    # Test to see if the height threshold has been recorded correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default)
    def test_height_threshold(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        for line in postStatsFile:

            if "statistic images were thresholded" in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the height threshold is what we expected.
        self.assertIn(structData["hThresh"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to see if the extent threshold has been recorded correctly.
    @data(fsl_thr_clustfwep05)
    def test_extent_threshold(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # Check for the extent threshold.
        for line in postStatsFile:

            if "statistic images were thresholded using clusters " \
                       "determined by" in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the extent threshold is what we expected.
        self.assertIn(structData["eThresh"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the slice image had been embedded correctly
    @data(fsl_thr_clustfwep05, ex_spm_contrast_mask, ex_spm_conjunction)
    def test_slice_image_extract(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")
        nextLine = False

        # Check for the slice image.
        for line in postStatsFile:

            if nextLine:

                self.testString = line
                break

            # If we see this the next line contains the slice image.
            if "<a href = './cluster_z" in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertIn(structData["sliceImExtract"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the FSL logo had been embedded correctly.
    @data(fsl_con_f, ex_spm_default, ex_spm_conjunction)
    def test_logo(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # This is an extract of the encoding for the FSL logo
        logoExtract = 'WriWP7OC0Zy6j7w4yMeoqnKL9NPivby0uILm1ZSwKEFh0N' \
                      'PvrlodWs7iI7DP+7YnoR1Gf1ouFiBtOspXAjPB5UHncMdv' \
                      '8OtY+qeGVCuUTlefl5yPWtaSN0nu7KL76kXUJP8JJ6fnkG' \
                      'p5L+VYLK4CExSsFcbcjaQf60aMRzGh61deHtQWyuXZ7R8E' \
                      'Fuqg9x+ddddWCXMb3FtyCN4CnPNZF7ZC58RwW7IZYolLht' \
                      'ucjHTPfpVvS737Kiyw3J8iQbjC2CFB9OfpTQk7mX'

        # Check for the FSL logo.
        for line in postStatsFile:

            # If we see this the next line contains the logo.
            if '<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki">' in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the FSL logo contained the extract.
        self.assertIn(logoExtract, self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the lower slice value is given correctly correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default, ex_spm_conjunction)
    def test_lower_slice_val(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # This is an extract of the encoding for the colorbar
        colorBarExtract = 'P+6AP+yAP+qAP+oAP+gAP+eAP+WAP+MAP+EAP+CAP98AP9' \
                          '6AP9yAP9wAP9oAP9mAP9gAP9eAP9WAP9UAP9EAP9CAP86A' \
                          'P84AP8wAP8oAP8mAP8eAP8cAP8WAP8UAP8MAP8KAP/lAP/' \
                          'dAP/bAP/TAP/RAP/JAP/BAP+/AP+3AP+1AP+vAP+tAP+lA' \
                          'P+jAP+bAP+ZAP+TAP+RAP+JAP+HAP9/AP93AP91AP9tAP9' \
                          'rAP9jAP9bAP9ZAP9RAP9PAP9J'

        # Check for the FSL logo.
        for line in postStatsFile:

            # If we see this the next line contains the colorbar and limits.
            if colorBarExtract in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the FSL logo contained the extract.
        self.assertIn(structData["lowSliceVal"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the upper slice value is given correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default, ex_spm_conjunction)
    def test_upper_slice_val(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # This is an extract of the encoding for the colorbar
        colorBarExtract = 'P+6AP+yAP+qAP+oAP+gAP+eAP+WAP+MAP+EAP+CAP98AP9' \
                          '6AP9yAP9wAP9oAP9mAP9gAP9eAP9WAP9UAP9EAP9CAP86A' \
                          'P84AP8wAP8oAP8mAP8eAP8cAP8WAP8UAP8MAP8KAP/lAP/' \
                          'dAP/bAP/TAP/RAP/JAP/BAP+/AP+3AP+1AP+vAP+tAP+lA' \
                          'P+jAP+bAP+ZAP+TAP+RAP+JAP+HAP9/AP93AP91AP9tAP9' \
                          'rAP9jAP9bAP9ZAP9RAP9PAP9J'

        # Check for the FSL logo.
        for line in postStatsFile:

            # If we see this the next line contains the colorbar and limits.
            if colorBarExtract in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the FSL logo contained the extract.
        self.assertIn(structData["highSliceVal"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the contrast name is correctly in postStats.
    @data(fsl_thr_clustfwep05, ex_spm_contrast_mask)
    def test_contrast_name(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")
        nextLine = False

        # Check for the slice image.
        for line in postStatsFile:

            # We need this line.
            if nextLine:

                self.testString = line
                break

            # If we see this the next line contains the slice image.
            if "<h3>Thresholded Activation Images</h3>" in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertIn(structData["contrastName"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the contrast name is correctly in postStats in conjunction
    # datasets.
    @data(ex_spm_conjunction)
    def test_contrast_name_conjunction(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")
        nextLine = False

        # Check for the slice image.
        for line in postStatsFile:

            # We need this line.
            if nextLine:

                self.testString = line
                break

            # If we see this the next line contains the slice image.
            if "<h3>Thresholded Activation Images</h3>" in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertTrue(structData["contrastName"][0] in self.testString and
                        structData["contrastName"][1] in self.testString,
                        msg='Test failed on ' + structData["Name"])

    # Checks if the correct number of pages have been generated.
    @data(fsl_con_f, ex_spm_default, ex_spm_conjunction, fsl_gamma_basis,
          fsl_con_f_multiple)
    def test_multiple_page_gen(self, structData):

        # Setup
        filePath = self.get_file_path(structData)

        # Count the number of files in the cluster data directory.
        numExc = len([name for name in os.listdir(
            filePath) if os.path.isfile(os.path.join(filePath, name))])-4

        # Assert if the number of excursions is correct.
        self.assertTrue(numExc == structData["numExc"],
                        msg='Test failed on ' + structData["Name"])

    # Checks if the correct number of slice images have been generated.
    @data(fsl_con_f, ex_spm_default, ex_spm_conjunction, fsl_gamma_basis)
    def test_multiple_con_gen(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # Count the number of slice images.
        numSliceIm = 0
        for line in postStatsFile:

            if "<a href = './cluster_z" in line:

                numSliceIm = numSliceIm + 1

        # Close the file
        postStatsFile.close()

        # Assert if the number of slice images is correct.
        self.assertTrue(numSliceIm == structData["numExc"],
                        msg='Test failed on ' + structData["Name"])

    # Test to check the correct contrast name matches the correct slice image.
    @data(fsl_contrast_mask, fsl_gamma_basis, fsl_con_f_multiple)
    def test_matching_con_name(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        postStatsFile = open(os.path.join(
          filePath, 'report_poststats.html'), "r")

        # Look for the contrast name of interest.
        nextLine = False
        for line in postStatsFile:

            # If this is the line containing the slice image check for the
            # extract
            if nextLine:

                self.testString = line
                break

            # If this line contains the contrast name the next line is the
            # image.
            if structData['matchConName'] in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertIn(structData["matchSliceImExtract"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to check whether the design matrix is being displayed correctly.
    @data(fsl_con_f, ex_spm_default)
    def test_design_matrix(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        statsFile = open(os.path.join(filePath, 'report_stats.html'), "r")

        nextLine = False

        # Check for the design matrix.
        for line in statsFile:

            if nextLine:

                self.testString = line
                break

            # If we see this the next line contains the design matrix.
            if '<a href="DesignMatrix.csv">' in line:

                nextLine = True

        # Close the file
        statsFile.close()

        # Verify the slice image contained the extract.
        self.assertIn(structData["desMatExtract"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to check whether the contrast vectors are being written correctly.
    @data(ex_spm_conjunction, ex_spm_default)
    def test_con_vec_string(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        statsFile = open(os.path.join(filePath, 'report_stats.html'), "r")

        conPresent = [False]*len(structData['conVec'])

        # Look through each line.
        for line in statsFile:

            # Check if each contrast vector is in the line.
            for i in range(0, len(structData['conVec'])):

                conVec = structData['conVec'][i]

                # If the contrast vector is there, record that we've seen it.
                if conVec in line:

                    conPresent[i] = True

        statsFile.close()

        self.assertNotIn(False, conPresent,
                         msg='Test failed on ' + structData["Name"])

    # Test to check whether the cluster table statistics are being
    # displayed correctly.
    @data(ex_spm_default, fsl_default, fsl_group_wls, fsl_group_ols)
    def test_clusTable(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        clusFile = open(os.path.join(filePath,
                                     'cluster_zstat1_std.html'), "r")

        # Look through each line.
        for line in clusFile:

            if structData['clusTabExtract'] in line:

                self.testString = line
                break

        clusFile.close()

        # Verify the table contained the extract.
        self.assertIn(structData["clusTabExtract"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to check whether the peak table statistics are being
    # displayed correctly.
    @data(ex_spm_default, fsl_default, fsl_group_wls, fsl_group_ols)
    def test_peakTable(self, structData):

        # Setup
        filePath = self.get_file_path(structData)
        clusFile = open(os.path.join(filePath,
                                     'cluster_zstat1_std.html'), "r")

        # Look through each line.
        for line in clusFile:

            if structData['peakTabExtract'] in line:

                self.testString = line
                break

        clusFile.close()

        # Verify the table contained the extract.
        self.assertIn(structData["peakTabExtract"], self.testString,
                      msg='Test failed on ' + structData["Name"])


# ===============================================================================

if __name__ == "__main__":

    # Get path of script
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    dataDir = os.path.join(scriptPath, "data")

    if not os.path.isdir(dataDir):  # Data folder does not exist

        os.makedirs(dataDir)

    dataNames = ["fsl_con_f",
                 "fsl_thr_clustfwep05",
                 "fsl_contrast_mask",
                 "fsl_gamma_basis",
                 "fsl_con_f_multiple"
                 "ex_spm_contrast_mask",
                 "ex_spm_default",
                 "ex_spm_conjunction"]

    local = True

    for dataName in dataNames:  # Check if data is on local machine

        # Data not found on local machine
        if not os.path.isfile(os.path.join(dataDir, dataName + ".nidm.zip")):

            local = False
            break

    if not local:

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

    globData = os.path.join(dataDir, "*.zip")
    data = glob.glob(globData)  # Get names of all zip files in data folder

    for i in data:  # Loop over all zip files in data folder and create html

        viewer.main(i, i.replace(".nidm.zip", "") + "_test", overwrite=True)

    unittest.main()  # Tests
