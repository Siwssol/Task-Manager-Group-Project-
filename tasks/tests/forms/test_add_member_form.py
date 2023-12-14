from django.test import TestCase
from tasks.forms import AddMemberForm
from tasks.models import Board, User
from django.core.exceptions import ValidationError

class AddMemberFormTest(TestCase):
    def setUp(self):
        self.form_input = {'email':'johndoe@example.org'}

    def test_valid_email(self):
        form = AddMemberForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_email(self):
        self.form_input['email'] = ''
        form = AddMemberForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        self.form_input['email'] = 'ichbinkrankenhouse@example.com'
        form = AddMemberForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_clean_email_method(self):
        form = AddMemberForm()
        form.cleaned_data = {'email': 'test@example.com'}
        cleaned_email = form.clean_email()
        self.assertRaises(ValidationError)

        form.cleaned_data = {'email': ''}
        cleaned_email = form.clean_email()
        self.assertRaises(ValidationError)

        form.cleaned_data = {'email': 'Johndoe@example.org'}
        cleaned_email = form.clean_email
        self.assertEqual(cleaned_email, 'Johndoe@example.org')

    def test_email_exist_in_database_method(self):
        form = AddMemberForm()
        email_exists = form.email_exist_in_database('Janedoe@example.org')
        self.assertTrue(email_exists)

        email_exists = form.email_exist_in_database('ichbinkrankenhouse@example.com')
        self.assertFalse(email_exists)
