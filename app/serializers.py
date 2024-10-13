from rest_framework import serializers
from .models import Client,Project
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username"]




class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields=["id","client_name","created_at","created_by"]
        read_only_fields=["created_at","created_by"]



class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)  # Read-only, returns list of user info (id and username)
    user_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), write_only=True)  # For assigning users by ID
    client = serializers.CharField(source='client.client_name', read_only=True)  # Show 'client_name' instead of 'client' ID

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'user_ids', 'created_at', 'created_by']  # Include client as name, users with details

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids')  # Pop user_ids from validated_data
        project = Project.objects.create(**validated_data)  # Create project with remaining data
        project.users.set(user_ids)  # Assign users to the project using the provided user IDs
        return project