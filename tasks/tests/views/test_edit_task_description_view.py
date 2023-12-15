""""Tests for the Change Task Description View"""
from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import Task, TaskList, Board, User, Teams
from tasks.forms import EditTaskDescriptionForm
from datetime import datetime

class EditTaskDescriptionTestCase(TestCase):
    """"Tests for the Change Task Description View"""

    def setUp(self):
        self.client = Client()

        # Create a user
        self.user1 = User.objects.create(username='USER1', email='a@gmail.com', password='Subject6')
        self.user2 = User.objects.create(username='USER2', email='b@gmail.com', password='Subject6')

        # Log in the user
        self.client.login(username='USER1', password='Subject6')

        self.team = Teams.objects.create(author=self.user1)
        self.team.members.add(self.user1, self.user2)

        # Create a board, task list, and task
        self.board = Board.objects.create(
            author_id=self.user1.id,
            board_name='Test Board',
            board_type='Team',
            team = self.team
        )

        self.task_list = TaskList.objects.create(
            board=self.board,
            listName='Test List'
        )

        self.task = Task.objects.create(
            list=self.task_list,
            task_name='Test Task',
            task_description='Task Description',
            due_date=datetime.now().date(),
            task_priority=Task.Priority.LOW
        )

    def test_change_task_description_view(self):
        # Prepare the data for the POST request
        data = {
            'new_description': 'New description',
            'board_name': self.board.board_name
        }

        self.client.login(username=self.user1.username, password='Subject6')

        # Get the URL for the view
        url = reverse('change_task_description', args=[self.task.id, self.board.board_name])


        # Send a POST request to the view
        response = self.client.post(url, data)

        # Check if the response is a redirect (indicating success)
        self.assertRedirects(response,  reverse('board', args=[self.board.board_name]))

        # Refresh the task from the database
        self.task.refresh_from_db()

        # Check if the task description has been updated
        self.assertEqual(self.task.task_description, 'New description')

    def test_change_task_description_invalid_form(self):
        # Prepare invalid data for the POST request
        invalid_data = {
            'new_description': 'A' * 1000,  # This exceeds the maxlength of the textarea
            'board_name': self.board.board_name
        }

        # Get the URL for the view
        url = reverse('change_task_description', args=[self.task.id, self.board.board_name])

        # Send a POST request with invalid data to the view
        response = self.client.post(url, invalid_data)

        # Check if the response contains the form
        self.assertContains(response, '<form')

        # Check if the task description has not been updated
        self.task.refresh_from_db()
        self.assertEqual(self.task.task_description, 'Original description')
