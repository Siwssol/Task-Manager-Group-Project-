from django.core.management.base import BaseCommand, CommandError
from tasks.models import User, Teams, Board, TaskList, Task
import pytz
from faker import Faker
from random import randint, random
from django.utils import timezone

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
        for i in range(10):  
            team = Teams.objects.create(author=User.objects.first())
            board_name = f"Board_{i}"  # unique name for each board
            board = Board.objects.create(author=User.objects.first(), board_name=board_name, team=team)
            print(f"Created board '{board_name}' for team {team}")
            # Create task lists
            for list_name in ['To-Do', 'In Progress', 'Done']: 
                task_list = TaskList.objects.create(board=board, listName=list_name)
                print(f"Created task list '{list_name}' for board '{board_name}'")

                #create task
                for _ in range(15): 
                    task = Task.objects.create(
                        list=task_list,
                        task_name=fake.sentence(),
                        task_description=fake.paragraph(),
                        due_date=fake.date_time_this_year(tzinfo=timezone.utc)
                    )
                    print(f"Created task '{task.task_name}' for task list '{list_name}' in board '{board_name}'")

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name.lower() + '.' + last_name.lower() + '@example.org'

