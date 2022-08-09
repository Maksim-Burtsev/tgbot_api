from rest_framework.viewsets import mixins, GenericViewSet

from django_filters import rest_framework as filters

from notes.models import Note
from notes.serializers import NoteSerializer
from notes.filters import NoteFilter


class NoteViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """CRD for Notes"""

    serializer_class = NoteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NoteFilter

    def get_queryset(self):
        return Note.objects.all()
