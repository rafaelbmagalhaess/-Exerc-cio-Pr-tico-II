from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .models import Livro, Categoria, Autor, Colecao
from .serializers import LivroSerializer, CategoriaSerializer, AutorSerializer, ColecaoSerializer
from .permissions import IsOwnerOrReadOnly  


class LivroFilter(filters.FilterSet):
    titulo = filters.CharFilter(lookup_expr='icontains')
    autor = filters.CharFilter(field_name='autor__nome', lookup_expr='icontains')
    categoria = filters.CharFilter(field_name='categoria__nome', lookup_expr='icontains')
    categoria_inicia_com = filters.CharFilter(field_name='categoria__nome', lookup_expr='startswith') 
    titulo_inicia_com = filters.CharFilter(field_name='titulo', lookup_expr='startswith') 

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria', 'categoria_inicia_com', 'titulo_inicia_com']



class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    name = "colecao-detail"


class ColecaoListCreate(generics.ListCreateAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        
        serializer.save(colecionador=self.request.user)

    name = "colecao-list-create"

class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"


class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"


class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter) 
    categoria_inicia_com = filters.CharFilter(field_name='nome', lookup_expr='startswith') 
    ordering_fields = ['nome']  
    ordering = ['nome']  
    name = "categoria-list"

class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)  
    ordering_fields = ['nome'] 
    ordering = ['nome']  
    name = "autor-list"

class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)  
    filterset_class = LivroFilter  
    ordering_fields = ['titulo', 'autor', 'categoria', 'publicado_em'] 
    ordering = ['titulo']  
    name = "livro-list"
