from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_details, name='post_detail'),
    path('<int:post_id>/share/', views.share, name='share_post')
]
