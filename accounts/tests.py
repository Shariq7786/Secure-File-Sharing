# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AccountsViewTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='Username', password='786')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.dashboard_url = reverse('dashboard')

    def test_register_view_get(self):
        # Test HTTP GET on register view
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_view_post(self):
        # Test HTTP POST on register view (user creation)
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'django786',
            'password2': 'django786'
        })
        self.assertEqual(User.objects.count(), 2)  # Including the user created in setUp

    def test_login_view_post(self):
        # Test login with POST
        self.client.login(username='Username', password='786')
        response = self.client.post(self.login_url, {
            'username': 'Username',
            'password': '786'
        })
        self.assertRedirects(response, self.dashboard_url)

    def test_dashboard_access(self):
        # Test access to dashboard
        self.client.login(username='Username', password='786')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)