from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from pillbox.models import ActiveSubstance, Category, Pill, Manufacturer, MedicineForm
from .permissions import IsAdmiOrReadOnly
from .serializers import (
    ActiveSubstanceSerializer, CategorySerializer, CreatePillSerializer, CommentSerializer, ReadPillSerializer,
    ManufacturerSerializers, MedicineFormSerializer,
)


class PillCommonViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmiOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_pill(self):
        return get_object_or_404(Pill, id=self.kwargs.get('pill_id'))

    def get_queryset(self):
        return self.get_pill().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, pill=self.get_pill())


class ActiveSubstanceViewSet(PillCommonViewSet):
    queryset = ActiveSubstance.objects.all()
    serializer_class = ActiveSubstanceSerializer


class ManufacturerViewSet(PillCommonViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializers


class MedicineFormViewSet(PillCommonViewSet):
    queryset = MedicineForm.objects.all()
    serializer_class = MedicineFormSerializer


class CategoryViewSet(PillCommonViewSet):
    queryset = Category.objects.filter(is_published=True)
    serializer_class = CategorySerializer


class PillViewSet(PillCommonViewSet):
    queryset = Pill.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return CreatePillSerializer
        return ReadPillSerializer
