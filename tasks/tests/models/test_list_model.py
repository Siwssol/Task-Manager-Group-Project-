from django.test import TestCase
from tasks.models import TaskList, Board
from django.utils import timezone


class ListModelTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Test Board")
        self.todo_list = TaskList.objects.create( board = self.board, name="To Do")

    def test_list_str(self):
        self.assertEqual(str(self.todo_list), "To Do")