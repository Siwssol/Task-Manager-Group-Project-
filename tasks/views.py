from django.conf import settings
from django.http import HttpResponse
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
from tasks.models import Board, TaskList, User, Teams, Task

@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    current_boards = Board.objects.all().filter(author=current_user)
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
                created_team.members.add(current_user)
                for em in emails:
                    usr = User.objects.get(email = em)
                    created_team.members.add(usr)
            else:
                """A private team will have a single member team. This could allow for future ability to implement change from private -> team """
                created_team = Teams.objects.create(author = current_user)
                created_team.members.add(current_user)
            board = Board.objects.create(author=current_user, board_name = board_name,
                                          board_type=board_type, team_emails = board_members,
                                          team = created_team)
            TaskList.objects.create(board = board, listName="To Do")
            TaskList.objects.create(board = board, listName="In Progress")
            TaskList.objects.create(board = board, listName="Completed")
            boards = Board.objects.all()
            return render(request,'dashboard.html',{'user':current_user, 'boards': boards})
        else:
            return render(request, 'create_board.html', {'form':form})
    else:
        return render(request, 'create_board.html', {'form':form})


"""Display the Task Creation screen"""
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
            return render(request, 'board.html',{'user': current_user,'lists': lists, 'tasks': tasksList})
        else:
            return render(request, 'createTask.html', {'form': form})
    else:
        return render(request, 'createTask.html', {'form':form})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""
    return render(request, 'home.html')

def board(request, board_name):
    """Display specific board"""
    current_user = request.user
    lists = TaskList.objects.all().filter(board = board_name)
    tasksList = []
    for list in lists:
        tasks = Task.objects.all().filter(list = list)
        for task in tasks:
            print(task)
            tasksList.append(task)

    return render(request, 'board.html', {'user': current_user, 'lists': lists, 'tasks': tasksList})

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


def change_task_name(request, taskID):
    form = EditTaskNameForm()
    if request.method == 'POST':
        form = EditTaskNameForm(request.POST)
        if form.is_valid():
            # Process the form data 
            task_id = form.cleaned_data['task_id']
            new_name = form.cleaned_data['new_name']

            # Perform the task update logic 
            Task.objects.filter(id=task_id).update(task_name=new_name)
        else:
            return render(request, 'change_task_name.html', {'form': form})

    else:
        return render(request, 'change_task_name.html', {'form': form})



def change_task_description(request):
    if request.method == 'POST':
        form = EditTaskDescriptionForm(request.POST)
        if form.is_valid():
            # Process the form data 
            task_id = form.cleaned_data['task_id']
            new_description = form.cleaned_data['new_description']

            # Perform the task update logic 
            Task.objects.filter(id=task_id).update(task_name=new_description)

            
    else:
        form = EditTaskDescriptionForm()

    return render(request, 'change_task_description.html', {'form': form})  


