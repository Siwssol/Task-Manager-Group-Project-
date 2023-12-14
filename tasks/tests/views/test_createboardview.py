from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Teams, TeamMembershipStatus, Board, TaskList
from tasks.forms import CreateBoardForm

class CreateBoardViewTestCase(TestCase):
    """Tests for the create board view."""


    def setUp(self):
        self.url = reverse('create_board')
        self.user = User.objects.get(username='@johndoe')

    def test_create_board_url(self):
        self.assertEqual(self.url, '/create_board')  # Replace with the actual URL

    def test_get_create_board(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_board.html')  # Replace with the actual template name

    def test_valid_form_submission_for_team_board(self):
        self.client.login(username=self.user.username, password="testpassword")

        form_data = {
            'board_name': 'Test Team Board',
            'board_type': 'Team',
            'team_emails': 'user1@example.com, user2@example.com',
        }

        response = self.client.post(self.url, data=form_data)

        self.assertRedirects(response, '/dashboard/', status_code=302, target_status_code=200)

        self.assertTrue(Board.objects.filter(author=self.user, board_name='Test Team Board', board_type='Team').exists())
        self.assertTrue(TaskList.objects.filter(board__author=self.user, listName='To Do').exists())