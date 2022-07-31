from django_filters import rest_framework as filters

from notes.models import Note


class NoteFilter(filters.FilterSet):
    class Meta:
        model = Note
        fields = ("category",)
