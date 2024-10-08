# core/filters.py

import django_filters
from .models import Livro

class LivroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    autor = django_filters.CharFilter(field_name='autor__nome', lookup_expr='icontains')
    categoria = django_filters.AllValuesFilter(field_name='categoria__nome')

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria']
