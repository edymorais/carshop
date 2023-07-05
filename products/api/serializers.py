from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response

from products.models import Product, ProductImages, ProductSpecifications, Specification


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecifications
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        images = self.initial_data.getlist('images')
        specifications_data = self.initial_data.getlist('specifications')

        with transaction.atomic():
            try:

                product = Product.objects.create(**validated_data)

                for image in images:
                    ProductImages.objects.create(product=product, foto=image)

                for spec_data in specifications_data:
                    spec = Specification.objects.get(pk=spec_data)
                    ProductSpecifications.objects.create(product=product, specification=spec)

                return product

            except ValueError as e:
                return e
            except Exception as e:
                return e


class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'type', 'brand', 'model', 'year', 'fabrication', 'version', 'color', 'is_new', 'fuel_type',
                  'exchange', 'distance_round', 'motor', 'observation', 'price_sale', 'price', 'images',
                  'specifications']

    def get_images(self, obj):
        product_images = []
        images = ProductImages.objects.filter(product=obj.id)
        for i in images:
            product_images.append(f'{i.foto}')

        return product_images

    def get_specifications(self, obj):
        product_specifications = []
        specifications = ProductSpecifications.objects.filter(product=obj.id)
        for spec in specifications:
            specification = {}
            specification['categorie'] = spec.specification.categories
            specification['name'] = spec.specification.name
            product_specifications.append(specification)

        return product_specifications


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'