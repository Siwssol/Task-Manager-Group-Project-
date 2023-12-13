""""Tests for the Change Task Name View"""
from django.test import TestCase
from tasks.forms import EditTaskNameForm
from django.urls import reverse
from datetime import datetime
from tasks.models import Task

class EditTaskNameTestCase(TestCase):
    """"Tests for the Change Task Description View"""

    def setUp(self):
        self.url = reverse('change_task_name')
        self.task = Task.objects.get(new_name='Create User Stories',
                                        status='To Do',
                                        task_description = 'Break down assignment tasks',
                                        due_date = datetime(2023, 10, 9, 23, 55, 59, 342380))

    def tearDown(self):
        Task.objects.all().delete()

    def test_get_change_task_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_task_name.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditTaskNameForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_change_name_description(self):
        self.task['new_name'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pulvinar magna ac ipsum auctor consequat. Duis lacinia, elit quis tincidunt.'
        response = self.client.post(self.url, self.task)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_task_name.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditTaskNameForm))
        self.assertTrue(form.is_bound)

    def test_unsuccessful_change_task_description(self):
        response = self.client.post(self.url, self.task)
        response_url = reverse('change_task_name')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'change_task_name.html')

    """Test clean method"""

    def test_clean_method_blank_name(self):
        data = {"new": ""}
        form = EditTaskNameForm(data=data)
        self.assertFalse(form.is_valid())
        self.asserEqual(form.errors["new_name"][0], "Task name cannot be blank")

    def test_clean_method_50_character_name(self):
        data = {"new_name": "1" * 50}
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
        data = {"new_name": "Some new Task"}
        form = EditTaskNameForm(data=data, instance=task)
        self.assertTrue(form.is_valid())
        updated_name = form.save(commit=False)
        self.assertNotEquals(updated_name.task_name, "Some new Task")