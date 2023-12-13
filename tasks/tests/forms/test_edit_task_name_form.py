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

    def tearDown(self):
        Task.objects.all().delete()


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

    """Test clean method"""

    def test_clean_method_blank_name(self):
        data = {"new_name": ""}
        form = EditTaskNameForm(data=data)
        self.assertFalse(form.is_valid())

    def test_clean_method_50_character_name(self):
        data = {"new_description": "1" * 50}
        form = EditTaskNameForm(data=data)
        self.assertTrue(form.is_valid())

    def test_clean_method_over_50_character_name(self):
        data = {"new_name": "1" * 100}
        form = EditTaskNameForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["new_name"][0], "Task name length cannot exceed 50")


    """Test save method"""
    def test_save_method_commit_true(self):
        task = Task.objects.create(task_name="Some Task",
                                   description="Some description")
        data = {"new_name": "Some new Task"}
        form = EditTaskNameForm(data=data, instance=task)
        self.assertTrue(form.is_valid())
        updated_name = form.save()
        self.assertEqual(updated_name.task_name, "Some new Task")

    def test_save_method_commit_false(self):
        task = Task.objects.create(task_name="Some Task 2",
                                   description="Some description")
        data = {"new_name": "Some new Task 2"}
        form = EditTaskNameForm(data=data, instance=task)
        self.assertTrue(form.is_valid())
        updated_name = form.save(commit=False)
        self.assertNotEquals(updated_name.task_name, "Some new Task 2")