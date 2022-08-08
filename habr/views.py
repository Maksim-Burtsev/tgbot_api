import logging

from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

from django_filters import rest_framework as filters

from habr.parser import Parser
from habr.parser import ParseDataError, ScrapingError
from habr.filters import PostsFilter
from habr.serializers import PostSerializer
from habr.logic import get_unseen_posts


logger = logging.getLogger(__name__)


class PostListView(views.APIView):

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostsFilter

    def get(self, request):

        category = request.query_params.get("category")

        parser = Parser()
        try:
            posts = parser.get_posts(category)
        except (ScrapingError, ParseDataError) as e:
            logger.warning(f"Problem with parser: {e}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            data = get_unseen_posts(posts)

        serializer = PostSerializer(data=data, many=True)
        serializer.is_valid()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
