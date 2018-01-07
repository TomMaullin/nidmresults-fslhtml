import os
import shutil
import sys
import rdflib
import zipfile
import glob
from dominate import document
from dominate.tags import p, a, h1, h2, h3, img, ul, li, hr, link, style, br
from dominate.util import raw
import errno
import time
from nidmviewerfsl.pageStyling import *
import math

def addQueryToList(query): #Adds the query results to a list 

	queryList = []
	for i in query:
		
		for j in i:
		
			queryList.append("%s" % j)
		
	return(queryList)

def printQuery(query): #Generic function for printing the results of a query - used for testing
	i = 0
	for row in query: 

	#STARTFOR
		i = i+1
		#if len(row) == 1:
			
		print("%s" % row)
		
		#elif len(row) == 2:
		
		#	print("%s, %s" % row)
		
		#elif len(row) == 3:
			
		#	print("%s, %s, %s" % row)
			
		#else:
			
		#	print("Error, not a suitable length")

	print('length: ' + str(i))
	#ENDFOR     

def checkFWEExtentThreshold(graph): #checks for FWE corrected extent threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

               SELECT ?x

               WHERE {{?x a nidm_ExtentThreshold: . ?x a obo_FWERadjustedpvalue: . ?x prov:value ?thresh . }

               FILTER(STR(?thresh) = '1'^^xsd:string)}"""
			   
	queryResult = graph.query(query)
		
	return(queryResult)

def checkFDRExtentThreshold(graph): #checks for FWE corrected extent threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>

               SELECT ?x

               WHERE {?x a nidm_ExtentThreshold: . ?x a obo_qvalue: .}"""
			   
	queryResult = graph.query(query)
		
	return(queryResult)

