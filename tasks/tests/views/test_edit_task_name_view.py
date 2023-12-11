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