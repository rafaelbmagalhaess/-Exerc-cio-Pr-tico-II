from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Colecao

class EditarColecaoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.other_token = Token.objects.create(user=self.other_user)

    def get_auth_header(self, token):
        return {'Authorization': f'Token {token}'}

    def test_editar_colecao_do_proprio_usuario(self):
        colecao = Colecao.objects.create(nome='Coleção Inicial', usuario=self.user)
        url = f'/colecoes/{colecao.id}/'
        data = {'nome': 'Coleção Editada'}
        response = self.client.put(url, data, **self.get_auth_header(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        colecao.refresh_from_db()
        self.assertEqual(colecao.nome, 'Coleção Editada')

    def test_editar_colecao_de_outro_usuario(self):
        colecao = Colecao.objects.create(nome='Coleção de Outro', usuario=self.other_user)
        url = f'/colecoes/{colecao.id}/'
        data = {'nome': 'Tentando Editar'}
        response = self.client.put(url, data, **self.get_auth_header(self.token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
