from django.test import TestCase
from tasks.forms import CreateBoardForm
from tasks.models import Board, User

class NewBoardTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='USER1', email='a@gmail.com', password='Subject6')
        self.user2 = User.objects.create(username='USER2', email='b@gmail.com', password='Subject6')
        self.user2 = User.objects.create(username='USER3', email='c@gmail.com', password='Subject6')
        self.user2 = User.objects.create(username='USER4', email='d@gmail.com', password='Subject6')



        self.form_input = {'board_name' : "Board 1", 
                           'board_type' : "Private",
                            'team_emails' : "Enter team emails here if necessary, seperated by commas.",
                            }
    
    def test_valid_board_form(self):
        form = CreateBoardForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_has_necessary_fields(self):
        form = CreateBoardForm()
        self.assertIn('board_name',form.fields)
        self.assertIn('board_type',form.fields)
        self.assertIn('team_emails',form.fields)
    
    def test_board_name_must_not_be_empty(self):
        self.form_input['board_name'] = ""
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_type_must_not_be_invalid(self):
        self.form_input['board_type'] = 'INVALID'
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_name_must_not_be_empty_characters(self):
        self.form_input['board_name'] = "   "
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_members_must_not_be_placeholder_text_if_user_selects_team(self):
        self.form_input['board_type'] = 'Team'
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_members_must_not_be_empty_if_board_type_is_team(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['team_emails'] = ""
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_members_must_not_consist_of_just_whitespace_if_board_type_is_team(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['team_emails'] = " "
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_members_must_not_consist_of_valid_and_invalid_emails(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['team_emails'] = "a@gmail.com, b@gmail.com, loremipsusmori"
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())        

    def test_board_invalid_if_user_selects_private_team_type_and_leaves_empty_members_text(self):
        self.form_input['board_type'] = 'Private'
        self.form_input['team_emails'] = ""
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_invalid_if_user_selects_private_team_type_and_puts_whitespace_in_members_text(self):
        self.form_input['team_emails'] = " "
        self.form_input['board_type'] = 'Private'
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_valid_if_user_selects_private_team_type_and_puts_any_text_in_members(self):
        self.form_input['team_emails'] = "lorem ipsus mori"
        self.form_input['board_type'] = 'Private'
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_valid_if_user_selects_team_team_type_and_enters_valid_emails(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['team_emails'] = 'a@gmail.com'
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_valid_if_user_selects_team_team_type_and_enters_multiple_valid_emails(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['team_emails'] = 'a@gmail.com, b@gmail.com, c@gmail.com'
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_board_type(self):
        form_data = {
            'board_name': 'Test Board',
            'board_type': 'INVALID',
            'team_emails': 'a@gmail.com.com, b@gmail.com',
        }
        form = CreateBoardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['board_type'], ['Select a valid option.'])


    def test_case_insensitive_emails(self):
        self.form_input['team_emails'] = 'A@Gmail.com, B@GMAIL.COM'
        form = CreateBoardForm(data=self.form_input)
        self.assertTrue(form.is_valid())


