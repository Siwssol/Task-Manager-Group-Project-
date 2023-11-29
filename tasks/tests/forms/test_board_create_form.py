from django.test import TestCase
from tasks.forms import CreateBoardForm
from tasks.models import Board, User

class NewBoardTest(TestCase):

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):

        self.form_input = {'board_name' : "Board 1", 
                           'board_type' : "Private",
                            'board_members' : "Enter team emails here if necessary, seperated by commas.",
                            }
    
    def test_valid_board_form(self):
        form = CreateBoardForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_has_necessary_fields(self):
        form = CreateBoardForm()
        self.assertIn('board_name',form.fields)
        self.assertIn('board_type',form.fields)
        self.assertIn('board_members',form.fields)
    
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
        self.form_input['board_members'] = ""
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_members_must_not_consist_of_just_whitespace_if_board_type_is_team(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['board_members'] = " "
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_board_members_must_not_consist_of_valid_and_invalid_emails(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['board_members'] = "abcd@gmail.com, abcd123@gmail.com, loremipsusmori"
        form = CreateBoardForm(data = self.form_input)
        self.assertFalse(form.is_valid())        

    def test_board_valid_if_user_selects_private_team_type_and_leaves_empty_members_text(self):
        self.form_input['board_members'] = ""
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_valid_if_user_selects_private_team_type_and_puts_whitespace_in_members_text(self):
        self.form_input['board_members'] = " "
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_valid_if_user_selects_private_team_type_and_puts_any_text_in_members(self):
        self.form_input['board_members'] = "lorem ipsus mori"
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_valid_if_user_selects_team_team_type_and_enters_valid_emails(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['board_members'] = 'abcd@gmail.com'
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_board_valid_if_user_selects_team_team_type_and_enters_multiple_valid_emails(self):
        self.form_input['board_type'] = 'Team'
        self.form_input['board_members'] = 'abcd@gmail.com, abcd1@gmail.com, abcd2@gmail.com'
        form = CreateBoardForm(data = self.form_input)
        self.assertTrue(form.is_valid())


