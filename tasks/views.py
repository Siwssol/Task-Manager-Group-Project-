from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateBoardForm, CreateTaskForm, EditTaskDescriptionForm, EditTaskNameForm
from tasks.helpers import login_prohibited
from .models import Board, TaskList
from tasks.models import Board, TaskList, User, Teams, Task, TeamMembershipStatus

#
from tasks.forms import AddMemberForm
from tasks.forms import RemoveMemberForm

@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    current_boards = Board.objects.all().filter(team__members = current_user)
    current_boards.distinct()
    for i in current_boards:
        print(i)
    return render(request, 'dashboard.html', {'user': current_user, 'boards' : current_boards})

@login_required
def create_board_view(request):
    """ Display board creation screen"""
    form = CreateBoardForm()
    if request.method == 'POST':
        current_user = request.user
        form = CreateBoardForm(request.POST)
        if form.is_valid():
            board_name = form.cleaned_data.get('board_name')
            board_type = form.cleaned_data.get('board_type')
            board_members = form.cleaned_data.get('team_emails')
            """ Create Team based on user input"""
            emails = form.emails_to_python()
            if board_type == 'Team':
                created_team = Teams.objects.create(author = current_user)
                TeamMembershipStatus.objects.create(team = created_team, user = current_user, permission_level = TeamMembershipStatus.Permissions.OWNER)
                for em in emails:
                    usr = User.objects.get(email = em)
                    TeamMembershipStatus.objects.create(team = created_team, user = usr)
            else:
                """A private team will have a single member team. This could allow for future ability to implement change from private -> team """
                created_team = Teams.objects.create(author = current_user)
                TeamMembershipStatus.objects.create(team = created_team, user = current_user, permission_level = TeamMembershipStatus.Permissions.OWNER)
            board = Board.objects.create(author=current_user, board_name = board_name,
                                          board_type=board_type, team_emails = board_members,
                                          team = created_team)
            TaskList.objects.create(board = board, listName="To Do")
            TaskList.objects.create(board = board, listName="In Progress")
            TaskList.objects.create(board = board, listName="Completed")
            boards = Board.objects.all().filter(team__members = current_user)
            return redirect('/dashboard/')
        else:
            return render(request, 'create_board.html', {'form':form})
    else:
        return render(request, 'create_board.html', {'form':form})


"""Display the Task Creation screen"""
@login_required
def createTaskView(request, taskListID, board_name):
    print(taskListID)
    taskList = TaskList.objects.get(pk = taskListID)
    form = CreateTaskForm()

    print(request.method)
    # TEMP COMMENT
    # TEMP COMMENT 2
    if request.method == 'POST':
        current_user = request.user
        form = CreateTaskForm(request.POST)
        # print("Have entered this if statement")
        if form.is_valid():
            #print("Task created")
            task_name = form.cleaned_data.get('task_name')
            task_description = form.cleaned_data.get('task_description')
            due_date = form.cleaned_data.get('due_date')
            lists = TaskList.objects.all().filter(board=board_name)
            task = Task.objects.create(list = taskList, task_name = task_name, task_description = task_description, due_date = due_date)
            #print(task.task_name, task.task_description)
            tasksList = []
            for list in lists:
                tasks = Task.objects.all().filter(list=list)
                for task in tasks:
                    print(task)
                    tasksList.append(task)

            """Debugging print statements
            for task in tasks:
                print(task.task_name)
            for list in lists:
                print(list)
            """
            return redirect('/boards/' + board_name)
        else:
            return render(request, 'createTask.html', {'form': form})
    else:
        return render(request, 'createTask.html', {'form':form})

@login_required
def change_task_name(request, taskID, board_name):
    task = get_object_or_404(Task, id=taskID)
    if request.method == 'POST':
        current_user = request.user
        form = EditTaskNameForm(request.POST, instance=task, initial={'board_name': board_name})
        if form.is_valid():
            # Process the form data
            new_name = form.cleaned_data['new_name']
            # Perform the task update logic
            Task.objects.filter(id=taskID).update(task_name=new_name)
            lists = TaskList.objects.all().filter(board=board_name)
            tasksList = []
            for list in lists:
                tasks = Task.objects.all().filter(list=list)
                for task in tasks:
                    print(task)
                    tasksList.append(task)
            return redirect('/boards/' + board_name)
        else:
            return render(request, 'change_task_name.html', {'form': form})

    else:
        form = EditTaskNameForm(instance=task, initial={'board_name': board_name})
    return render(request, 'change_task_name.html', {'form': form})

@login_required
def change_task_description(request, taskID, board_name):
    task = get_object_or_404(Task, id=taskID)
    if request.method == 'POST':
        current_user = request.user
        form = EditTaskDescriptionForm(request.POST, instance=task, initial={'board_name': board_name})
        if form.is_valid():
            # Process the form data
            new_description = form.cleaned_data['new_description']
            # Perform the task update logic
            Task.objects.filter(id=taskID).update(task_description=new_description)
            lists = TaskList.objects.all().filter(board=board_name)
            tasksList = []
            for list in lists:
                tasks = Task.objects.all().filter(list=list)
                for task in tasks:
                    print(task)
                    tasksList.append(task)
            return redirect('/boards/' + board_name)
        else:
            return render(request, 'change_task_description.html', {'form': form})

    else:
        form = EditTaskDescriptionForm(instance=task, initial={'board_name': board_name})
    return render(request, 'change_task_description.html', {'form': form})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""
    return render(request, 'home.html')


