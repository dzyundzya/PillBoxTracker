from django.contrib.auth import get_user_model
from rest_framework import serializers

from pillbox.models import (
    ActiveSubstance, Category, Comment, Pill, Manufacturer, MedicineForm
)

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'created_at')


class ActiveSubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveSubstance
        fields = ('id', 'name', 'slug')


class ManufacturerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name', 'slug', 'country',)


class MedicineFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineForm
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'slug', 'is_published')


class CreatePillSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    active_substance = serializers.SlugRelatedField(
        slug_field='slug', queryset=ActiveSubstance.objects.all(),
        many=True
    )
    manufacturer = serializers.SlugRelatedField(
        slug_field='name', queryset=Manufacturer.objects.all()
    )
    medicine_form = serializers.SlugRelatedField(
        slug_field='slug', queryset=MedicineForm.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Pill
        fields = (
            'id', 'name', 'description', 'author', 'pub_date',
            'manufacturer', 'medicine_form', 'active_substance',
            'category', 'is_published',
        )


class ReadPillSerializer(serializers.ModelSerializer):
    active_substance = ActiveSubstanceSerializer(many=True, read_only=True)
    manufacturer = ManufacturerSerializers(read_only=True)
    medicine_form = MedicineFormSerializer(read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='slug', read_only=True
    )

    class Meta:
        model = Pill
        fields = (
            'id', 'name', 'description', 'manufacturer',
            'medicine_form', 'active_substance', 'category',
        )