def returnExtentThreshold(graph): #checks for corrected extent threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>

               SELECT ?x

               WHERE {?y a nidm_Inference: . ?y prov:used ?x . ?x a nidm_ExtentThreshold: . }"""
			   
	queryResult = graph.query(query)
		
	return(queryResult)

def formatClusterStats(g, excName):

        clusterData = {}
        
        #---------------------------------------------------------------------------------------------------------
        #First we gather data for peaks table.
        #---------------------------------------------------------------------------------------------------------

        #We must include cluster p values in the query.
        peak_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
                       prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
                       prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
                       prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
                       prefix prov: <http://www.w3.org/ns/prov#>
                       prefix nidm_coordinateVector: <http://purl.org/nidash/nidm#NIDM_0000086>
                       prefix nidm_pValueUncorrected: <http://purl.org/nidash/nidm#NIDM_0000116> 
                       prefix nidm_pValueFWER: <http://purl.org/nidash/nidm#NIDM_0000115> 
                       prefix nidm_qValueFDR: <http://purl.org/nidash/nidm#NIDM_0000119>
                       
                       
                       SELECT ?peakStat ?clus_index ?loc

                       WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                               ?exc prov:atLocation ?conMap . ?clus nidm_clusterLabelID: ?clus_index .
                               ?peak prov:wasDerivedFrom ?clus . ?peak nidm_equivalentZStatistic: ?peakStat .
                               ?peak prov:atLocation ?locObj . ?locObj nidm_coordinateVector: ?loc .}

                       FILTER(STR(?conMap) = '""" + excName + """'^^xsd:string)}"""
                
        #Run the peak query
        peakQueryResult = g.query(peak_query)

        #Retrieve query results.
        clusterIndicesForPeaks = [int("%0.0s %s %0.0s" % row) for row in peakQueryResult]
        peakZstats = [float("%s %0.0s %0.0s" % row) for row in peakQueryResult]
        locations = ["%0.0s %0.0s %s" % row for row in peakQueryResult]

        #Obtain permutation used to sort the results in order of descending cluster index and then descending peak statistic size.
        peaksSortPermutation = sorted(range(len(clusterIndicesForPeaks)), reverse = True, key=lambda k: (-clusterIndicesForPeaks[k], peakZstats[k]))

        #Sort all peak data using this permutation.
        sortedPeaksZstatsArray = [peakZstats[i] for i in peaksSortPermutation]
        sortedClusIndicesForPeaks = [clusterIndicesForPeaks[i] for i in peaksSortPermutation]
        sortedPeakLocations = [locations[i] for i in peaksSortPermutation]

        clusterData['peakZstats'] = sortedPeaksZstatsArray
        clusterData['peakClusIndices'] = sortedClusIndicesForPeaks
        clusterData['peakLocations'] = sortedPeakLocations

        #---------------------------------------------------------------------------------------------------------
        #Second we gather data for cluster table.
        #---------------------------------------------------------------------------------------------------------


        if len(checkFWEExtentThreshold(g)) > 0:
                
                clus_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
                       prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
                       prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
                       prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
                       prefix prov: <http://www.w3.org/ns/prov#>
               
                       SELECT ?clus_index ?clus_size ?pVal

                       WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                               ?exc prov:atLocation ?conMap . ?clus a nidm_SupraThresholdCluster: .
                               ?clus nidm_clusterLabelID: ?clus_index . ?clus nidm_clusterSizeInVoxels: ?clus_size .
                               ?clus nidm_pValueFWER: ?pVal .}

                       FILTER(STR(?conMap) = '""" + excName + """'^^xsd:string)}"""
                
        elif len(checkFDRExtentThreshold(g)) > 0:
                
                clus_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
                       prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
                       prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
                       prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
                       prefix prov: <http://www.w3.org/ns/prov#>
               
                       SELECT ?clus_index ?clus_size ?pVal

                       WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                               ?exc prov:atLocation ?conMap . ?clus a nidm_SupraThresholdCluster: .
                               ?clus nidm_clusterLabelID: ?clus_index . ?clus nidm_clusterSizeInVoxels: ?clus_size .
                               ?clus nidm_qValueFDR: ?pVal .}

                       FILTER(STR(?conMap) = '""" + excName + """'^^xsd:string)}"""

        else:
                
                clus_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
                       prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
                       prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
                       prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
                       prefix prov: <http://www.w3.org/ns/prov#>
               
                       SELECT ?clus_index ?clus_size

                       WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                               ?exc prov:atLocation ?conMap . ?clus a nidm_SupraThresholdCluster: .
                               ?clus nidm_clusterLabelID: ?clus_index . ?clus nidm_clusterSizeInVoxels: ?clus_size . }

                       FILTER(STR(?conMap) = '""" + excName + """'^^xsd:string)}"""

        #A corrected cluster threshold has been applied so we should display cluster P values.
        if len(checkFWEExtentThreshold(g)) > 0 or len(checkFDRExtentThreshold(g)) > 0:
                
                #Run the cluster query
                clusQueryResult = g.query(clus_query)

                #Retrieve query results.
                clusterIndices = [int("%s %0.0s %0.0s" % row) for row in clusQueryResult]
                clusterSizes = [int("%0.0s %s %0.0s" % row) for row in clusQueryResult]
                clusterPVals = ["%0.0s %0.0s %s" % row for row in clusQueryResult]

                #Remove any spaces from P vals
                clusterPVals = [float(pval.replace(" ", "")) for pval in clusterPVals]

                #Create an array for the highest peaks.
                highestPeakZArray = [0]*len(clusterIndices)
                highestPeakLocations = [0]*len(clusterIndices)
                for i in list(range(0, len(peakZstats))):
                        if highestPeakZArray[clusterIndicesForPeaks[i]-1] < peakZstats[i]:
                                highestPeakZArray[clusterIndicesForPeaks[i]-1] = peakZstats[i]
                                highestPeakLocations[clusterIndicesForPeaks[i]-1] = locations[i]

                #Obtain permutation used to sort the results in order of descending cluster index and then for each cluster by peak statistic size.
                clusterSortPermutation = sorted(range(len(clusterIndices)), reverse = True, key=lambda k: clusterSizes[k])

                #Sorted cluster arrays
                sortedClusSizeArray = [clusterSizes[i] for i in clusterSortPermutation]
                sortedClusIndicesArray = [clusterIndices[i] for i in clusterSortPermutation]
                sortedClusPVals = [clusterPVals[i] for i in clusterSortPermutation]

                #Sort the highest peaks
                sortedMaxPeakZstats = [highestPeakZArray[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]
                sortedMaxPeakLocations = [highestPeakLocations[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]

                #Deal with inf issues.
                logClusPVals = [0]*len(sortedClusPVals)
                for i in list(range(0, len(sortedClusPVals))):
                        if sortedClusPVals[i] == 0:
                                logClusPVals[i] = math.inf
                        else:
                                logClusPVals[i] = -math.log(sortedClusPVals[i], 10)
                                
                clusterData['clusterPValues'] = sortedClusPVals
                clusterData['logClusterPValues'] = logClusPVals
                
        else:
                #Run the cluster query
                clusQueryResult = g.query(clus_query)

                #Retrieve query results.
                clusterIndices = [int("%s %0.0s" % row) for row in clusQueryResult]
                clusterSizes = [int("%0.0s %s" % row) for row in clusQueryResult]

                #Create an array for the highest peaks.
                highestPeakZArray = [0]*len(clusterIndices)
                highestPeakLocations = [0]*len(clusterIndices)
                for i in list(range(0, len(peakZstats))):
                        if highestPeakZArray[clusterIndicesForPeaks[i]-1] < peakZstats[i]:
                                highestPeakZArray[clusterIndicesForPeaks[i]-1] = peakZstats[i]
                                highestPeakLocations[clusterIndicesForPeaks[i]-1] = locations[i]

                #Obtain permutation used to sort the results in order of descending cluster index and then for each cluster by peak statistic size.
                clusterSortPermutation = sorted(range(len(clusterIndices)), reverse = True, key=lambda k: clusterSizes[k])

                #Sorted cluster arrays
                sortedClusSizeArray = [clusterSizes[i] for i in clusterSortPermutation]
                sortedClusIndicesArray = [clusterIndices[i] for i in clusterSortPermutation]

                #Sort the highest peaks
                sortedMaxPeakZstats = [highestPeakZArray[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]
                sortedMaxPeakLocations = [highestPeakLocations[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]

        clusterData['clusSizes'] = sortedClusSizeArray
        clusterData['clusIndices'] = sortedClusIndicesArray
        clusterData['clusPeakZstats'] = sortedMaxPeakZstats
        clusterData['clusPeakLocations'] = sortedMaxPeakLocations

        print(clusterData)
        
        return(clusterData)

def generateExcPage(outdir, excName, conData):

        #Create new document.
        excPage = document(title="Cluster List") #Creates initial HTML page
        with excPage.head:
                style(raw(getRawCSS()))
        excPage += raw("<center>")
        excPage += hr()
        excPage += raw("Co-ordinate information for " + excName + " - ")
        excPage += raw("<a href='../main.html'>back</a>")
        excPage += raw(" to main page")
        excPage += hr()

        #Cluster statistics section.
        excPage += h1("Cluster List")

        #Work out if we have cluster p value data.
        pDataAvailable = 'clusterPValues' in conData
        

        #Make the cluster statistics table.
        excPage += raw("<table cellspacing='3' border='3'><tbody>")

        #If we have pvalues for clusters include them.
        if pDataAvailable:
                excPage += raw("<tr><th>Cluster Index</th><th>Voxels</th><th>P</th><th>-log10(P)</th><th>Z-MAX</th><th>Z-MAX X (mm)</th><th>Z-MAX Y (mm)</th><th>Z-MAX Z (mm)</th></tr>")
        else:
                excPage += raw("<tr><th>Cluster Index</th><th>Voxels</th><th>Z-MAX</th><th>Z-MAX X (mm)</th><th>Z-MAX Y (mm)</th><th>Z-MAX Z (mm)</th></tr>")
        
        #Add the cluster statistics data into the table.
        for cluster in range(0, len(conData['clusSizes'])):
                #New row
                excPage += raw("<tr>")
                excPage += raw("<td>" + str(conData['clusIndices'][cluster]) + "</td>")
                excPage += raw("<td>" + str(conData['clusSizes'][cluster]) + "</td>")
                
                #If cluster p data is available
                if pDataAvailable:
                        excPage += raw("<td>" + ("%.4g" % conData['clusterPValues'][cluster]) + "</td>")
                        excPage += raw("<td>" + ("%.4f" % conData['logClusterPValues'][cluster]) + "</td>")
                
                excPage += raw("<td>" + str(float('%.2f' % float(conData['clusPeakZstats'][cluster]))) + "</td>")

                #Peak location
                formattedLoc = conData['clusPeakLocations'][cluster].replace(" ", "").replace("[", "").replace("]","").split(",")
                excPage += raw("<td>" + str(formattedLoc[0]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[1]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[2]) + "</td>")
                excPage += raw("</tr>")

        #Close table
        excPage += raw("</tbody></table>")

        excPage += br()
        excPage += br()
        excPage += h1("Local Maxima")
        
        #Make the peak statistics table.
        excPage += raw("<table cellspacing='3' border='3'><tbody>")
        excPage += raw("<tr><th>Cluster Index</th><th>Z-MAX</th><th>Z-MAX X (mm)</th><th>Z-MAX Y (mm)</th><th>Z-MAX Z (mm)</th></tr>")

        #Add the peak statistics data into the table.
        for peak in range(0, len(conData['peakZstats'])):
                #New row
                excPage += raw("<tr>")
                excPage += raw("<td>" + str(conData['peakClusIndices'][peak]) + "</td>")
                excPage += raw("<td>" + str(float('%.2f' % float(conData['peakZstats'][peak]))) + "</td>")

                #Peak location
                formattedLoc = conData['peakLocations'][peak].replace(" ", "").replace("[", "").replace("]","").split(",")
                excPage += raw("<td>" + str(formattedLoc[0]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[1]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[2]) + "</td>")
                excPage += raw("</tr>")

        #Close table
        excPage += raw("</tbody></table>")
        
        excPage += raw("</center>")
        excFile = open(os.path.join(outdir, excName + ".html"), "x")
        print(excPage, file = excFile) #Prints html page to a file
        excFile.close()

def queryExcursionSetNifti(graph): #Selects excursoion set NIFTI URI

        query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
			   prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ConjunctionInference: <http://purl.org/nidash/nidm#NIDM_0000011>
               prefix spm_PartialConjunctionInference: <http://purl.org/nidash/spm#SPM_0000005>
			   prefix dc: <http://purl.org/dc/elements/1.1/>
			   prefix nidm_ConjunctionInference: <http://purl.org/nidash/nidm#NIDM_0000011>
			   prefix spm_PartialConjunctionInference: <http://purl.org/nidash/spm#SPM_0000005>
               SELECT ?image

               WHERE {{?x a nidm_Inference:} UNION {?x a nidm_ConjunctionInference:} UNION {?x a spm_PartialConjunctionInference:}.
                       ?y prov:wasGeneratedBy ?x . ?y a nidm_ExcursionSetMap: . ?y prov:atLocation ?image}"""

        queryResult = graph.query(query)
        return(addQueryToList(queryResult))

