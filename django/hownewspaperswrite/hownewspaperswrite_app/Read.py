import os,sys
from models import *
import operator
lib = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..', '..', 'bin', 'src', 'tools'))
sys.path.append(lib)
import TextOperations
from django.core.exceptions import ObjectDoesNotExist

from django.core.cache import cache

#get the cache key for storage
def cache_get_key(*args, **kwargs):
	import hashlib
	serialise = []
	for arg in args:
		serialise.append(str(arg))
	for key,arg in kwargs.items():
                serialise.append(str(key))
		serialise.append(str(arg))
	key = hashlib.md5("".join(serialise)).hexdigest()
	return key

#decorator for caching functions
def cache_for(time):
	def decorator(fn):
		def wrapper(*args, **kwargs):
			key = cache_get_key(fn.__name__, *args, **kwargs)
			result = cache.get(key)
			if not result:
				result = fn(*args, **kwargs)
				cache.set(key, result, time)
			return result
		return wrapper
	return decorator

class Read(object):
    """This class provides methods to access data in aggregated fashion, eventually it will be part of the api."""

    def __init__(self):
        """"""
        self.toolsText = TextOperations.TextOperations()

    #def getMostCommonWords(self, respType = "tuple"):
     #   """Returns most common words overall."""
      #  topused = {}
       # result = PostItem.objects.filter(tipo = 'MOSTCOMMONWORD')
       # topused['total'] = result.count()
        #res = result.order_by('word')

       # for item in result:
        #    num = result.filter(word=item.word).count()
         #   topused[item.word] = item.numeric

        #return self.convertToResponseType(data, respType)



    def convertToResponseType(self, data, respType = "tuple"):
        if "tuple" in respType:
            t = sorted(data.items(), key=lambda x:x[1], reverse = True)
            #t = sorted(data.items(), reverse = True)
            return t
        elif "dict" in respType:
            if isinstance(data, dict):
                return data
            else: raise
        else:
            return data

    def getMostCommonWordsTotal(self, respType = "tuple", filter = "", include_percentage = True):
        """Calculates most common words aggregated on all sites."""
        #import math
        topused = {}
        if len(filter) != 0:
            results = PostItem.most_common.filter(testata__title = filter)
        else:
            results = PostItem.most_common.all()
        total_words = self.getTotalWordsInt(testata = filter)
        topused['Words'] = total_words
        allWords = []

        for item in results:
            if item.word not in allWords:
                topused.setdefault(item.word,0)
                allWords.append(item.word)
            topused[item.word] += item.numeric  
                #sys.stderr.flush()
                #sys.stderr.write("Word: %s\nPerc word: %s\nWord: %s\nTotal words: %s\n" % ((item.word).encode('utf8'), str(num),str(item.numeric),str(total_words)))
        wordfreqpct = {}
        
        for key, value in topused.items():
            num = round(((float(value)/float(total_words))*100), 3)
            if include_percentage is True:
                wordfreqpct[key] = {"numeric": value, "percentage":num}
            else:
                wordfreqpct[key] = value
        return self.convertToResponseType(wordfreqpct, respType)
        #return wordfreqpct



    def getTotalArticles(self):
        """Returns total number of articles in database, divided by newspaper."""
        newspaper = {}
        newspaper['total'] = SitePost.objects.all().count()
        allSites = Site.objects.all()
        for site in allSites:
            newspaper[site.title] = SitePost.objects.filter(testata__url = site.url).count()
        return newspaper

    @cache_for(72000000000)
    def getTotalWordsInt(self, testata = ""):
        """Counts all the number of words by each article."""
        if len(testata) == 0:
            allArticles = SitePost.objects.all()
        else:
            allArticles = SitePost.objects.filter(testata__title = testata)
        totalWords = []
        for article in allArticles:
            totalWords += article.testo.split()
        totalWordsInt = len([word for word in totalWords if len(word)>4])
        return totalWordsInt




    def getWordsFreqBySite(self, add_percent_count = True):
        print "Fetching all words frequencies by site..."
        allSites = Site.objects.all()
        sites = {}
        for site in allSites:
            topused = {}
            total_words = self.getTotalWordsInt(testata = site.title)
            common = PostItem.most_common.filter(testata__title = site.title)
            for word in common:
                count = self.getWordFreqBySite(site, word)
                num = round(((float(count)/float(total_words))*100), 3)
                #sys.stderr.write("Type float %s\n" % (num))
                #sys.stderr.flush()
                #sys.stderr.write("Word: %s\nPerc word: %s\nWord: %s\nTotal words: %s\n" % ((item.word).encode('utf8'), str(num),str(item.numeric),str(total_words)))
                if add_percent_count is True:
                    topused[word] = {"numeric":count,"percentage": num}
                else:
                    topused[word] = count
            sites[site.title] = topused
        return sites

    def getWordFreqBySite(self, site, ref):
        print "Word count for %s" % site.title
        allArticles = SitePost.objects.filter(testata__title = site.title)
        num = 0
        for article in allArticles:
            words = article.testo.split()
            for word in words:
                if word in ref.word:
                    num += 1
        return num

    def getTotalWords(self, filter = ""):
        print "Fetching all words in articles..."
        if len(filter) == 0:
            allArticles = SitePost.objects.all()
        else:
            allArticles = SitePost.objects.filter(testata__title = filter)
        #allArticles = SitePost.objects.all()
        totale_articoli = []
        urls = []
        totalWordsNum = 0
        for article in allArticles:
            if article.url_articolo not in urls:
                totale_articoli.append((article.testata, article.testo))
                totalWordsNum += len(article.testo)
                urls.append(article.url_articolo)
                print "Processing %s with %s words..." % (article.url_articolo, len(article.testo))
        #totale_articoli is a list of tuples with testata object class and article text
        avg = str(float(totalWordsNum)/float(len(totale_articoli)))
        print "Total articles: %s Total words: %s with an average of %s per article" % (str(totalWordsNum), len(totale_articoli),avg)
        return totale_articoli

    def getAllWordsFrequency(self):
        """Return words with occurrences."""
        paroleTesto = {}
        totale = ""
        print "Calculating frequency distribution for all articles..."
        articoli = SitePost.objects.all()
        for articolo in articoli:
            totale += " "+articolo.testo
        paroleTesto = self.toolsText.getWordCount(totale)
        print "Calculated frequency distribution for %s articles." % len(articoli)
        return paroleTesto #allWords #, giornali

    def getReadyToSave(self, totale_articoli):
        giornali = []
        for articolo in totale_articoli:
            site = articolo[0]
            wordcount = self.toolsText.getWordCount(articolo[1])
            giornali.append((site, wordcount))
        return giornali

    def getAllTopWords(self, testata = ""):
        if len(testata) == 0:
            allArticles = SitePost.objects.all()
        else:
            allArticles = SitePost.objects.filter(testata__title = testata)
        #data = {}
        words = ""
        for article in allArticles:
            words += " "+article.testo#.split()
            #allWords +=words
        print "[Read.getAllTopWords] Counting all words..."
        wordcount = self.toolsText.getWordCount(words)
        #data["total"] = wordcount
        return wordcount

    def getTopWordsBySite(self):
        allSites = Site.objects.all()
        data = {}
        for site in allSites:
            wordcount = self.getAllTopWords(testata = site.title)
            data[site.title] = wordcount
        return data



    #def getTotalWordsByArticle(self):
    #    allArticles = SitePost.objects.all()
    #    data = {}
    #    for article in allArticles:
    #        words = article.testo.split()
    #        wc = {}
    #        for word in words:
    #            wc.setdefault(word, 0)
    #            wc[word] += 1
    #        data[article.testata.title] = wc
    #    return data

    def getTotalLinks(self):
        """Returns total links in database."""

    def getPost(self,url):
        """Retrieves site post by url."""
        try:
            post = SitePost.objects.get(url_articolo=url)
            return post
        except ObjectDoesNotExist:
            return False

###### FUNZIONI SPECIFICHE PER TESTATA #####

    def getMostCommonWordsBySite(self, respType = "tuple", include_percentage = True):
        """Retrieves most common words by site."""
        testate = Site.objects.all()
        giornali = {}
        for testata in testate:
            giornali[testata.title] = self.getMostCommonWordsTotal(filter = testata.title, respType = respType, include_percentage = include_percentage)
        return giornali



    def getSite(self,url = "", title = ""):
        """Retrieves site specific information."""
        if len(url) == 0 and len(title)==0:
            return
        if len(url) == 0:
            q = title
        else:
            q = url
        return Site.objects.get(title = q)

    def getAverageArticleLength(self, nome):
        """Gets the average article word length."""
        return {}


    def getMostForeignWordsBySite(self, nome):
        """Returns rank of website with most foreign words.
        Return
        [{
            "title": "La Repubblica",
            "percentage_foreign_words": 0.30,
            "most_used_foreign_words": ["hamburger","cheese","meeting"]
        }]
        """

