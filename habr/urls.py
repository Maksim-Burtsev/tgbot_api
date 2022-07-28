from django.urls import path

from habr.views import PostListView


urlpatterns = [
    path('get_articles/', PostListView.as_view())
]