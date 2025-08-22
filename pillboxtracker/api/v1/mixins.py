from rest_framework import mixins, viewsets

from .permissions import IsAdmiOrReadOnly


class ListCreateDestroyMixin(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = (IsAdmiOrReadOnly,)
    lookup_field = 'slug'
