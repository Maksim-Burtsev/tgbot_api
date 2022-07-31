from rest_framework import viewsets

from django_filters import rest_framework as filters

from notes.models import Note
from notes.serializers import NoteSerializer
from notes.filters import NoteFilter


class NoteViewSet(viewsets.ModelViewSet):
    """CRUD for Notes"""

    serializer_class = NoteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NoteFilter

    def get_queryset(self):
        return Note.objects.all()
