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
    
    {'username': '@lewis', 'email': 'lewis.johnson@example.org', 'first_name': 'Lewis', 'last_name': 'Johnson'},
    {'username': '@hasan', 'email': 'hasan.johnson@example.org', 'first_name': 'Hasan', 'last_name': 'Johnson'},
    {'username': '@bruno', 'email': 'bruno.johnson@example.org', 'first_name': 'Bruno', 'last_name': 'Johnson'},
    {'username': '@adil', 'email': 'adil.johnson@example.org', 'first_name': 'Adil', 'last_name': 'Johnson'},
    {'username': '@fardeen', 'email': 'fardeen.johnson@example.org', 'first_name': 'Fardeen', 'last_name': 'Johnson'},
    
    {'username': '@user1', 'email': 'user1.johnson@example.org', 'first_name': 'user1', 'last_name': 'Johnson'},
    {'username': '@user2', 'email': 'user2.johnson@example.org', 'first_name': 'user2', 'last_name': 'Johnson'},
    {'username': '@user3', 'email': 'user3.johnson@example.org', 'first_name': 'user3', 'last_name': 'Johnson'},
    {'username': '@user4', 'email': 'user4.johnson@example.org', 'first_name': 'user4', 'last_name': 'Johnson'},
    {'username': '@user5', 'email': 'user5.johnson@example.org', 'first_name': 'user5', 'last_name': 'Johnson'},
    {'username': '@user6', 'email': 'alexa.johnson@example.org', 'first_name': 'user6', 'last_name': 'Johnson'},
    {'username': '@user7', 'email': 'olivia.johnson@example.org', 'first_name': 'user7', 'last_name': 'Johnson'},
    {'username': '@user8', 'email': 'ethan.johnson@example.org', 'first_name': 'user8', 'last_name': 'Johnson'},
    {'username': '@user9', 'email': 'emily.johnson@example.org', 'first_name': 'user9', 'last_name': 'Johnson'},
    {'username': '@user10', 'email': 'nathan.johnson@example.org', 'first_name': 'user10', 'last_name': 'Johnson'},
    {'username': '@user11', 'email': 'zoe.johnson@example.org', 'first_name': 'user11', 'last_name': 'Johnson'},
    {'username': '@user12', 'email': 'gabriel.johnson@example.org', 'first_name': 'user12', 'last_name': 'Johnson'},
    {'username': '@user13', 'email': 'sophie.johnson@example.org', 'first_name': 'user13', 'last_name': 'Johnson'},
    {'username': '@user14', 'email': 'mason.johnson@example.org', 'first_name': 'user14', 'last_name': 'Johnson'},
    {'username': '@user15', 'email': 'lily.johnson@example.org', 'first_name': 'user15', 'last_name': 'Johnson'},
    {'username': '@user16', 'email': 'aiden.johnson@example.org', 'first_name': 'user16', 'last_name': 'Johnson'},
    {'username': '@user17', 'email': 'mia.johnson@example.org', 'first_name': 'user17', 'last_name': 'Johnson'},
    {'username': '@user18', 'email': 'luke.johnson@example.org', 'first_name': 'user18', 'last_name': 'Johnson'},
    {'username': '@user19', 'email': 'ava.johnson@example.org', 'first_name': 'user19', 'last_name': 'Johnson'},
    {'username': '@user20', 'email': 'noah.johnson@example.org', 'first_name': 'user20', 'last_name': 'Johnson'}
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 50
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
            user_achievement = Achievements.objects.create(user=user)
            for i in range(30):
                user_achievement.increment_achievements("tasks_doing")
                user_achievement.increment_achievements("tasks_completed")
                
            for i in range(10):
                user_achievement.increment_achievements("boards_created")
                team = Teams.objects.create(author=user)
                team.members.add(user)
                board_name = f"{user.username}'s Board {i}"
                board = Board.objects.create(
                    author=user,
                    board_name=board_name,
                    board_type='Private',
                    team = team
                )
                
                for list_name in ['To Do', 'In Progress', 'Completed']:
                    task_list = TaskList.objects.create(board=board, listName=list_name)
                    
                    for _ in range(30):
                        user_achievement.increment_achievements("tasks_created")
                        Task.objects.create(
                            list=task_list,
                            task_name=fake.sentence(),
                            task_description=fake.paragraph(),
                            due_date=fake.date_time_this_year(tzinfo=timezone.utc)
                        )
                        
                        
        print("start test 2")
        
        john = users.get(username = "@johndoe")
        jane = users.get(username = "@janedoe")
        charlie = users.get(username = "@charlie")

        team = Teams.objects.create(author=john)
        team.members.add(john)
        team.members.add(jane)
        team.members.add(charlie)
        
        board_name = 'JohnDoes Team'
        board = Board.objects.create(
            author = john,
            board_name = board_name,
            board_type='Team',
            team = team
        )
        
        
        for list_name in ['To Do', 'In Progress', 'Completed']:
            task_list = TaskList.objects.create(board=board, listName=list_name)
            for _ in range(30):
                user_achievement.increment_achievements("tasks_created")
                user_achievement.increment_achievements("tasks_created")
                Task.objects.create(
                            list=task_list,
                            task_name=fake.sentence(),
                            task_description=fake.paragraph(),
                            due_date=fake.date_time_this_year(tzinfo=timezone.utc)
                        )
        
        hasan = users.get(username = "@hasan")
        lewis = users.get(username = "@lewis")
        bruno = users.get(username = "@bruno")
        fardeen = users.get(username = "@fardeen")
        adil = users.get(username = "@adil")

        team5= Teams.objects.create(author=lewis)
        team5.members.add(lewis)
        team5.members.add(fardeen)
        team5.members.add(adil)
        team5.members.add(bruno)
        team5.members.add(hasan)
        
        
        board_name = 'Team 5 '
        board = Board.objects.create(
            author = lewis,
            board_name = board_name,
            board_type='Team',
            team = team5
        )
        
        for list_name in ['To Do', 'In Progress', 'Completed']:
            task_list = TaskList.objects.create(board=board, listName=list_name)
            for _ in range(30):
                user_achievement.increment_achievements("tasks_created")
                Task.objects.create(
                            list=task_list,
                            task_name=fake.sentence(),
                            task_description=fake.paragraph(),
                            due_date=fake.date_time_this_year(tzinfo=timezone.utc)
                        )
        
        
        for i in range(1, 21):
            
            username = f"@user{i}"
            user = users.get(username=username)

                # Create a team for each user
            team20 = Teams.objects.create(author=user)
            team20.members.add(user)

        board = Board.objects.create(
            author=user,
            board_name= "team20",
            board_type='Team',
            team=team20)
        
        for list_name in ['To Do', 'In Progress', 'Completed']:
            task_list = TaskList.objects.create(board=board, listName=list_name)
            for _ in range(30):
                user_achievement.increment_achievements("tasks_created")
                Task.objects.create(
                            list=task_list,
                            task_name=fake.sentence(),
                            task_description=fake.paragraph(),
                            due_date=fake.date_time_this_year(tzinfo=timezone.utc)
                        )
        
              
def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name.lower() + '.' + last_name.lower() + '@example.org'

