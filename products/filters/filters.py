from django_filters import rest_framework as filters

from products.models import Specification


class SpecificationFilter(filters.FilterSet):
    class Meta:
        model = Specification
        fields = ['name', 'categories']
