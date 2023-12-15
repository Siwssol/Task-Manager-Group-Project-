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


"""Model in charge of storing achievement metrics for each respective user"""
class Achievements(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    number_of_boards_created = models.IntegerField(default=0)
    number_of_boards_deleted = models.IntegerField(default=0)
    number_of_tasks_created = models.IntegerField(default=0)
    number_of_tasks_doing = models.IntegerField(default=0)
    number_of_tasks_completed = models.IntegerField(default=0)
    number_of_logins_completed = models.IntegerField(default=0)

    boards_created_1 = models.DateField(null=True, blank=True, verbose_name='1st Board Deleted')
    boards_created_10 = models.DateField(null=True, blank=True, verbose_name='10th Board Deleted')
    boards_created_50 = models.DateField(null=True, blank=True, verbose_name='50th Board Deleted')
    boards_created_100 = models.DateField(null=True, blank=True, verbose_name='100th Board Deleted')

    boards_deleted_1 = models.DateField(null=True, blank=True, verbose_name='1st Board Deleted')
    boards_deleted_10 = models.DateField(null=True, blank=True, verbose_name='10th Board Deleted')
    boards_deleted_50 = models.DateField(null=True, blank=True, verbose_name='50th Board Deleted')
    boards_deleted_100 = models.DateField(null=True, blank=True, verbose_name='100th Board Deleted')

    tasks_created_1 = models.DateField(null=True, blank=True, verbose_name='1st Board Deleted')
    tasks_created_10 = models.DateField(null=True, blank=True, verbose_name='10th Board Deleted')
    tasks_created_50 = models.DateField(null=True, blank=True, verbose_name='50th Board Deleted')
    tasks_created_100 = models.DateField(null=True, blank=True, verbose_name='100th Board Deleted')

    tasks_doing_1 = models.DateField(null=True, blank=True, verbose_name='1st Board Deleted')
    tasks_doing_10 = models.DateField(null=True, blank=True, verbose_name='10th Board Deleted')
    tasks_doing_50 = models.DateField(null=True, blank=True, verbose_name='50th Board Deleted')
    tasks_doing_100 = models.DateField(null=True, blank=True, verbose_name='100th Board Deleted')

    tasks_completed_1 = models.DateField(null=True, blank=True, verbose_name='1st Board Deleted')
    tasks_completed_10 = models.DateField(null=True, blank=True, verbose_name='10th Board Deleted')
    tasks_completed_50 = models.DateField(null=True, blank=True, verbose_name='50th Board Deleted')
    tasks_completed_100 = models.DateField(null=True, blank=True, verbose_name='100th Board Deleted')

    logins_completed_1 = models.DateField(null=True, blank=True, verbose_name='1st Board Deleted')
    logins_completed_10 = models.DateField(null=True, blank=True, verbose_name='10th Board Deleted')
    logins_completed_50 = models.DateField(null=True, blank=True, verbose_name='50th Board Deleted')
    logins_completed_100 = models.DateField(null=True, blank=True, verbose_name='100th Board Deleted')

    # increment one of the number fields above depending on the type of task completed
    def increment_achievements(self,achievement_type):

        achievement = f'number_of_{achievement_type}'
        setattr(self, achievement, getattr(self, achievement) + 1)

        # Check for milestones and update dates
        milestone_field_name = f'{achievement_type}_1'
        if getattr(self, achievement) == 1 and not getattr(self, milestone_field_name):
            setattr(self, milestone_field_name, timezone.now().date())

        milestone_field_name = f'{achievement_type}_10'
        if getattr(self, achievement) == 10 and not getattr(self, milestone_field_name):
            setattr(self, milestone_field_name, timezone.now().date())

        milestone_field_name = f'{achievement_type}_50'
        if getattr(self, achievement) == 50 and not getattr(self, milestone_field_name):
            setattr(self, milestone_field_name, timezone.now().date())

        milestone_field_name = f'{achievement_type}_100'
        if getattr(self, achievement) == 100 and not getattr(self, milestone_field_name):
            setattr(self, milestone_field_name, timezone.now().date())

        # Save the changes
        self.save()


""" Model in charge of storing user and their respective permission level within the board (restricts interaction ability)"""
class TeamMembershipStatus(models.Model):
    class Permissions(models.IntegerChoices):
        OWNER = 1
        MEMBER = 2
        GUEST = 3
    
    team = models.ForeignKey('Teams', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_level = models.IntegerField(choices=Permissions.choices, default=Permissions.GUEST)


""" Initialises team object and stores the associated members and creator"""
class Teams(models.Model):
        
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='TeamMembershipStatus', related_name='team_member')
                
class Board(models.Model):
    BOARD_CHOICES = (('INVALID','Choose Type'),
                ('Private','Private'),
                ('Team','Team'),
                )
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name='auth')
        
    board_name = models.CharField(primary_key=True,
                                max_length=30,
                                unique=True,
                                blank = False
                                )
    
    board_type = models.CharField(max_length=11,
                                  choices=BOARD_CHOICES,
                                  default='INVALID',
                                  )
    
    team_emails = models.TextField(default="Enter team emails here if necessary, seperated by commas.",
                                  )
    team = models.OneToOneField(Teams,on_delete = models.CASCADE)
    
    def initialiseteam(self):
        team_users = self.team_emails.split(',')
        for email in team_users:
            usernames = email.split('@')
            username = '@' + usernames[0]
            self.team.add_user(username)
    

    def invite(self , name, perm):
        self.team.invite_user(name, perm)
        
        
    def remove_member(self, requesting_user, user_to_remove):
        if self.author != requesting_user:
            raise PermissionError("Only the board owner can remove members.")
        if self.team.members.filter(id=user_to_remove.id).exists():
            self.team.members.remove(user_to_remove)
        else:
            raise ValueError("User is not a member of the board")


    def removeuser(self , user):
        self.remove_user(user)


"""Each task will be stored in a certain list, so we need to keep track on which list the task is in"""
class TaskList(models.Model):

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    listName = models.CharField(max_length=50, blank=False)

class Task(models.Model):
    """Priority system"""
    class Priority(models.TextChoices):
        NONE = "NONE"
        LOW = "LOW"
        MID = "MID"
        HIGH = "HIGH"
    class Meta:
        ordering = ["due_date"]

    """Model used for creating tasks, with attached parameters."""
    # Links the task model to the list
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    #Defines the name
    task_name = models.CharField(max_length=50, blank=False)
    # Defines the description
    task_description = models.TextField(max_length=1000)
    #Defines the due Date
    due_date = models.DateTimeField()
    #Defines priority
    task_priority = models.TextField(choices=Priority.choices, default=Priority.NONE)
    #Defines assigned members
    assigned_members = models.ManyToManyField(User)
