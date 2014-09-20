import os, sys
lib = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','hownewspaperswrite'))
sys.path.append(lib)
from django.core.exceptions import ObjectDoesNotExist
from termcolor import colored


class SaveDataInDatabase:
    def __init__(self,):
        """"""

   

    def dropTable(request, table_name = "hownewspaperswrite_app_entity_items" ):
        #hownewspaperswrite_app_entity
        from django.db import connection, transaction
        cursor = connection.cursor()
        try:
            cursor.execute("DROP TABLE "+table_name+";")
        except Exception as e:
            print "Error in dropping app_postitem table %s " % e
        




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
        
    

    def addPostItem(self, site, word, tipo, parent_url = "", numeric = 0, tfidf = 0, stem = ""):
        """Add video to db

        :param video: Django video DB object containing title, description, url, thumb url ...

        Return two variables with:
            * **v** -- Created video object in database, dict.
            * **created** -- True if video is created, false if video is already present, bool.
        """
        from models import PostItem        
        try:
                v = PostItem.objects.get(word = word, testata_nome = site.title)
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
        if len(stem) > 0:
            v.stem = stem
        if tfidf > 0:
            #db specific hack
            v.tfidf = int(tfidf * 100000)
        print colored("Final: %s | %s | %s | %s | %s\n" % (word,site.title, tipo,v.numeric, v.stem), "white")
        return v

    def addEntity(self, nome= "", word = "", tipo = "", subtipo = "", value = 0, articles_ref = [], categoria = "cd ", add_items = True, add_articles = False):
        from models import Entity, PostItem, SitePost
        print colored("Saving %s from %s..." % (nome, word), "green")
        
        try:
            e = Entity.objects.get(name = nome)
        except ObjectDoesNotExist:
            e = Entity.objects.create(
                name = nome,
                tipo = tipo,
                subtipo = subtipo,
                category = categoria

            )

        if value != e.valore:
            e.valore = value
        if add_items is True:
            posts = PostItem.stems.filter(word__istartswith = word)
            c = 0
            for post in posts:
                c +=1
                e.items.add(post)
            print "Linked %s to %s items." % (nome, c)
        
        

        def saveArticle(e,articles):
            d = 0
            for article in articles:
                d +=1
                #TYPOOOOOOOOOOO
                e.aritcles.add(article)
                print "Linked %s to %s articles." % (nome,d)
                e.save()
                return e

        if add_articles is True:
            articles = SitePost.objects.filter(testo_icontains = word)
            e = saveArticle(e, articles)
        if len(articles_ref) > 0:
            e = saveArticle(e, articles_ref)

        print colored("Saved %s" % e.name, "yellow")
        return e
        

    def addArticlesToEntity(self, entity = {}):
        """Adds articles to entity."""
        from models import Entity, PostItem, SitePost
        if len(entity) == 0:
            entities = Entity.objects.all()
        else:
            entities = [entity]
        c = 0
        for ent in entities:
            print "Matching articles for %s..." % ent.name
            articles = SitePost.objects.filter(testo__icontains = ent.name)
            for article in articles:
                for ent_art in ent.aritcles.all():
                    if article.titolo not in ent_art.titolo:
                        ent.aritcles.add(article)
                        c += 1
                        ent.save()
            print "[AddToModels][addArticlesToEntity] Saved %s for %s " % (ent.aritcles.count(), ent.name)
        return {
            "entities": len(entities),
            "total_articles": len()
        }