from django.contrib import admin

from models import Site, SitePost, PostItem

admin.site.register(Site)
admin.site.register(SitePost)
admin.site.register(PostItem)
