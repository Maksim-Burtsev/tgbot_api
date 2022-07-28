from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

from django_filters import rest_framework as filters

from habr.models import Post
from habr.parser import Parser
from habr.filters import PostsFilter


class PostListView(views.APIView):

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostsFilter

    def get(self, request):
        return Response([], status=status.HTTP_200_OK)