#This function generates all pages for display.
def pageGenerate(g, outdir):

        print(outdir)

	#Make cluster pages
	os.mkdir(os.path.join(outdir, 'Cluster_Data'))
	excNiftiNames = queryExcursionSetNifti(g)

	for row in excNiftiNames:
	
		excName = "%s" % row
		excData = formatClusterStats(g, excName)
		generateExcPage(os.path.join(outdir, 'Cluster_Data'), excName.replace(".nii.gz", ""), excData)


##################################################################################################################################################
shutil.rmtree('/home/tom/Documents/Cluster_Data')
outdir = '/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/ex_spm_thr_clustfwep05_test/'
#os.mkdir(os.path.join(outdir, 'Cluster_Data'))
#t = time.time()
g = rdflib.Graph()
turtleFile = glob.glob(os.path.join(outdir, 'nidm.ttl'))
#turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/ex_spm_partial_conjunction_test/nidm.ttl')
g.parse(turtleFile[0], format = "turtle")
##################################################################################################################################################

#excNiftiNames = queryExcursionSetNifti(g)
#
#for row in excNiftiNames:
#        excName = "%s" % row
#        excData = formatClusterStats(g, excName)
#        generateExcPage(os.path.join(outdir, 'Cluster_Data'), excName.replace(".nii.gz", ""), excData)

printQuery(returnExtentThreshold(g))
pageGenerate(g, '/home/tom/Documents')
#t2 = time.time() - t
#print(t2)
