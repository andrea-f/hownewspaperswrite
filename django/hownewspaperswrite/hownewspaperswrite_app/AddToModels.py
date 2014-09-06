import os, sys
lib = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','hownewspaperswrite'))
sys.path.append(lib)
from django.core.exceptions import ObjectDoesNotExist
from termcolor import colored


class SaveDataInDatabase:
    def __init__(self,):
        """"""

   

    def dropTable(request):
        from django.db import connection, transaction
        cursor = connection.cursor()
        try:
            cursor.execute("DROP TABLE 'hownewspaperswrite_app_postitem';")
        except Exception as e:
            print "Error in dropping app_postitem table %s " % e
        try:

            cursor.execute("DROP TABLE 'hownewspaperswrite_app_postitem_testate';")
        except Exception as e:
            print "Error in dropping table of items: %s" % e




    def resetItemsFreqDist(self):
        """Resets items freq dist to zero for rebasing."""
        from models import PostItem

        results = PostItem.most_common.delete_everything()
        #results = PostItem.objects.all().delete()
        print "Resetting %s items..." % results.count()
        return
        updated = 0
        for res in results:
            if res.numeric != 0:
                print "Resetting: %s # %s" % (res.word, updated)
                res.numeric = 0
                res.save()
                updated += 1
        return updated


    def addSite(self, testate = "", url = "", thumbnail = "", description = "", language = 'eng'):
        """Creates site information."""
        from models import Site
        if len(url) == 0:
            raise Exception("No url")
        try:
            r = Site.objects.create(title=testate, url=url, thumbnail = thumbnail, description = description, language = language)
            createdSite = True
        except:
            r = Site.objects.get(url=url)
            createdSite = False
        print "AddSite: Site was created? %s" % createdSite
        return r

    def addSitePost(self, site, testo, url_articolo, links, titolo = ""):
        """Save in database all events contained in a file.

        :param listOfEvents:
            List of event objects to save in DB.

        Return int with total saved videos in database.

        """
        from models import SitePost
        if len(titolo) == 0:
            titolo = url_articolo
        #print titolo
        try:
            v = SitePost.objects.get(url_articolo = url_articolo)
            created = False            
        except:
            v = SitePost.objects.create(
                testata = site,
                url_articolo = url_articolo,
                testo = testo,
                titolo = titolo
            )
            created = True
            
        
        tot = 0
        print "Created: %s | URL: %s" % (created, v.url_articolo)

        if created is True:
            links = [self.addPostItem(site,link,'LINK', url_articolo) for link in links if "http" in link and len(link)>3]
            for link in links:
                v.links.add(link)
                tot+=1
        print "AddSitePost: Url: %s | Created? %s | Links created: %s" % (v.url_articolo, created, tot)
        return created
        
        

    def addPostItem(self, site, word, tipo, parent_url = "", numeric = 0):
        """Add video to db

        :param video: Django video DB object containing title, description, url, thumb url ...

        Return two variables with:
            * **v** -- Created video object in database, dict.
            * **created** -- True if video is created, false if video is already present, bool.
        """
        from models import PostItem
        #if len(parent_url) != 0 and "http" in parent_url:
        #    word = parent_url
        
        try:
                v = PostItem.objects.get(word = word, testata_nome = site.title)
                #for testata in v.testate.all():
                #    if site.title not in testata.title:
                #        v.testate.add(site)

                print colored("Updating: %s | %s | %s | %s | %s" % (word,v.testata.title, tipo,v.numeric, numeric), "red")
                v.numeric = int(v.numeric)+int(numeric)                
        except ObjectDoesNotExist:
                v = PostItem.objects.create(
                    word = word,
                    tipo = tipo,
                    url_articolo = parent_url,
                    numeric = numeric,
                    testata = site,
                    testata_nome = site.title
                )
                #v.testate.add(site)
                print colored("Saving: %s | %s | %s | %s" % (word,site.title, tipo, numeric), "green")
        print colored("Final: %s | %s | %s | %s \n" % (word,site.title, tipo,v.numeric), "white")
        return v
        