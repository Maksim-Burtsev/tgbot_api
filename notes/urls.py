from django.urls import include, path

from rest_framework import routers

from notes.views import NoteViewSet


router = routers.SimpleRouter()
router.register("", NoteViewSet, basename="notes")

urlpatterns = [
    path("", include(router.urls)),
]
