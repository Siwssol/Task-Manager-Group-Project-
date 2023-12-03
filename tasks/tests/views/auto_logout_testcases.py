from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse


class AutoSignOutTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

    def test_auto_sign_out_after_inactivity(self):
        # Log in the user
        self.client.login(username='testuser', password='12345')

        # Simulate user activity- HAVE TO INCLUDE SPECIFIC PAGE LATER ON
        self.client.get('/dashboard/')

        # Simulate inactivity
        session = self.client.session
        session['last_activity'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT_DELAY_MINUTES + 1)
        session.save()

        # Try accessing a page after inactivity - HAVE TO INCLUDE SPECIFIC PAGE LATER ON
        response = self.client.get('/another_page/')

        # Check if the user is logged out (redirected to login page) - HAVE TO INCLUDE SPECIFIC PAGE LATER ON
        self.assertRedirects(response, '/login/?next=/another_page/')

    def test_activity_resets_timer(self):
        # Log in and simulate activity
        self.client.login(username='testuser', password='12345')
        self.client.get('/some_page/')

        # Simulate more activity before timeout
        session = self.client.session
        session['last_activity'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT_DELAY_MINUTES - 1)
        session.save()

        # Try accessing a page - HAVE TO INCLUDE SPECIFIC PAGE LATER ON
        response = self.client.get('/another_page/')

        # Check if still logged in
        self.assertEqual(response.status_code, 200)
        
        def test_user_interactions_after_auto_sign_out(self):
        # Log in and simulate inactivity
            self.client.login(username='testuser', password='12345')
            session = self.client.session
            session['last_activity'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT_DELAY_MINUTES + 1)
            session.save()

        # Attempt to access a page after supposed auto sign-out
        response = self.client.get(reverse('some_view'))

        # Check for redirection to the login page
        self.assertRedirects(response, '/login/?next=' + reverse('some_view'))

    def test_auto_sign_out_across_multiple_devices(self):
        # Log in on two different client instances
        client1 = Client()
        client2 = Client()
        client1.login(username='testuser', password='12345')
        client2.login(username='testuser', password='12345')

        # Simulate inactivity on client1 and activity on client2
        session1 = client1.session
        session1['last_activity'] = timezone.now() - timedelta(minutes=settings.AUTO_LOGOUT_DELAY_MINUTES + 1)
        session1.save()
        client2.get('/some_page/')

        # Check if client1 is signed out
        response1 = client1.get('/another_page/')
        self.assertRedirects(response1, '/login/?next=/another_page/')

        # Check if client2 is still signed in
        response2 = client2.get('/another_page/')
        self.assertEqual(response2.status_code, 200)



