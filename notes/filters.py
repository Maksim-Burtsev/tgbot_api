from django_filters import rest_framework as filters

from notes.models import Note


class NoteFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Note
        fields = ("category",)
