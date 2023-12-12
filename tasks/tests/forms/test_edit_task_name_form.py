from tasks.models import Task
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from tasks.forms import EditTaskNameForm




class EditTaskNameTestCase(TestCase):
    def setUp(self):
            self.task = Task.objects.get(new_name='Create User Stories',
                                        status='To Do',
                                        task_description = 'Break down assignment tasks',
                                        due_date = datetime(2023, 10, 9, 23, 55, 59, 342380))

    # Check the new task name isn't empty
    def test_empty_new_task_name(self):
        self.task.new_name = ''
        self.assert_task_is_invalid()

    # Check new task name doesn't exceed given character count
    def test_new_task_over_50_characters(self):
        self.task.new_name = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pulvinar magna ac ipsum auctor consequat. Duis lacinia, elit quis tincidunt.'
        self.assert_task_is_invalid()

    # Check the new task name is valid
    def test_valid_new_task_name(self):
        self.assert_task_is_valid()

    # Check new task name can accept exactly 50 characters
    def test_new_task_equals_50_characters(self):
        self.task.new_name = 'Lorem ipsum dolor sit amet, consectetuer adipiscin'
        self.assert_task_is_valid()

    def test_save_method(self):
        form_data = {
            'task_id': self.task.id,
            'new_name': 'Updated Task Name',
        }
        form = EditTaskNameForm(data=form_data)
        self.assertTrue(form.is_valid())
        updated_task = form.save()
        self.assertEqual(updated_task.task_name, 'Updated Task Name')