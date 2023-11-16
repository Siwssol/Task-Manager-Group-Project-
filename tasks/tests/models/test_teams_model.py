"""Unit tests for the Team model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User
from tasks.models import Teams

class Teammodeltestcase(TestCase):
    """unit tests for the teams model"""
    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.team = Teams()
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')

    def test_add_user(self):
        self.team.add_user(self.user)
        self.assertIn(self.user, self.team.teammembers)
        self.assertIn('owner', self.team.teampermissions)

    def test_invite_user_valid_role(self):
        self.team.add_user(self.user)
        self.team.invite_user(self.user2, 'admin')
        self.assertIn(self.user, self.team.teammembers)
        self.assertIn(self.user2, self.team.teammembers)
        self.assertIn('owner', self.team.teampermissions)
        self.assertIn('admin', self.team.teampermissions)

    def test_invite_user_owner_role(self):
        self.team.add_user(self.user)
        self.team.invite_user(self.user2, 'owner')
        self.assertIn(self.user, self.team.teammembers)
        self.assertIn(self.user2, self.team.teammembers)
        self.assertIn('owner', self.team.teampermissions)
        self.assertNotIn('owner', self.team.teampermissions)

    def test_invite_user_invalid_role(self):
        self.team.add_user(self.user)
        self.team.invite_user(self.user2, 'invalid_role')
        self.assertNotIn(self.user2, self.team.teammembers)
        self.assertNotIn('invalid_role', self.team.teampermissions)

    def test_change_ownership_valid(self):
        self.team.add_user(self.user)
        self.team.add_user(self.user2)
        self.team.teampermissions = ['owner', 'admin']

        self.team.change_ownership(self.user, self.user2)
        self.assertNotIn('owner', self.team.teampermissions)
        self.assertIn(self.user, self.team.teammembers)
        self.assertIn(self.user2, self.team.teammembers)
        self.assertIn('admin', self.team.teampermissions)

    def test_change_ownership_invalid_current_owner(self):
        self.team.add_user(self.user)
        self.team.teampermissions = ['owner']
        # Attempting to change ownership without the current owner's permission
        self.team.teampermissions = ['admin', 'member']
        with self.assertRaises(ValueError):
            self.team.change_ownership(self.user, self.user2)

    def test_change_ownership_invalid_target_owner(self):
        self.team.add_user(self.user)
        self.team.teampermissions = ['owner']
        # Attempting to change ownership to a user who is not in the team
        non_team_member = User.objects.get(username='@testuser')
        with self.assertRaises(ValueError):
            self.team.change_ownership(self.user_owner, non_team_member)\
    
    def test_change_perms_valid(self):
        self.team.add_user(self.user)
        self.team.add_user(self.user2)
        
        self.team.change_perms(self.user2, 'member')
        self.assertIn(self.user2, self.team.teammembers)
        self.assertIn('owner', self.team.teampermissions)
        self.assertIn('member', self.team.teampermissions)

    def test_change_perms_invalid_owner(self):
        self.team.add_user(self.user)
        self.team.add_user(self.user2)
        with self.assertRaises(ValueError):
            self.team.change_perms(self.user, 'admin')

    def test_change_perms_invalid_role(self):
        self.team.add_user(self.user)
        self.team.add_user(self.user2)
        with self.assertRaises(ValueError):
            self.team.change_perms(self.user_admin, 'invalid_role')

    def test_change_perms_invalid_user(self):
        non_team_member = User.objects.get(username='@testuser')
        with self.assertRaises(ValueError):
            self.team.change_perms(non_team_member, 'member')