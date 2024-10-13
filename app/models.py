from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    client_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    def __str__(self):
        return self.client_name



class Project(models.Model):
    project_name=models.CharField(max_length=50)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,related_name="projects")
    users=models.ManyToManyField(User,related_name="assigned_projects")
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.CharField(max_length=100)

    def __str__(self):
        return self.project_name