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
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateBoardForm, CreateTaskForm, EditTaskDescriptionForm, EditTaskNameForm, RemoveMemberForm, AddMemberForm, AssignTasksForm
from tasks.helpers import login_prohibited
from tasks.models import Board, TaskList, User, Teams, Task, TeamMembershipStatus



@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    current_boards = Board.objects.all().filter(team__members = current_user)
    current_boards.distinct()
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
            return render(request,'dashboard.html',{'user':current_user, 'boards': boards})
        else:
            return render(request, 'create_board.html', {'form':form})
    else:
        return render(request, 'create_board.html', {'form':form})


"""Display the Task Creation screen"""
def createTaskView(request, taskListID, board_name):
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
                    tasksList.append(task)
            return render(request, 'board.html', {'user': current_user, 'lists': lists, 'tasks': tasksList})
        else:
            return render(request, 'change_task_name.html', {'form': form})

    else:
        form = EditTaskNameForm(instance=task, initial={'board_name': board_name})
    return render(request, 'change_task_name.html', {'form': form})


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
                    tasksList.append(task)
            return render(request, 'board.html', {'user': current_user, 'lists': lists, 'tasks': tasksList})
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

        task = Task.objects.get(id=taskID)
        list = TaskList.objects.get(board=board_name, listName=new_list)
        task.list_id = list
        task.save()

        boardName = Task.objects.get(id=taskID).list.board.board_name
        # Redirect back to the page or wherever you want
        return HttpResponseRedirect(reverse('board', args=[boardName]))


def board(request, board_name):
    """Display specific board"""
    current_user = request.user
    current_board = Board.objects.get(board_name = board_name)
    current_team = current_board.team
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
                    tasksList.append(task)
            return render(request, 'board.html', {'user': current_user, 'lists': lists, 'tasks': tasksList,'permission_level':member_status.permission_level})
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
                tasksList.append(task)

        return render(request, 'board.html', {'user': current_user, 'lists': lists, 'tasks': tasksList,'permission_level':member_status.permission_level})

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

"""
def change_task_name(request):
    if request.method == 'POST':
        form = EditTaskNameForm(request.POST)
        if form.is_valid():
            # Process the form data 
            task_id = form.cleaned_data['task_id']
            new_name = form.cleaned_data['new_name']

            # Perform the task update logic 
            Task.objects.filter(id=task_id).update(task_name=new_name)
            
    else:
        form = EditTaskNameForm()

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
"""

def change_task_name(request):

    """Handles change in task name."""

    if request.method == 'POST':
        form = EditTaskNameForm(request.POST)
        if form.is_valid():
            # Process the form data 
            task_id = form.cleaned_data['task_id']
            new_name = form.cleaned_data['new_name']
    

            # Perform the task update logic :
            #Filters through the attributes of the task and updates the name
            Task.objects.filter(pk=task_id).update(task_name=new_name)

            
    else:
        form = EditTaskNameForm()

    #renders template, passes form object returns HTTP response
    return render(request, 'change_task_name.html', {'form': form})    

def change_task_description(request):

    """Handles change in task description."""

    if request.method == 'POST':
        form = EditTaskDescriptionForm(request.POST)
        if form.is_valid():
            # Process the form data 
            task_id = form.cleaned_data['task_id']
            new_description = form.cleaned_data['new_description']

            # Perform the task update logic
            # #Filters through the attributes of the task and updates the description 
            Task.objects.filter(pk=task_id).update(task_description=new_description)

            
    else:
        form = EditTaskDescriptionForm()

    #renders template, passes form object returns HTTP response

    return render(request, 'change_task_description.html', {'form': form})  


#def assign_tasks(request):
    #if request.method == 'POST':
        #form = AssignTasksForm(request.POST)
        #if form.is_valid():
            #selected_team_members = form.cleaned_data['team_members']
            #return render(request, 'task_assigned.html', {'selected_team_members': selected_team_members})
    #else:
        #form = TaskAssignmentForm()

    #return render(request, 'assign_task.html', {'form': form})


@login_required
def assign_tasks_view(request, taskID, board_name):
    redirect_to_home = False
    add_more_users = False
    form = AssignTasksForm()
    if request.method == 'POST':
        form = AssignTasksForm(request.POST)
        if form.is_valid():
            if 'redirect_to_home' in request.POST:
                redirect_to_home = True
            elif 'add_more_users' in request.POST:
                add_more_users = True
            if redirect_to_home or add_more_users:
                user = form.cleaned_data.get('username')
                user_object = User.objects.get(username = user)
                team_total = Board.objects.get(board_name = board_name).team
                team_members = list(team_total.members.all())
                assigned_members = list(Task.objects.get(pk=taskID).assigned_members.all())
                if user_object not in team_members or TeamMembershipStatus.objects.get(team=team_total,user= user_object).permission_level == 3:
                    messages.error(request, f"{user} is not a member of this board's team or is yet to fully join.")
                elif user_object in assigned_members:
                    messages.error(request,f"{user} is already assigned to this task.")
                else:
                    task = Task.objects.get(pk=taskID)
                    task.assigned_members.add(user_object)
                    task.save()
                    if redirect_to_home:
                        return redirect('/boards/' + board_name)  
                    if add_more_users:
                        return redirect('/assign_tasks/' + str(taskID) + "/" + board_name)
        else:
            context = generate_context(form,board_name,taskID)
            return render(request, 'assign_tasks.html', context)
                   
    context = generate_context(form,board_name,taskID)
    return render(request, 'assign_tasks.html', context)

def generate_context(form, board_name,taskID,error_msg = None):
    current_board = Board.objects.get(board_name=board_name)
    current_members_manager = TeamMembershipStatus.objects.filter(team=current_board.team)
    members = []
    membership_type = []
    for member in current_members_manager:
        members.append(member.user.username)
        if member.permission_level != 3:
            membership_type.append("Member")
        else:
            membership_type.append("Not yet joined")
    members_and_types = zip(members,membership_type)
    context = {
        'form' : form,
        'taskID': taskID,
        'board_name': board_name,
        'options': members_and_types,
        'error' : error_msg
    }
    return context


