# Here I will define all the custom tags
from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

# a variable named register(register, nothing else),which is an instance of template.Library(),is used to register customer tags and filters
register = template.Library()


# simple_tag
# returns a string , the total number posts published
@register.simple_tag
def count_posts():
    total_posts = Post.published.count()
    return total_posts


# simple_tag
# instead of a simple list, now it is returning an iterable value, list of posts
@register.simple_tag
def most_commented_posts(count=5):
    return Post.published.annotate(most_commented=Count('comment')).order_by('-most_commented')[:count]


# @register.simple_tag
# def recent_posts(count=5):
#     return Post.published.all().order_by('-publish')[:count]

# Lets rebuilt the recent_posts() function as a inclusion_tag, it returns render html result (render(template, context))
@register.inclusion_tag('blog/post/recent_posts.html')  # a template
def recent_posts(count=5):
    recent_posts = Post.published.all().order_by('-updated')[:count]
    return {'recent_posts': recent_posts}  # a context


# CUSTOM FILTER to converts markdown text into normal text
@register.filter(name='blah')
def markdown_text(text):
    return mark_safe(markdown.markdown(text))
