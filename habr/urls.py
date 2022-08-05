from django.urls import path
from django.views.decorators.cache import cache_page

from habr.views import PostListView


urlpatterns = [
    path('get_posts/', cache_page(5)(PostListView.as_view()))
]