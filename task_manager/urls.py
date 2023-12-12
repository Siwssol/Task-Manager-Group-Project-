"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('create_board/',views.create_board_view,name='create_board_view'),
    path('boards/<str:board_name>', views.board, name='board'),
    path('change-task-description/<int:taskID>/<str:board_name>/', views.change_task_description, name='change_task_description'),
    path('change-task-name/<int:taskID>/<str:board_name>/', views.change_task_name, name='change_task_name'),
    path('createTask/<int:taskListID>/<str:board_name>/', views.createTaskView, name='createTask'),
    path('board/<str:board_name>/add_member/', views.add_member_to_board, name='add_member_to_board'),
]

# Leaving this here until error has been fixed
path('change-task-name/', views.change_task_description, name='change_task_description'),
path('change-task-name/', views.change_task_name, name='change_task_name'),