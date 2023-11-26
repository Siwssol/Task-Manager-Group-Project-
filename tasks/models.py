from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from libgravatar import Gravatar
from datetime import datetime


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""


        return self.gravatar(size=60)


class Teams():
    """initialises the teams and shows what type of permissions there are """
    permissions = ['owner', 'admin', 'member', 'guest']
    def __init__(self):
        self.teammembers = []
        self.teampermissions = []
        
    """function for adding a user to the team"""
    def add_user(self, user):
        self.teammembers.append(user)
        if 'owner' not in self.teampermissions:
            self.teampermissions.append('owner')
        else:
            self.teampermissions.append('guest')
    """function for inviting users after team has been initialised"""
    def invite_user(self, user, str):
        self.teammembers.append(user)
        """invite via email will go in here once it is figured out how to do so"""
        if str.lower() in Teams.permissions:
            if str.lower() != 'owner':
                self.teammembers.append(str.lower())
            else:
                print("only one owner can exist within a board")
    
    """function for changing ownership if need be"""
    """this ensures that the owner level of permission has to be willingly changed rather than being able to make a new user as an owner"""
    
    def change_ownership(self, user, user2):
        pos1 = self.teammembers.index(user)
        pos2 = self.teammembers.index(user2)    
        if pos1 == self.teampermissions.index('owner'):
            self.teampermissions[pos1], self.teampermissions[pos2] = self.teampermissions[pos2], self.teampermissions[pos1]

    def change_perms(self,user,str):
        pos = self.teammembers.index(user)
        if str in Teams.permissions:    
            if self.teampermissions[pos] != 'owner':
                self.teampermissions[pos] = str.lower()

    def remove_user(self, user):
        pos = self.teammembers(user)
        if self.teampermissions[pos]!= 'owner':
            self.teampermissions.pop(pos)
            self.teammembers.pop(pos)

    def access_perms(self,user):
        pos = self.teammembers(user)
        return self.teampermissions[pos]

    class Meta:
        managed = False
       
    
class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    BOARD_CHOICES = (('INVALID','Choose Type'),
                    ('Private','Private'),
                    ('Team','Team'),
                    )
        
    board_name = models.CharField(primary_key=True,
                                max_length=30,
                                unique=True,
                                )
    
    board_type = models.CharField(max_length=11,choices=BOARD_CHOICES,default='INVALID')
    team_emails = models.TextField(default="Enter team emails here if necessary, seperated by commas.")

    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    
    def initialiseteam(self):
        team_users = self.team_emails.split(',')
        for email in team_users:
            usernames = email.split('@')
            username = '@' + usernames[0]
            self.team.add_user(username)
    
    def invite(self , name, perm):
        self.team.invite_user(name, perm)

    def removemember(self,user):
        self.remove_user(user)


"""Each task will be stored in a certain list, so we need to keep track on which list the task is in"""
class TaskList(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    listName = models.CharField(max_length=50, blank=False)

class Task(models.Model):

    """Model used for creating tasks, with attached parameters."""
    # Links the task model to the list
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, default="To do")
    #Defines the name
    task_name = models.CharField(max_length=50, blank=False)
    # Defines the status
    status = models.CharField(max_length=50, blank=False)
    # Defines the description
    task_description = models.TextField(max_length=1000)
    #Defines the due Date
    due_date = models.DateTimeField()