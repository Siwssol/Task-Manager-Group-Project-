from tasks.models import Task, TaskList, Board, Teams, User
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

class TaskModelsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='USER1', email='a@gmail.com', password='Subject6')
        self.user2 = User.objects.create(username='USER2', email='b@gmail.com', password='Subject6')

        self.team = Teams.objects.create(author=self.user1)
        self.team.members.add(self.user1, self.user2)

        self.board = Board.objects.create(
            author_id= self.user1.id,
            board_name='Test Board',
            board_type='Team',
            team = self.team
        )

        self.task_list = TaskList.objects.create(
            board=self.board,
            listName='Test List'
        )

        self.task = Task.objects.create(
            list=self.task_list,
            task_name='Test Task',
            task_description='Task Description',
            due_date=datetime.now().date(),
            task_priority=Task.Priority.LOW
        )

    def test_task_list_creation(self):
        print("run 1")
        self.assertEqual(self.task_list.listName, 'Test List')
        self.assertEqual(self.task_list.board, self.board)

    def test_task_creation(self):
        print("run 2")
        self.assertEqual(self.task.task_name, 'Test Task')
        self.assertEqual(self.task.task_description, 'Task Description')
        self.assertEqual(self.task.due_date, (datetime.now().date()))
        self.assertEqual(self.task.task_priority, Task.Priority.LOW)
        self.assertEqual(self.task.list, self.task_list)

    def test_assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except (ValidationError):
            self.fail('Test task should be valid')

    def test_assert_task_is_invalid(self):
        self.task.task_name = "A" * 100
        self.task.save()
        with self.assertRaises(ValidationError):
            self.task.full_clean()