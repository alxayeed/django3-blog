from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSiteMap(Sitemap):
    # change frequency of every object returned by items(). values can be - 'always','hourly','daily','weekly','monthly','yearly','never'
    changefreq = 'weekly'

    # priority of every object returned by items. range 0.4-1.0, default 0.5
    priority = 0.9

    # returns sequence of QuerySet objects to lastmod(),location(),changefreq() etc
    def items(self):
        return Post.published.all()

    # return the datetime of the modificiation of the obj
    def lastmod(self, obj):
        return obj.updated
