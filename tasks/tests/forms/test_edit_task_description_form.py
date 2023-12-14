from tasks.forms import EditTaskDescriptionForm
from tasks.models import Task
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

class EditTaskDescriptionFormTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            task_name='Test Task',
            task_description='Original description',
            due_date='2023-12-31'
        )

        self.form_input = {'new_description': 'Updated description'}

    def test_valid_task_description_form(self):
        form = EditTaskDescriptionForm(instance=self.task, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_long_task_description(self):
        self.form_input['new_description'] = 'A' * 1001
        form = EditTaskDescriptionForm(instance=self.task, data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_description'], ['Task description length cannot exceed 1000'])

    def test_save_method(self):
        form = EditTaskDescriptionForm(instance=self.task, data=self.form_input)
        self.assertTrue(form.is_valid())
        original_description = self.task.task_description
        form.save()
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertNotEqual(updated_task.task_description, original_description)
        self.assertEqual(updated_task.task_description, 'Updated description')

    def test_clean_method_long_description(self):
        task = Task.objects.create(
            task_name='Test Task',
            task_description='Original description that is too long' * 50,
            due_date='2023-12-31'
        )
        form_input = {'new_description': 'Updated description that is too long' * 50}

        form = EditTaskDescriptionForm(instance=task, data=form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_description'], ['Task description length cannot exceed 1000'])




