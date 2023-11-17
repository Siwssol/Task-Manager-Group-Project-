from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from libgravatar import Gravatar

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