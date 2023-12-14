from tasks.models import Task, TaskList, Board
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

class TaskModelsTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            author_id=1,
            board_name='Test Board',
            board_type='Team',
            team_emails='test1@example.com,test2@example.com'
        )

        self.task_list = TaskList.objects.create(
            board=self.board,
            listName='Test List'
        )

        self.task = Task.objects.create(
            list=self.task_list,
            task_name='Test Task',
            task_description='Task Description',
            due_date=datetime.now(),
            task_priority=Task.Priority.LOW
        )

    def test_task_list_creation(self):
        self.assertEqual(self.task_list.listName, 'Test List')
        self.assertEqual(self.task_list.board, self.board)

    def test_task_creation(self):
        self.assertEqual(self.task.task_name, 'Test Task')
        self.assertEqual(self.task.task_description, 'Task Description')
        self.assertEqual(self.task.due_date.date(), (datetime.now()))
        self.assertEqual(self.task.task_priority, Task.Priority.LOW)
        self.assertEqual(self.task.list, self.task_list)

    def assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except (ValidationError):
            self.fail('Test task should be valid')

    def assert_task_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.task.full_clean()