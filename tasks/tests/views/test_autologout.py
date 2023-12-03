# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class AutoLogoutTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

    def test_auto_logout_due_to_inactivity(self):
        # User login
        self.client.login(username='testuser', password='12345')
        self.client.get(reverse('dashboard'))

        # Simulate user inactivity past the threshold
        self.client.session['last_active_time'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT + 10)
        self.client.session.save()

        # Attempt to access another page
        response = self.client.get(reverse('another_view'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('another_view'))

    def test_continued_activity_prevents_logout(self):
        # User login and initial activity
        self.client.login(username='testuser', password='12345')
        self.client.get(reverse('dashboard'))

        # Simulate activity within the threshold
        self.client.session['last_active_time'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT - 5)
        self.client.session.save()

        # Access a page within the activity window
        response = self.client.get(reverse('stay_active_view'))
        self.assertEqual(response.status_code, 200)

    def test_auto_logout_behavior_on_multiple_sessions(self):
        # Initialize two different clients (simulating two sessions)
        client_a = Client()
        client_b = Client()
        client_a.login(username='testuser', password='12345')
        client_b.login(username='testuser', password='12345')

        # Client A is inactive while Client B stays active
        client_a.session['last_active_time'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT + 10)
        client_a.session.save()
        client_b.get(reverse('dashboard'))

        # Verify Client A is logged out
        response_a = client_a.get(reverse('test_view_a'))
        self.assertRedirects(response_a, reverse('login') + '?next=' + reverse('test_view_a'))

        # Verify Client B remains logged in
        response_b = client_b.get(reverse('test_view_b'))
        self.assertEqual(response_b.status_code, 200)

    def test_user_action_post_auto_logout(self):
        # User login and then goes inactive
        self.client.login(username='testuser', password='12345')
        self.client.session['last_active_time'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT + 10)
        self.client.session.save()

        # User tries to access a page after auto logout
        response = self.client.get(reverse('post_logout_view'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('post_logout_view'))




