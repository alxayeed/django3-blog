from django.urls import path
from . import views
from.feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='list'),
    path('tag/<slug:tag_slug>', views.post_list, name='list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_details, name='post_detail'),
    path('<int:post_id>/share/', views.share, name='share_post'),
    path('feed/', LatestPostsFeed(), name='post_feed')
]
