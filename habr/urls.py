from django.urls import path

from habr.views import PostListView


urlpatterns = [
    path('get_posts/', PostListView.as_view())
]