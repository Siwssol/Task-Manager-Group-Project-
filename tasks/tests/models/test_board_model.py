from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from tasks.models import Board, User


class BoardModelTestCase(TestCase):
    
    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        super(TestCase,self).setUp()
        self.user = User.objects.get(username='@johndoe')
        self.board = Board(
            author = self.user,
            board_name = "Test Board",
            board_type = 'Private',
            team_emails = "Enter team emails here if necessary, seperated by commas."
        )
        
    def test_valid_board(self):
        try:
            self.board.full_clean()
        except ValidationError:
            self.fail("Board not valid.")
    
    def test_author_must_not_be_blank(self):
        self.board.author = None
        with self.assertRaises(ValidationError):
            self.board.full_clean()

    def test_board_must_not_be_blank(self):
        self.board.board_name = ''
        with self.assertRaises(ValidationError):
            self.board.full_clean()
    
    def test_board_type_must_not_be_invalid(self):
        pass


    """ THESE TESTS WILL BE NECESSARY FOR TESTING NEW BOARDS APPEARING AND NOT APPEARING"""
    # def test_create_new_board_url(self):
    #     self.assertEqual(self.url, '/create_board/')

    # def test_successful_new_board(self):
    #     self.client.login(username=self.user.username, password="Password123")
    #     user_count_before = Board.objects.count()
    #     response = self.client.post(self.url, self.data,follow=True)
    #     user_count_after = Board.objects.count()
    #     self.assertEqual(user_count_before+1,user_count_after)
    #     new_board = Board.objects.count()
    #     self.assertEqual(self.user, new_board.author)
    #     response_url = reverse('feed')
    #     self.assertRedirects(
    #         response, response_url,
    #         status_code=302, target_status_code=200,
    #         fetch_redirect_response=True
    #     )
    #     self.assertTemplateUsed(response,'feed.html')
    
    # def test_unsuccessful_new_board(self):
    #     self.client.login(username='@johndoe',password='Password123')
    #     user_count_before = Board.objects.count()
    #     self.data['board_name'] = ""
    #     response = self.client.post(self.url,self.data, follow=True)
    #     user_count_after = Board.objects.count()
    #     self.assertEqual(user_count_after,user_count_before)
    #     self.assertTemplateUsed(response, 'create_board')
    
    # def test_cannot_create_board_for_other_user(self):
    #     self.client.login(username='@johndoe',password='Password123')
    #     other_user = User.objects.get(username='@johndoe')
    #     self.data['author'] = other_user.id
    #     user_count_before = Board.objects.count()
    #     response = self.client.post(self.url, self.data, follow=True)
    #     user_count_after = Board.objects.count()
    #     self.assertEqual(user_count_before+1,user_count_after)
    #     new_board = Board.objects.latest('created_at')
    #     self.assertEqual(self.user, new_board.author)

