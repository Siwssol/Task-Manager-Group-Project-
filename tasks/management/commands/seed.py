from django.core.management.base import BaseCommand, CommandError

from tasks.models import User, Teams, Board, TaskList, Task

from tasks.models import User, Achievements

import pytz
from faker import Faker
from random import randint, random
from django.utils import timezone
from django.contrib.auth import get_user_model

fake = Faker('en_GB')

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 300
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.create_teams_boards_tasks()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def try_create_user(self, data):
        try:
            self.create_user(data)
        except Exception as e:
            print(f"Error creating user: {e}")

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )

    
    
    def create_teams_boards_tasks(self):
        users = get_user_model().objects.all()

        for user in users:
            for i in range(10):
                
                team = Teams.objects.create(author=user)
                team.members.add(user)
                # Create a private board without a team
                board_name = f"{user.username}'s Board {i}"
                board = Board.objects.create(
                    author=user,
                    board_name=board_name,
                    board_type='Private',
                    team = team
                )
    
"""                for list_name in ['To-Do', 'In Progress', 'Done']:
                    task_list = TaskList.objects.create(board=board, listName=list_name)

        Achievements.objects.create(user = User.objects.get(username = data['username']))

                    # Create 30 tasks per board
                    for _ in range(30):
                        Task.objects.create(
                            list=task_list,
                            task_name=fake.sentence(),
                            task_description=fake.paragraph(),
                            due_date=fake.date_time_this_year(tzinfo=timezone.utc)
                        )
            print(f"Created private boards and tasks for user: {user}")"""


    
def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name.lower() + '.' + last_name.lower() + '@example.org'

