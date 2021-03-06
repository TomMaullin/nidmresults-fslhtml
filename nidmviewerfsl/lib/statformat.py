#!/usr/bin/env python3
# ======================================================================
#
# This file contains functions used for formatting statistical data
# returned by SPARQL queries on NIDM-Results packs.
#
# Authors: Peter Williams, Tom Maullin, Camille Maumet (10/01/18)
#
# ======================================================================
from queries.querytools import run_query
from style.pagestyling import encode_image
import numpy as np
import random
import os
import math
import matplotlib
matplotlib.use('Agg')


# This function converts obo statistic types into the corresponding statistic.
def statistic_type(stat):

    if stat == "http://purl.obolibrary.org/obo/STATO_0000376":

        return("Z")

    elif stat == "http://purl.obolibrary.org/obo/STATO_0000282":

        return("F")

    elif stat == "http://purl.obolibrary.org/obo/STATO_0000176":

        return("T")

    else:

        return("P")


# This function returns the cluster forming threshold type of an image.
def height_thresh_type(graph, imageType):

    if run_query(graph, 'askIfOboStatistic', 'Ask'):

        return(imageType)

    else:

        return("P")


# This function returns the statistic type of a statistic
def statistic_type_string(statImage):

    if statImage == "T":

        return("T")

    elif statImage == "F":

        return("F")

    elif statImage == "Z":

        return("Z (Gaussianised T/F)")


def format_cluster_stats(g, excName):

    # ----------------------------------------------------------------------
    # First we gather data for peaks table.
    # ----------------------------------------------------------------------

    # Run the peak query
    peakQueryResult = run_query(g, 'selectPeakData', 'Select',
                                {'EXC_NAME': excName})

    # Retrieve query results.

    peakZstats = [float(peakQueryResult[i]) for i in list(range(0, len(
                                                    peakQueryResult), 5))]
    clusterIndicesForPeaks = [int(peakQueryResult[i]) for i in list(range(
                                             1, len(peakQueryResult), 5))]
    locations = [peakQueryResult[i] for i in list(range(2, len(
                                                    peakQueryResult), 5))]

    # If a corrected height threshold has been applied we should display
    # corrected peak P values. Else we should use uncorrected peak P values.
    try:
        if run_query(g, 'askCHeightThreshold', 'Ask'):

            peakPVals = [float(peakQueryResult[i]) for i in list(
                                        range(3, len(peakQueryResult), 5))]

        else:

            peakPVals = [float(peakQueryResult[i]) for i in list(
                                        range(4, len(peakQueryResult), 5))]

    # This is a temporary bug fix due to the FSL exporter currently not
    # recording corrected peak P-values.
    except ValueError:

        peakPVals = [math.nan for row in peakQueryResult]

    # Obtain permutation used to sort the results in order of descending
    # cluster index and then descending peak statistic size.
    peaksSortPermutation = sorted(range(len(clusterIndicesForPeaks)),
                                  reverse=True,
                                  key=lambda k: (clusterIndicesForPeaks[k],
                                                 peakZstats[k]))

    # Sort all peak data using this permutation.
    sortedPeaksZstatsArray = [peakZstats[i] for i in peaksSortPermutation]
    sortedClusIndicesForPeaks = [
        clusterIndicesForPeaks[i] for i in peaksSortPermutation]
    sortedPeakLocations = [locations[i] for i in peaksSortPermutation]
    sortedPeakPVals = [peakPVals[i] for i in peaksSortPermutation]

    # ----------------------------------------------------------------------
    # Second we gather data for cluster table.
    # ----------------------------------------------------------------------

    # Run the cluster query
    clusQueryResult = run_query(g, 'selectClusterData', 'Select',
                                {'EXC_NAME': excName})

    clusterIndices = [
        int(clusQueryResult[i]) for i in list(
            range(0, len(clusQueryResult), 3))]
    clusterSizes = [
        int(clusQueryResult[i]) for i in list(
            range(1, len(clusQueryResult), 3))]
    clusterPVals = [
        float(clusQueryResult[i]) for i in list(
            range(2, len(clusQueryResult), 3))]

    # Create an array for the highest peaks.
    highestPeakZArray = [0]*len(clusterIndices)
    highestPeakLocations = [0]*len(clusterIndices)
    for i in list(range(0, len(peakZstats))):
        if highestPeakZArray[clusterIndicesForPeaks[i]-1] < peakZstats[i]:
            highestPeakZArray[clusterIndicesForPeaks[i]-1] = peakZstats[i]
            highestPeakLocations[clusterIndicesForPeaks[i]-1] = locations[i]

    # Obtain permutation used to sort the results in order of descending
    # cluster index and then for each cluster by peak statistic size.
    clusterSortPermutation = sorted(
        range(len(clusterIndices)),
        reverse=True,
        key=lambda k: (clusterSizes[k], clusterIndices[k]))

    # Sorted cluster arrays
    sortedClusSizeArray = [
        clusterSizes[i] for i in clusterSortPermutation]
    sortedClusIndicesArray = [
        clusterIndices[i] for i in clusterSortPermutation]
    sortedClusPVals = [
        clusterPVals[i] for i in clusterSortPermutation]

    # Sort the highest peaks
    sortedMaxPeakZstats = [
        highestPeakZArray[
            sortedClusIndicesArray[i]-1] for i in list(
                range(0, len(clusterIndices)))]
    sortedMaxPeakLocations = [
        highestPeakLocations[
            sortedClusIndicesArray[i]-1] for i in list(
                range(0, len(clusterIndices)))]

    # Deal with inf issues for peaks.
    logPeakPVals = [0]*len(sortedPeakPVals)
    for i in list(range(0, len(sortedPeakPVals))):
        if sortedPeakPVals[i] == 0:
            logPeakPVals[i] = math.inf
        else:
            logPeakPVals[i] = -math.log(sortedPeakPVals[i], 10)

    # Deal with inf issues for clusters.
    logClusPVals = [0]*len(sortedClusPVals)
    for i in list(range(0, len(sortedClusPVals))):
        if sortedClusPVals[i] == 0:
            logClusPVals[i] = math.inf
        else:
            logClusPVals[i] = -math.log(sortedClusPVals[i], 10)

    # Record the data for display.
    clusterData = {}

    # If a corrected cluster threshold has been applied we should display
    # cluster P values.
    if run_query(g, 'askCExtentThreshold', 'Ask'):

        clusterData['clusterPValues'] = sortedClusPVals
        clusterData['logClusterPValues'] = logClusPVals

    clusterData['clusSizes'] = sortedClusSizeArray
    clusterData['clusIndices'] = sortedClusIndicesArray
    clusterData['clusPeakZstats'] = sortedMaxPeakZstats
    clusterData['clusPeakLocations'] = sortedMaxPeakLocations
    clusterData['peakZstats'] = sortedPeaksZstatsArray
    clusterData['peakClusIndices'] = sortedClusIndicesForPeaks
    clusterData['peakLocations'] = sortedPeakLocations
    clusterData['peakPVals'] = sortedPeakPVals
    clusterData['logPeakPVals'] = logPeakPVals

    return(clusterData)


