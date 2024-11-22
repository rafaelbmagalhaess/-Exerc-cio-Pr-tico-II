from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Colecao

class CriarColecaoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def get_auth_header(self, token):
        return {'Authorization': f'Token {token}'}

    def test_criar_colecao_com_usuario_autenticado(self):
        url = '/colecoes/'
        data = {'nome': 'Minha Coleção'}
        response = self.client.post(url, data, **self.get_auth_header(self.token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Colecao.objects.count(), 1)
        self.assertEqual(Colecao.objects.first().nome, 'Minha Coleção')
        self.assertEqual(Colecao.objects.first().usuario, self.user)

    def test_criar_colecao_sem_autenticacao(self):
        url = '/colecoes/'
        data = {'nome': 'Coleção do visitante'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Colecao.objects.count(), 0)
