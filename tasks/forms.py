"""Forms for the tasks app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

from .models import User, Board

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user

    

class EditTaskNameForm(forms.ModelForm):

    task_id = forms.IntegerField()
    new_name = forms.CharField(max_length=50, blank=False)



class CreateBoardForm(forms.ModelForm):
    """Form enabling user to create a board"""
    

    class Meta:
        """Board Form Options"""

        model = Board
        fields = ['board_name', 'board_type', 'team_emails']

    def clean(self):
        """Clean the data inputted by the user and generate a response if there are any errors."""

        super().clean()
        board_type = self.cleaned_data.get('board_type')

        if board_type == 'INVALID':

            self.add_error('board_type', 'Board Type is not valid. Please choose another type.')

        team_members = self.cleaned_data.get('team_emails')

        if (team_members == "Enter team emails here if necessary, seperated by commas." and board_type == "Team"):
            self.add_error('team_emails', 'Team emails is not valid.')

        elif (team_members == "Enter team emails here if necessary, seperated by commas." and board_type == "INVALID"):
            self.add_error('team_emails', 'Team emails is not valid.')

    def save(self):
        """ Create new board"""
        super().save(commit=False)
        board = Board.objects.create_board(
            self.cleaned_data.get('author'),
            board_name=self.cleaned_data.get('board_name'),
            board_type=self.cleaned_data.get('board_type'),
            team_emails=self.cleaned_data.get('team_emails'),
        )

            