def contrast_vec(data, v_min, v_max):

    # This import is needed only in this function.
    from matplotlib import pyplot as plt

    conLength = len(data)

    # We invert the values so the colours appear correctly (i.
    # e. 1 -> white, 0 -> black).
    data = np.ones(len(data))-data

    # Make the contrast vector larger so we can make an image.
    data = np.kron(data, np.ones((10, 30)))

    # Add border to data.
    data[:, 0] = v_max*np.ones(10)
    data[:, 30*conLength-1] = v_max*np.ones(10)
    data[0, :] = v_max*np.ones(30*conLength)
    data[10-1, :] = v_max*np.ones(30*conLength)

    # Create figure.
    fig = plt.figure(figsize=(len(data), 1))

    # Remove axis
    ax = fig.add_subplot(1, 1, 1)
    plt.axis('off')

    # Add contrast vector to figure
    plt.imshow(data, aspect='auto', cmap='Greys', vmin=v_min, vmax=v_max)

    # Check for bording box.
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    # Save figure (without bording box)
    tempFile = 'tempCon' + str(random.randint(0, 999999)) + '.png'
    plt.savefig(tempFile, bbox_inches=extent)

    # Encode the figure.
    encodedIm = encode_image(tempFile)

    # Remove the image.
    os.remove(tempFile)

    # Return the image
    return('data:image/jpg;base64,' + encodedIm.decode())


# This function takes in an excursion set name and a graph and generates
# an FSL-like name for the HTML output display for the excursionset.
#
# e.g. ExcursionSet_F001.nii.gz -> cluster_zfstat1_std.html
def get_clus_filename(g, excName):

    # For SPM data we can't work out the filename we want from just
    # the contrast name.
    if run_query(g, 'askSPM', 'Ask'):

        # For SPM data we must look for the statistic map to
        # assert which statistic is associated to a contrast.
        statisticMap = run_query(g, 'selectStatMap', 'Select',
                                 {'EXC_NAME': (excName + '.nii.gz')})[0]

        # If it's T stat string is '', if it's F stat string
        # is 'f'
        if statisticMap[0] == 'T':
            statString = ''
        else:
            statString = statisticMap[0].lower()

        return('cluster_z' + statString + 'stat1_std.html')

    else:

        # In FSL the excursion set maps are always of the form
        # ExcursionSet_(stattype)00(number), unless only one T
        # statistic was computed. Then the excursion set map is
        # named ExcursionSet.
        if '_F' in excName:

            statString = 'f'

        else:

            statString = ''

        # The last letter of the name should either be the
        # excursion number or, if there is only one excursion
        # set, 't'.
        number = excName.replace('.nii.gz', '')[-1]

        if number == 't':

            number = '1'

        return('cluster_z' + statString + 'stat' + number + '_std.html')
