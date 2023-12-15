from django.test import TestCase
from django.core.exceptions import ValidationError
from tasks.forms import AddMemberForm
from tasks.models import Task, TaskList, Board, Teams, User
from datetime import datetime

class AddMemberFormTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='USER1', email='a@gmail.com', password='Subject6')
        self.user2 = User.objects.create(username='john', email='johndoe@example.org', password='Subject6')

        self.team = Teams.objects.create(author=self.user1)
        self.team.members.add(self.user1, self.user2)

        self.board = Board.objects.create(
            author_id=self.user1.id,
            board_name='Test Board',
            board_type='Team',
            team=self.team
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

        self.form_input = {'email': 'johndoe@example.org'}

    def test_valid_email(self):
        form = AddMemberForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_email(self):
        self.form_input['email'] = ''
        form = AddMemberForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        self.form_input['email'] = 'ichbinkrankenhouse@example.com'
        form = AddMemberForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_clean_email_method_valid_email(self):
        form = AddMemberForm(data = self.form_input)
        form.cleaned_data = {'email': 'test@example.com'}
        with self.assertRaises(ValidationError) as context:
            form.clean_email()
        self.assertEqual(
            str(context.exception),
            "['No user found with this email address.']"
        )

    def test_clean_email_method_blank_email(self):
        form = AddMemberForm(data = self.form_input)
        form.cleaned_data = {'email': ''}
        with self.assertRaises(ValidationError) as context:
            cleaned_email = form.clean_email()
            self.assertEqual(str(context.exception), 'Email field cannot be blank.')

    def test_clean_email_method_valid_formatted_email(self):
        form = AddMemberForm(data = {'email': 'johndoe@example.org'})
        form.cleaned_data = {'email': 'johndoe@example.org'}
        cleaned_email = form.clean_email()
        self.assertEqual(cleaned_email, 'johndoe@example.org')

    def test_email_exist_in_database_method_existing_email(self):
        form = AddMemberForm(data = self.form_input)
        email_exists = form.email_exist_in_database('johndoe@example.org')
        self.assertTrue(email_exists)

    def test_email_exist_in_database_method_non_existing_email(self):
        form = AddMemberForm(data = self.form_input)
        email_exists = form.email_exist_in_database('ichbinkrankenhouse@example.com')
        self.assertFalse(email_exists)
