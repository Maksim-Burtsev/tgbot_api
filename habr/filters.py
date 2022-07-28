from django_filters import rest_framework as filters


class PostsFilter(filters.FilterSet):
    category = filters.CharFilter()