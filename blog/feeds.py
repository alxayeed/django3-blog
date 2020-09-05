from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = "Al's Blog"
    link = reverse_lazy('blog:list')
    description = 'New Post of my blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body
