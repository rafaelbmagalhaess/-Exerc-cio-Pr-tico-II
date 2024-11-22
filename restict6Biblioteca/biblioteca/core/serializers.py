from rest_framework import serializers
from .models import Categoria, Autor, Livro, Colecao  


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class ColecaoSerializer(serializers.ModelSerializer):
    colecionador = serializers.StringRelatedField() 
    livros = serializers.PrimaryKeyRelatedField(queryset=Livro.objects.all(), many=True)  

    class Meta:
        model = Colecao
        fields = ['id', 'nome', 'descricao', 'livros', 'colecionador']

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome']

class LivroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer()  
    categoria = CategoriaSerializer() 

    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'categoria', 'publicado_em']