from rest_framework import viewsets

from pillbox.models import ActiveSubstance, Category, Pill, Manufacturer, MedicineForm
from .mixins import ListCreateDestroyMixin
from .permissions import IsAdmiOrReadOnly
from .serializers import (
    ActiveSubstanceSerializer ,CategorySerializer, CreatePillSerializer, ReadPillSerializer,
    ManufacturerSerializers, MedicineFormSerializer,
)


class ActiveSubstanceViewSet(viewsets.ModelViewSet):
    queryset = ActiveSubstance.objects.all()
    serializer_class = ActiveSubstanceSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializers
    http_method_names = ['get', 'post', 'patch', 'delete']


class MedicineFormViewSet(viewsets.ModelViewSet):
    queryset = MedicineForm.objects.all()
    serializer_class = MedicineFormSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_published=True)
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class PillViewSet(viewsets.ModelViewSet):
    queryset = Pill.objects.filter(is_published=True)
    permission_classes = (IsAdmiOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return CreatePillSerializer
        return ReadPillSerializer
