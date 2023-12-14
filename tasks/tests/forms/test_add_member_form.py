from django.test import TestCase
from django.core.exceptions import ValidationError
from tasks.forms import AddMemberForm  # Replace 'your_app' with the actual app name

class AddMemberFormTest(TestCase):
    def setUp(self):
        self.form_input = {'email': 'johndoe@example.org'}

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

    def test_clean_email_method_valid_email(self):
        form = AddMemberForm()
        form.cleaned_data = {'email': 'test@example.com'}
        with self.assertRaises(ValidationError) as context:
            form.clean_email()
        self.assertEqual(
            str(context.exception),
            'No user found with this email address'
        )

    def test_clean_email_method_blank_email(self):
        form = AddMemberForm()
        form.cleaned_data = {'email': ''}
        with self.assertRaises(ValidationError) as context:
            cleaned_email = form.clean_email()
            self.assertEqual(str(context.exception), 'Email field cannot be blank.')

    def test_clean_email_method_valid_formatted_email(self):
        form = AddMemberForm()
        form.cleaned_data = {'email': 'Johndoe@example.org'}
        cleaned_email = form.clean_email()
        self.assertEqual(cleaned_email, 'Johndoe@example.org')

    def test_email_exist_in_database_method_existing_email(self):
        form = AddMemberForm()
        email_exists = form.email_exist_in_database('Janedoe@example.org')
        self.assertTrue(email_exists)

    def test_email_exist_in_database_method_non_existing_email(self):
        form = AddMemberForm()
        email_exists = form.email_exist_in_database('ichbinkrankenhouse@example.com')
        self.assertFalse(email_exists)
