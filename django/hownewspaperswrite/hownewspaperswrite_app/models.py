from django.db import models

# Create your models here.
class Created(models.Model):
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        app_label = "hownewspaperswrite_app"
        abstract = True

class Site(Created):
    url = models.URLField(db_index=True, unique = True, null=False, blank=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.CharField(max_length=150, blank=True)
    language = models.CharField(max_length= 70, default = 'eng')
    

    def __unicode__(self):
        if self.title is None:
            return "None"
        else:
            return self.title

    
    def __unicode__(self):
        s = ""
        if self.description is None:
            s = "None"
        else:
            s = self.description
        return s
    
    class Meta:
        app_label = "hownewspaperswrite_app"
        ordering = ('title',)
     
class LinksInPost(models.Manager):
    """Returns Locations from items"""
    def get_query_set(self):
        return super(LinksInPost, self).get_query_set().filter(links)

    def __unicode__(self):
        return self.links
   
class MostCommonWords(models.Manager):
    """Returns Locations from items"""
    def get_query_set(self):
        return super(MostCommonWords, self).get_query_set().filter(tipo= 'MOSTCOMMONWORD')

    def __unicode__(self):
        return self.word

    def delete_everything(self):
        PostItem.objects.all().delete()

class PostItem(Created):
    word = models.CharField(max_length=200, db_index = True)
    numeric = models.PositiveIntegerField(default = 0)
    tipo = models.CharField(max_length=200)
    testata = models.ForeignKey(Site)
    testata_nome = models.CharField(max_length = 200, blank = False, null = False)
    url_articolo = models.URLField(db_index=True)
    most_common = MostCommonWords()
    objects = models.Manager()
    
    def __unicode__(self):
        return self.word

    class Meta:
        #ordering = ('name','date','occurrences',)
        app_label = "hownewspaperswrite_app"
        ordering = ('-numeric','word','created_at',)
        unique_together = ("word", "testata_nome")
    
    
class SitePost(Created):
    links = models.ManyToManyField(PostItem)
    testata = models.ForeignKey(Site)
    testo = models.TextField(blank=True, db_index=True)
    titolo = models.CharField(max_length=200)
    url_articolo = models.URLField(db_index=True, unique = True)

#class IterationsIndex(Created):
 #   top_words = models.ManyToManyField(PostItem)
  #  total_words = models.PositiveIntegerField(default = 0)
   # articles_scanned = models.ManyToManyField(SitePost)

    
