""""Tests for the Change Task Description View"""
from django.test import TestCase
from tasks.forms import EditTaskDescriptionForm
from django.urls import reverse
from datetime import datetime
from tasks.models import Task

class EditTaskDescriptionTestCase(TestCase):
    """"Tests for the Change Task Description View"""

    def setUp(self):
        self.url = reverse('change_task_description')
        self.task = Task.objects.get(task_name='Create User Stories',
                                        status='To Do',
                                        new_description = 'Break down assignment tasks',
                                        due_date = datetime(2023, 10, 9, 23, 55, 59, 342380))

    def test_get_change_task_description(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_task_description.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditTaskDescriptionForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_change_task_description(self):
        self.task['new_description'] = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestib'
        response = self.client.post(self.url, self.task)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_task_description.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditTaskDescriptionForm))
        self.assertTrue(form.is_bound)

    def test_unsuccessful_change_task_description(self):
        response = self.client.post(self.url, self.task)
        response_url = reverse('change_task_description')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'change_task_description.html')
