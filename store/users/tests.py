from http import HTTPStatus

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from users.models import EmailVerification, User


class UserRegistrationTest(TestCase):

    def setUp(self):
        soc_app = SocialApp.objects.create(
            provider='github',
            name='GitHub',
            client_id='fake',
            secret='fake_s'

        )
        soc_app.sites.add(Site.objects.get(id=1))

    def test_register(self):
        path = reverse('users:register')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Registration')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_post_success(self):
        data = {
            'first_name': 'Stef', 'last_name': 'Ros',
            'username': 'fr',
            'email': 'j@gmail.com',
            'password1': 'R456rtyFGH', 'password2': 'R456rtyFGH',
        }
        username = data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        path = reverse('users:register')
        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        # test user creation after registration
        self.assertTrue(User.objects.filter(username=username).exists())

        # test user email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())

    def test_register_post_errors(self):
        pass


class UserLoginTest(TestCase):
    def setUp(self):
        self.path = reverse('users:login')
        self.user = User.objects.create_user(username='Ivan', password='123qweAS')

        soc_app = SocialApp.objects.create(
            provider='github',
            name='GitHub',
            client_id='fake',
            secret='fake_s'

        )
        soc_app.sites.add(Site.objects.get(id=1))

    def login_user(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        return self.client.post(self.path, data=data)

    def test_login(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Login')
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        response = self.login_user('Ivan', '123qweAS')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_invalid_data(self):
        response = self.login_user('Ian', '123eAS')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Please enter a correct username and password', html=True)
