from django.test import TestCase
from datetime import date
from tasks.forms import CreateTaskForm 
from tasks.models import Task  

class CreateTaskFormTest(TestCase):
    def setUp(self):
        self.form_input = {
            'task_name': 'Test Task',
            'task_description': 'Description for the test task',
            'due_date_year': 2023,
            'due_date_month': 12,
            'due_date_day': 31,
        }

    def test_valid_task_form(self):
        form = CreateTaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_task_name(self):
        self.form_input['task_name'] = ''
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['task_name'], ['Task name cannot be blank'])

    def test_long_task_name(self):
        self.form_input['task_name'] = 'A' * 51
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['task_name'], ['Task name length cannot exceed 50'])

    def test_blank_due_date(self):
        self.form_input['due_date_year'] = ''
        self.form_input['due_date_month'] = ''
        self.form_input['due_date_day'] = ''
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['due_date'], ['Please enter a valid due date'])

    def test_invalid_due_date(self):
        self.form_input['due_date_year'] = 2022
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['due_date'], ['Please enter a valid due date'])

    def test_save_method(self):
        form = CreateTaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

        created_task = form.save()
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(created_task.task_name, 'Test Task')
        self.assertEqual(created_task.task_description, 'Description for the test task')
        self.assertEqual(created_task.due_date, date(2023, 12, 31))
        self.assertEqual(created_task.task_priority, 'NONE')