def achievements(request):
    current_user = request.user
    return render(request, 'achievements.html', {'user': current_user})

def updateTaskLocation(request, taskID, board_name):
    if request.method == 'POST':
        new_list = request.POST.get('new_list')
        print("SOMETHING" ,new_list)
        print(f"Task ID: {taskID}, New List Name: {new_list}")

        # Your logic to update the task sand move it to the new list goes here
        task = Task.objects.get(id=taskID)
        list = TaskList.objects.get(board=board_name, listName=new_list)
        print(list)
        task.list_id = list
        task.save()

        boardName = Task.objects.get(id=taskID).list.board.board_name
        # Redirect back to the page or wherever you want
        return HttpResponseRedirect(reverse('board', args=[boardName]))

@login_required
def board(request, board_name):
    """Display specific board"""
    current_user = request.user
    current_board = Board.objects.get(board_name = board_name)
    current_team = current_board.team    
    
    #changed
    board_members = current_board.team.members.all()

    ###
    
    if request.method == 'POST':
        # check if board overlay was interacted with or not
        # CODE NEEDS TO BE REFACTORED HERE DUE TO DUPLICATION
        if 'accepted' in request.POST:
            # Change user membership level and let them access board normally.
            team_membership_obj = TeamMembershipStatus.objects.get(team = current_team, user = current_user)
            team_membership_obj.permission_level = TeamMembershipStatus.Permissions.MEMBER
            team_membership_obj.save()
            member_status = TeamMembershipStatus.objects.get(team = current_team, user = current_user)
            lists = TaskList.objects.all().filter(board = board_name)
            tasksList = []
            for list in lists:
                tasks = Task.objects.all().filter(list = list)
                for task in tasks:
                    print(task)
                    tasksList.append(task)
            return render(request, 'board.html', {'user': current_user, 'lists': lists, 'tasks': tasksList,'permission_level':member_status.permission_level, "board_members": board_members})
        elif 'rejected' in request.POST:
            # remove user's association from the board if they choose to not be a part of it.
            team_membership_obj = TeamMembershipStatus.objects.get(team = current_team, user = current_user)            
            current_team.members.remove(current_user)  
            team_membership_obj.delete()
            boards = Board.objects.filter(team__members = current_user)
            return render(request,'dashboard.html',{'user':current_user, 'boards': boards})
    else:
        # if user did not send post request (did not press accept or reject), display the board as normal.    
        member_status = TeamMembershipStatus.objects.get(team = current_team, user = current_user)
        lists = TaskList.objects.all().filter(board = board_name)
        tasksList = []
        for list in lists:
            tasks = Task.objects.all().filter(list = list)
            for task in tasks:
                print(task)
                tasksList.append(task)

        return render(request, 'board.html', {'user': current_user, 'lists': lists, 'tasks': tasksList,'permission_level':member_status.permission_level, "board_name":board_name, "board_members": board_members})

class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)




class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    

@login_required
def add_member_to_board(request, board_name):
    usr = request.user
    board = get_object_or_404(Board, board_name= board_name)
    current_team = board.team
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if board.team.members.filter(id=user.id).exists():
                    messages.error(request, "User is already a member of this board.")
                else:
                    TeamMembershipStatus.objects.create(team = current_team, user = user)
                    messages.success(request, "Member added successfully.")
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    # In your add_member_to_board view
    return redirect(reverse('board', kwargs={'board_name': board_name}))



@login_required
def remove_member_from_board(request, board_name):
    current_user = request.user
    board = get_object_or_404(Board, board_name=board_name)
    if not board.author == current_user:
        messages.error(request, "Only the board owner can remove members.")
        return redirect(reverse('board', kwargs={'board_name': board_name}))

    if request.method == 'POST':
        form = RemoveMemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user_to_remove = User.objects.get(email=email)
                if user_to_remove == board.author:
                    messages.error(request, "You cannot remove yourself from the board.")
                elif board.team.members.filter(id=user_to_remove.id).exists():
                    board.team.members.remove(user_to_remove)
                    messages.success(request, "Member removed successfully.")
                else:
                    messages.error(request, "User is not a member of this board.")
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    return redirect(reverse('board', kwargs={'board_name': board_name}))


@login_required
def delete_board(request, board_name):
    board = get_object_or_404(Board, board_name=board_name)

    # Check if the current user is the author of the board
    if request.user != board.author:
        messages.error(request, "You do not have permission to delete this board.")
        return redirect(reverse('board', kwargs={'board_name': board_name}))

    # Perform deletion
    board.delete()
    messages.success(request, "Board deleted successfully.")
    return redirect('dashboard')





#def assign_tasks(request):
    #if request.method == 'POST':
        #form = AssignTasksForm(request.POST)
        #if form.is_valid():
            #selected_team_members = form.cleaned_data['team_members']
            #return render(request, 'task_assigned.html', {'selected_team_members': selected_team_members})
    #else:
        #form = TaskAssignmentForm()

    #return render(request, 'assign_task.html', {'form': form})





