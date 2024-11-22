from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Colecao

class DeletarColecaoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.other_token = Token.objects.create(user=self.other_user)

    def get_auth_header(self, token):
        return {'Authorization': f'Token {token}'}

    def test_deletar_colecao_do_proprio_usuario(self):
        colecao = Colecao.objects.create(nome='Coleção para Deletar', usuario=self.user)
        url = f'/colecoes/{colecao.id}/'
        response = self.client.delete(url, **self.get_auth_header(self.token))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Colecao.objects.count(), 0)

    def test_deletar_colecao_de_outro_usuario(self):
        colecao = Colecao.objects.create(nome='Coleção de Outro', usuario=self.other_user)
        url = f'/colecoes/{colecao.id}/'
        response = self.client.delete(url, **self.get_auth_header(self.token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
