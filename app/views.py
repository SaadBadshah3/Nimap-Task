from django.shortcuts import render
from .models import Client,Project
from .serializers import ClientSerializer,ProjectSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class LP(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=Client.objects.all()
    serializer_class=ClientSerializer
    permission_classes=[IsAuthenticated]


    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Rud(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset=Client.objects.all()
    serializer_class=ClientSerializer
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProjectView(GenericAPIView,CreateModelMixin):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    permission_classes=[IsAuthenticated]


    def post(self,request,client_id,*args,**kwargs):
        client=Client.objects.get(id=client_id)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client,created_by=self.request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserProject(GenericAPIView,ListModelMixin):
    serializer_class=ProjectSerializer
    permission_classes=[IsAuthenticated]


    def get_queryset(self):
        print(self.request.user)  # Log the current user
        queryset = self.request.user.assigned_projects.all()  # Get the assigned projects
        print(queryset)  # Log the returned queryset
        return queryset

    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)        