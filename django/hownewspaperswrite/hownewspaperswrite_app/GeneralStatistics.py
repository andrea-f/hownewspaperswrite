import os, sys
lib = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(lib)
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

import operator
lib = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..', '..', 'bin', 'src', 'tools'))
sys.path.append(lib)
import Matrix
import TextOperations
import pprint
from Read import Read

class GeneralDataView(object):
    """This class formulates the response to the web query."""

    def __init__(self):
        #result = hasattr(DataManagement,req)()
        """"""
        self.dm = Read()

    def fetch(self, request):
        newspapers = self.dm.getTotalArticles()
        topused = self.dm.getMostCommonWordsTotal()
        total_words = self.dm.getTotalWordsInt()
        giornali = self.dm.getMostCommonWordsBySite()
        pprint.pprint(giornali)
        #for giornale in giornali:
        #    sys.stderr.write("Giornali:\n %s\n" % (giornale['testata']))
        sys.stderr.flush()

        sys.stderr.write("Fetched: %s" % (str(newspapers)))
        sys.stderr.flush()
        return render_to_response('statistics.html', locals(), RequestContext(request))

    



class DataOperations():
    """This class performs nlp analysis on data."""

    def __init__(self, abs_path = ""):
        """"""
        self.abs_path = abs_path
        self.matrix = Matrix.CreateMatrix(abs_path = abs_path)

    def saveMatrix(self, words = {}, abs_path = "", filename = "", min = 0.001, max = 10.0):
        """Generates and saves matrix file from wordlist dictionary of word and occurrences.

        :param words:
            holds "word":445, of all words in database,  dict.
        """
        if len(abs_path) == 0:
            abs_path = self.abs_path
        
        gmd = Read()
        #if len(words) == 0:
         #   words =
        #testate is dict of newspaper title and associated a dict with words and their frequency
        testate = gmd.getMostCommonWordsBySite(respType = "dict", include_percentage = False)
        print "Generating and saving matrix, calling Matrix()..."
        wordlist = self.matrix.saveMatrix(words, testate, abs_path, filename = filename, min = min, max = max)
        return wordlist

    def hierarchical_clustering(self, abs_path = "", filename = ""):
        """Creates clusters and dendrogram."""
        if len(abs_path) == 0:
            abs_path = self.abs_path
        fn = abs_path+"/"+filename
        print "Definig clusters for %s..." % fn
        dataDict = self.matrix.hierarchical_clustering(filename = fn)
        print "Drawing the dendrogram..."
        imgFile = self.matrix.draw_dendrogram(dataDict['clusters'], dataDict['titles'], jpeg = filename+".jpg")
        return imgFile

