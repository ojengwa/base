from django.test import TestCase
from django.urls import resolve, reverse


class TestAPIURLs(TestCase):

    def test_api_rest_password_reset_reverse(self):
        assert reverse('rest_password_reset') == '/api/v1/password/reset/'

    def test_api_rest_password_reset_resolve(self):
        assert resolve(
            '/api/v1/password/reset/').view_name == 'rest_password_reset'

    def test_api_rest_password_reset_confirm_reverse(self):
        assert reverse(
            'rest_password_reset_confirm') == '/api/v1/password/reset/confirm/'

    def test_api_rest_password_reset_confirm_resolve(self):
        assert resolve(
            '/api/v1/password/reset/confirm/'
        ).view_name == 'rest_password_reset_confirm'

    def test_api_rest_login_reverse(self):
        assert reverse('rest_login') == '/api/v1/login/'

    def test_api_rest_login_resolve(self):
        assert resolve('/api/v1/login/').view_name == 'rest_login'

    def test_api_rest_logout_reverse(self):
        assert reverse('rest_logout') == '/api/v1/logout/'

    def test_api_rest_logout_resolve(self):
        assert resolve('/api/v1/logout/').view_name == 'rest_logout'

    def test_api_rest_user_details_reverse(self):
        assert reverse('rest_user_details') == '/api/v1/me/'

    def test_api_rest_user_details_resolve(self):
        assert resolve(
            '/api/v1/current-user/').view_name == 'rest_user_details'

    def test_api_docs_reverse(self):
        assert reverse('api_docs') == '/api/v1/docs/'

    def test_api_docs_resolve(self):
        assert resolve('/api/v1/docs/').view_name == 'api_docs'
