from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json

task_list = [
    {
    "id": 1,
    "title": "Create a new project",
    "description": "Create a new project using Magic",
    "completed": False
  }
]

# Create your views here.
@api_view(["GET", "POST"])
def tasks(request):
    
    if request.method == "GET":
        return Response({"tasks": task_list}, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        print(request.data)
        task_list.append(request.data)
        return Response({"tasks": task_list}, status=status.HTTP_201_CREATED)
