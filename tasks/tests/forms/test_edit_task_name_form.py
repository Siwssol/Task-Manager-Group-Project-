from tasks.models import Task,TaskList
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from tasks.forms import EditTaskNameForm

class EditTaskNameFormTest(TestCase):

    def setUp(self):
        # Create a TaskList for testing
        self.task_list = TaskList.objects.create(name="Test Task List")

        # Create a Task for testing
        self.task = Task.objects.create(
            list=self.task_list,
            task_name="Original Task Name",
            task_description="Original task description.",
            due_date=datetime.now(),
            task_priority=Task.Priority.LOW
        )

    def test_valid_edit_task_name_form(self):
        form_data = {'new_name': 'Updated Task Name'}
        form = EditTaskNameForm(data=form_data, instance=self.task)

        self.assertTrue(form.is_valid())
        updated_task = form.save()

        self.assertEqual(updated_task.task_name, 'Updated Task Name')
        self.assertEqual(Task.objects.get(pk=self.task.pk).task_name, 'Updated Task Name')

    def test_empty_new_name(self):
        form_data = {'new_name': ''}
        form = EditTaskNameForm(data=form_data, instance=self.task)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_name'][0], 'Task name cannot be blank.')

    def test_long_new_name(self):
        form_data = {'new_name': 'a' * 51}
        form = EditTaskNameForm(data=form_data, instance=self.task)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_name'][0], 'Task name length cannot exceed 50.')

    def test_form_save_commit_true(self):
        form_data = {'new_name': 'Updated Task Name'}
        form = EditTaskNameForm(data=form_data, instance=self.task)

        self.assertTrue(form.is_valid())
        updated_task = form.save(commit=True)

        self.assertEqual(updated_task.task_name, 'Updated Task Name')
        self.assertEqual(Task.objects.get(pk=self.task.pk).task_name, 'Updated Task Name')