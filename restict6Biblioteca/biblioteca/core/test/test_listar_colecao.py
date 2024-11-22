from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Colecao

class ListarColecaoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def get_auth_header(self, token):
        return {'Authorization': f'Token {token}'}

    def test_listar_colecao_com_usuario_autenticado(self):
        Colecao.objects.create(nome='Coleção Visível', usuario=self.user)
        url = '/colecoes/'
        response = self.client.get(url, **self.get_auth_header(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Coleção Visível')

    def test_listar_colecao_sem_autenticacao(self):
        Colecao.objects.create(nome='Coleção Privada', usuario=self.user)
        url = '/colecoes/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lista_colecoes_sem_ter_uma(self):
        url = '/colecoes/'
        response = self.client.get(url, **self.get_auth_header(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
