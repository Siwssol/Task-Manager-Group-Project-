"""Forms for the tasks app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Board, Teams, Task
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.core.exceptions import ValidationError


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
    """Form enabling users to change the task name."""

    class Meta:
        model = Task
        fields=['new_name']

    new_name = forms.CharField(max_length=50, required=True)

    def clean(self):
       cleaned_data = super().clean()
       new_task_name = cleaned_data.get("new_name")
       if not new_task_name:
           self.add_error("new_name", "Task name cannot be blank")
       elif len(new_task_name) > 50:
           self.add_error("new_name", "Task name length cannot exceed 50")

    def save(self, commit = True):
        instance = super().save(commit=False)
        new_task_name = self.cleaned_data['new_name']
        instance.task_name = new_task_name
        if commit:
            instance.save()
        return instance


class EditTaskDescriptionForm(forms.ModelForm):
    """Form enabling users to change the task description."""
    class Meta:
        model = Task
        fields=['new_description']

    new_description = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 1000}))

    def clean(self):
       cleaned_data = super().clean()
       new_task_description = cleaned_data.get("new_description")
       if new_task_description is not None and len(new_task_description) > 1000:
           self.add_error("new_description", "Task name length cannot exceed 1000")

    def save(self, commit = True):
        instance = super().save(commit=False)
        new_task_description = self.cleaned_data['new_description']
        instance.task_name = new_task_description
        if commit:
            instance.save()
        return instance


class CreateBoardForm(forms.ModelForm):
    """Form enabling user to create a board"""

    class Meta:
        """Board Form Options"""

        model = Board
        fields = ['board_name', 'board_type', 'team_emails']

    """Converts user inputted emails into comma seperated list """
    def emails_to_python(self):
        user_emails = self.cleaned_data.get('team_emails')
        user_emails = user_emails.split(",")
        for i in range(len(user_emails)):
            user_emails[i] = user_emails[i].strip()
        return user_emails
    
    """Checks all comma-seperated email values in User model and checks if they exist or not."""
    def emails_exist_in_database(self):
        user_emails = self.emails_to_python()
        doesntExist = False
        for usr in user_emails:
            if (doesntExist):
                break
            try:
                User.objects.get(email = usr) 
            except User.DoesNotExist:
                doesntExist = True
        return doesntExist
      
    def clean(self):
        """Clean the data inputted by the user and generate a response if there are any errors."""

        super().clean()

        board_name = self.cleaned_data.get('board_name')
        board_name_result = self.checkBoard(board_name)
        if(board_name_result):
            self.add_error('board_name','Board name is empty.')
            
        board_type = self.cleaned_data.get('board_type')
        board_type_result = self.checkBoardType(board_type)
        if (board_type_result):
            self.add_error('board_type','Select a valid option.')
        
        team_members = self.cleaned_data.get('team_emails')
        team_members_result = self.checkEmails(team_members,board_type)
        if (team_members_result):
            self.add_error('team_emails','Inputted emails is not valid')

    def checkBoard(self,board_name_to_analyse):
        if (board_name_to_analyse is None):
            return True
        else:
            return False
    
    def checkBoardType(self,board_type_to_analyse):
        if (board_type_to_analyse == "INVALID"):
            return True
        else:
            return False

    def checkEmails(self,team_emails_to_analyse,board_type_to_analyse):
        if (board_type_to_analyse == 'Private'):
            return False
        elif (team_emails_to_analyse is None):
            return True
        else:
            if (team_emails_to_analyse is None):
                return True
            elif (team_emails_to_analyse == "Enter team emails here if necessary, seperated by commas." and (board_type_to_analyse == 'INVALID' or board_type_to_analyse == 'Team')):
                return True
            else:
                return self.emails_exist_in_database()
        return False


    def save(self):
        """ Create new board"""
        super().save(commit=False)
        board = Board.objects.create_board(
            self.cleaned_data.get('author'),
            board_name=self.cleaned_data.get('board_name'),
            board_type=self.cleaned_data.get('board_type'),
            team_emails=self.cleaned_data.get('team_emails'),
        )


"""Form to create Task"""
class CreateTaskForm(forms.ModelForm):
    class Meta:

        model = Task
        fields = ["task_name", "task_description", "due_date"]

    due_date = forms.DateField(widget = forms.SelectDateWidget())

    def clean(self):
        cleaned_data = super().clean()
        task_name = cleaned_data.get("task_name")
        if not task_name:
            self.add_error("task_name", "Task name cannot be blank")
        elif len(task_name) > 50:
            self.add_error("task_name", "Task name length cannot exceed 50")

        due_date = cleaned_data.get("due_date")
        if not due_date:
            self.add_error("due_date", "Please enter a valid due date")

    def save(self):
        """Creates Task"""
        super().save(commit=False)
        task = Task.objects.create_task(
            task_name = self.cleaned_data.get('task_name'),
            task_description = self.cleaned_data.get('task_description'),
            due_date = self.cleaned_data.get('due_date')
        )
        task.save()
        return task

    
    # forms for checkbox -> add member 
    #
class AddMemberForm(forms.Form):
    email = forms.EmailField(label='Member Email')

    def email_exist_in_database(self, email):
        """Check if the email exists in the User model."""
        try:
            User.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False

    def clean_email(self):
        """Clean and validate the email field."""
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError("Email field cannot be blank.")

        if not self.email_exist_in_database(email):
            raise ValidationError("No user found with this email address.")

        return email

#forms for checkbox -> remove member 

class RemoveMemberForm(forms.Form):
    email = forms.EmailField(label='Member Email')

    def email_exist_in_database(self, email):
        """Check if the email exists in the User model."""
        try:
            User.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False

    def clean_email(self):
        """Clean and validate the email field."""
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError("Email field cannot be blank.")

        if not self.email_exist_in_database(email):
            raise ValidationError("No user found with this email address.")

        return email


    
# class AssignTasksForm(forms.Form):
#     available_members = forms.ModelMultipleChoiceField(
#         queryset=Teams.team_members.all(),
#         #Teams.objects.all()
#         widget = forms.CheckboxSelectMultiple

#     )

    """
class AssignTasksForm(forms.Form):
    available_members = forms.ModelMultipleChoiceField(
        queryset=Teams.team_members.all(),
        #Teams.objects.all()
        widget = forms.CheckboxSelectMultiple

    )
"""
