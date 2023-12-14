from django.test import TestCase
from datetime import date
from tasks.forms import CreateTaskForm 
from tasks.models import Task  

class CreateTaskFormTest(TestCase):
    def setUp(self):
        self.form_input = {
            'task_name': 'Test Task',
            'task_description': 'Description for the test task',
            'due_date': date(2023, 12, 31),
            'task_priority': Task.Priority.NONE,
        }

    def test_valid_task_form(self):
        form = CreateTaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_task_name(self):
        self.form_input['task_name'] = ''
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['task_name'], ['Task name cannot be blank.'])

    def test_long_task_name(self):
        self.form_input['task_name'] = 'A' * 51
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['task_name'], ['Task name length cannot exceed 50.'])

    def test_blank_due_date(self):
        self.form_input['due_date'] = None
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['due_date'], ['This field is required.'])

    def test_invalid_due_date(self):
        self.form_input['due_date'] = date(2022, 1, 1)
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['due_date'], ['Due date must be in the future.'])

