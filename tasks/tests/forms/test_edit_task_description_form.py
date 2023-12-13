from tasks.forms import EditTaskDescriptionForm
from tasks.models import Task
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime



class EditTaskNameDescriptionCase(TestCase):
    def setUp(self):
            self.task = Task.objects.get(task_name='Create User Stories',
                                        status='To Do',
                                        new_description = 'Break down assignment tasks',
                                        due_date = datetime(2023, 10, 9, 23, 55, 59, 342380))
    def tearDown(self):
        Task.objects.all().delete()

    # Check description accepts an empty string
    def test_empty_task_description(self):
        self.task.new_description = ''
        self.assert_task_is_valid()
    
    # Check description rejects over 1000 characters
    def test_task_description_over_1000_characters(self):
        self.task.new_description = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestib'
        self.assert_task_is_invalid()

    # Check description accepts exactly 1000 characters
    def test_description_equals_1000_characters(self):
        self.task.status = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N'
        self.assert_task_is_valid()

    """Test clean method"""
    def test_clean_method_blank_description(self):
        data = {"new_description": ""}
        form = EditTaskDescriptionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_clean_method_1000_character_description(self):
        data = {"new_description": "1" * 1000}
        form = EditTaskDescriptionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_clean_method_over_1000_character_description(self):
        data = {"new_description": "1" * 2000}
        form = EditTaskDescriptionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["new_description"][0], "Task description length cannot exceed 1000")


    """Test save method"""
    def test_save_method_commit_true(self):
        task = Task.objects.create(task_name="Some Task",
                                   description="previous description")
        data = {"new_description": "Some description"}
        form = EditTaskDescriptionForm(data=data, instance=task)
        self.assertTrue(form.is_valid())
        updated_description = form.save()
        self.assertEqual(updated_description.task_description, "Some description")

    def test_save_method_commit_false(self):
        task = Task.objects.create(task_name="Some Task 2",
                                   description="previous description")
        data = {"new_description": "Some description"}
        form = EditTaskDescriptionForm(data=data, instance=task)
        self.assertTrue(form.is_valid())
        updated_description = form.save(commit=False)
        self.assertNotEquals(updated_description.task_description, "Some description")




