from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from products.api.serializers import ProductSerializer, ProductImagesSerializer, ProductSpecificationsSerializer, \
    ProductListSerializer, SpecificationSerializer
from products.filters.filters import SpecificationFilter
from products.models import Product, ProductSpecifications, ProductImages, Specification
from itertools import groupby


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductListSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Atualizar imagens
            images_data = request.data.get('images')
            if images_data:
                for image_data in images_data:
                    image_id = image_data.get('id')
                    if image_id:
                        # Atualizar imagem existente
                        image = ProductImages.objects.get(id=image_id, product=product)
                        image_serializer = ProductImagesSerializer(image, data=image_data)
                        if image_serializer.is_valid():
                            image_serializer.save()
                    else:
                        # Adicionar nova imagem
                        image_data['product'] = product.id
                        image_serializer = ProductImagesSerializer(data=image_data)
                        if image_serializer.is_valid():
                            image_serializer.save()

            # Atualizar especificações
            specifications_data = request.data.get('specifications')
            if specifications_data:
                for spec_data in specifications_data:
                    spec_id = spec_data.get('id')
                    if spec_id:
                        spec = ProductSpecifications.objects.get(id=spec_id, product=product)
                        spec_serializer = ProductSpecificationsSerializer(spec, data=spec_data)
                        if spec_serializer.is_valid():
                            spec_serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=204)

    @action(detail=True, methods=['POST'])
    def add_image(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        data = {
            "product": product.pk,
            "foto": request.FILES.get('image')
        }
        serializer = ProductImagesSerializer(data=data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['POST'])
    def add_specification(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        data = {
            "product": product.pk,
            "specification": request.data.get("specification")
        }
        serializer = ProductSpecificationsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# class SpecificationsViewSet(viewsets.ViewSet):
#     filterset_class = SpecificationFilter
#
#     def list(self, request):
#         queryset = Specification.objects.all()
#         serializer = SpecificationSerializer(queryset, many=True)
#         return Response(serializer.data)


class SpecificationsListViewSet(generics.ListAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    filterset_class = SpecificationFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class SpecificationsCategoriesViewSet(generics.ListAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer

    # filterset_class = SpecificationFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.order_by('categories', 'name')  # Certifique-se de ordenar por categorias e nome

        grouped_data = []
        for key, group in groupby(queryset, lambda x: x.categories):
            group_dict = {
                'category': key,
                'specifications': []
            }
            for item in group:
                group_dict['specifications'].append({
                    'id': item.id,
                    'name': item.name,
                })
            grouped_data.append(group_dict)

        return Response(grouped_data, status=200)
