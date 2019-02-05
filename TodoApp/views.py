from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from . import models


@login_required
def index(request):
    """Home page that displays active TodoLists and their related information."""

    appStatus = ""
    if request.method == "GET":
        pass
    elif request.POST["submit"] == "Create":
        listName = request.POST['listName']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
        else:
            try:
                models.TodoList.objects.create(name=listName, todoCount=0, doneCount=0)
                appStatus = "New TodoList created successfully."
            except IntegrityError:
                appStatus = "Create operation failed. Please make sure that your TodoList name " \
                            "does not exist in current TodoLists"
    elif request.POST["submit"] == "Delete":
        listName = request.POST['listName']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
        else:
            try:
                models.TodoList.objects.get(name=listName).delete()
                appStatus = "Specified TodoList deleted successfully."
            except models.TodoList.DoesNotExist:
                appStatus = "Delete operation failed. Please make sure that your TodoList name " \
                            "exists in current TodoLists"

    todoList = models.TodoList.objects.all()
    return render(request, "index.html", {"todoLists": todoList, "status": appStatus})


