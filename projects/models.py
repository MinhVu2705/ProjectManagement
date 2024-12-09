from django.db import models
from django.contrib.auth.models import User  # Sử dụng User model của Django

# Create your models here.
from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Mở'),
        ('closed', 'Đóng'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Tên dự án")
    description = models.TextField(verbose_name="Mô tả")
    status = models.CharField(choices=STATUS_CHOICES, default='open', max_length=50, verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('not started', 'Chưa bắt đầu'),
        ('in progress', 'Đang làm'),
        ('completed', 'Hoàn thành'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Tên nhiệm vụ")
    description = models.TextField(verbose_name="Mô tả nhiệm vụ")
    status = models.CharField(choices=STATUS_CHOICES, default='not started', max_length=50, verbose_name="Trạng thái")
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người được phân công")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name="Dự án")
    due_date = models.DateTimeField(verbose_name="Ngày hết hạn")
    
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    
    def __str__(self):
        return self.title