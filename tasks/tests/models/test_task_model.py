from tasks.models import Task
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

class TaskModelTestCase(TestCase):

    def setUp(self):
        self.task = Task.objects.get(test_name='Create User Stories',
                                     status='To Do',
                                     task_description = 'Break down assignment tasks',
                                     due_date = datetime(2023, 10, 9, 23, 55, 59, 342380))
        
    # Check the task name isn't empty
    def test_empty_task_name(self):
        self.task.task_name = ''
        self.assert_task_is_invalid()

    # Check task name doesn't exceed given character count
    def test_task_over_50_characters(self):
        self.task.task_name = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pulvinar magna ac ipsum auctor consequat. Duis lacinia, elit quis tincidunt.'
        self.assert_task_is_invalid()

    # Check the task name is valid
    def test_valid_task_name(self):
        self.assert_task_is_valid()

    # Check task name can accept exactly 50 characters
    def test_task_equals_50_characters(self):
        self.task.task_name = 'Lorem ipsum dolor sit amet, consectetuer adipiscin'
        self.assert_task_is_valid()

    # Check task status can accept exactly 50 characters
    def test_status_equals_50_characters(self):
        self.task.status = 'Lorem ipsum dolor sit amet, consectetuer adipiscin'
        self.assert_task_is_valid()

    # Check task status rejects over 50 chatacters
    def test_status_over_50_characters(self):
        self.task.status = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pulvinar magna ac ipsum auctor consequat. Duis lacinia, elit quis tincidunt.'
        self.assert_task_is_invalid()

    # Check task status rejects empty description
    def test_empty_status(self):
        self.task.status = ''
        self.assert_task_is_invalid()

    # Check description rejects an empty string
    def test_empty_task_description(self):
        self.task.task_description = ''
        self.assert_task_is_invalid()
    
    # Check description rejects over 1000 characters
    def test_task_description_over_1000_characters(self):
        self.task.task_description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestib'
        self.assert_task_is_invalid()

    # Check description accepts exactly 1000 characters
    def test_description_equals_1000_characters(self):
        self.task.status = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N'
        self.assert_task_is_valid()

    
        



    # Defines what is valid
    def assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except (ValidationError):
            self.fail('Test task should be valid')


    # Defines what is invalid
    def assert_task_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.task.full_clean()