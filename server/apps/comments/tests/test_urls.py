from django.test import TestCase
from django.urls import resolve, reverse

from server.apps.users.tests.factories import UserFactory


class TestCommentsURLs(TestCase):

    def setUp(self):
        self.user_pk = UserFactory().pk

    def test_comments_reverse(self):
        assert reverse('users:user-comments',
                       kwargs={'pk': self.user_pk}
                       ) == f'/api/users/{self.user_pk}/comments/'

    def test_comments_resolve(self):
        assert resolve(
            f'/api/users/{self.user_pk}/comments/'
        ).view_name == 'users:user-comments'
