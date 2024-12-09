"""
URL configuration for project_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# projects/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),  # Trang danh sách dự án
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),  # Chi tiết dự án
    path('create_project/', views.create_project, name='create_project'),  # Tạo dự án mới
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),  # Xóa dự án
    path('project/<int:project_id>/create_task/', views.create_task, name='create_task'),  # Tạo công việc
    path('project/<int:project_id>/task/', views.task_list, name='task_list'),  # Danh sách công việc của dự án
    path('project/<int:project_id>/task/<int:task_id>/delete/', views.delete_task, name='delete_task'),  # Xóa công việc
]
