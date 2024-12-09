# projects/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, Task
from .forms import ProjectForm, TaskForm

def project_list(request):
    search_query = request.GET.get('search', '')  # Lấy từ khóa tìm kiếm
    if search_query:
        projects = Project.objects.filter(name__icontains=search_query)  # Tìm kiếm theo tên
    else:
        projects = Project.objects.all()
    
    return render(request, 'projects/project_list.html', {'projects': projects, 'search_query': search_query})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dự án đã được tạo thành công.')
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form})

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, 'Dự án đã bị xóa thành công.')
    return redirect('project_list')

def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    status_filter = request.GET.get('status', '')  # Lọc công việc theo trạng thái
    
    if status_filter:
        tasks = Task.objects.filter(project=project, status=status_filter)
    else:
        tasks = Task.objects.filter(project=project)
    
    return render(request, 'projects/task_list.html', {'tasks': tasks, 'project': project, 'status_filter': status_filter})

def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, 'Công việc đã được tạo thành công.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'projects/create_task.html', {'form': form, 'project': project})

def delete_task(request, project_id, task_id):
    task = get_object_or_404(Task, id=task_id, project_id=project_id)
    task.delete()
    messages.success(request, 'Công việc đã bị xóa thành công.')
    return redirect('project_detail', project_id=project_id)
