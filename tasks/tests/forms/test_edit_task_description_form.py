from tasks.forms import EditTaskDescriptionForm
from tasks.models import Task, TaskList, Board, Teams
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

class EditTaskDescriptionFormTest(TestCase):

    def setUp(self):
        self.board = Board.objects.create(
        author_id=1,
        board_name='Test Board',
        board_type='Team',
        team_emails='test1@example.com,test2@example.com'
        )

        self.task_list = TaskList.objects.create(
        board=self.board,
        listName='Test List'
        )

        self.task = Task.objects.create(
        list=self.task_list,
        task_name='Test Task',
        task_description='Task Description',
        due_date=datetime.now(),
        task_priority=Task.Priority.LOW
        )

    def test_valid_edit_task_description_form(self):
        form_data = {'new_description': 'Updated task description.'}
        form = EditTaskDescriptionForm(data=form_data, instance=self.task)

        self.assertTrue(form.is_valid())
        updated_task = form.save()

        self.assertEqual(updated_task.task_description, 'Updated task description.')
        self.assertEqual(Task.objects.get(pk=self.task.pk).task_description, 'Updated task description.')

    def test_empty_new_description(self):
        form_data = {'new_description': ''}
        form = EditTaskDescriptionForm(data=form_data, instance=self.task)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_description'][0], 'This field is required.')

    def test_long_new_description(self):
        form_data = {'new_description': 'a' * 1001}
        form = EditTaskDescriptionForm(data=form_data, instance=self.task)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_description'][0], 'Task description length cannot exceed 1000')

    def test_form_save_commit_true(self):
        form_data = {'new_description': 'Updated task description.'}
        form = EditTaskDescriptionForm(data=form_data, instance=self.task)

        self.assertTrue(form.is_valid())
        updated_task = form.save(commit=True)

        self.assertEqual(updated_task.task_description, 'Updated task description.')
        self.assertEqual(Task.objects.get(pk=self.task.pk).task_description, 'Updated task description.')




