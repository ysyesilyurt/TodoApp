from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F, Max
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
                newListId = models.TodoList.objects.count()
                models.TodoList.objects.create(name=listName, todoCount=0, doneCount=0, listId=newListId)
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


@login_required
def items(request, listID=None):
    """List item page that displays entries and related information that specified TodoList contains."""

    appStatus = ""
    if request.method == "GET":
        pass
    elif request.POST["submit"] == "Create":
        itemContent = request.POST['itemContent']
        itemImportance = request.POST['itemImportance']
        if itemContent == "":
            appStatus = "Please specify what you need to do."
        else:
            if itemImportance == "":
                appStatus = "Please choose a valid importance level."
            else:
                lastItemId = models.TodoItem.objects.filter(belongingList_id=listID).aggregate(Max('itemId'))['itemId__max']
                if lastItemId is None:
                    newItemId = 0
                else:
                    newItemId = lastItemId + 1
                models.TodoList.objects.filter(listId=listID).update(todoCount=F('todoCount') + 1)
                models.TodoItem.objects.create(itemId=newItemId, content=itemContent, done="Nope",
                                               importance=itemImportance, belongingList_id=listID)
                appStatus = "New Todo created successfully."

    elif request.POST["submit"] == "Delete":
        todoId = request.POST['itemID']
        if todoId == "":
            appStatus = "Please choose a valid Todo"
        else:
            try:
                models.TodoItem.objects.filter(belongingList_id=listID, itemId=todoId).delete()
                models.TodoList.objects.filter(listId=listID).update(todoCount=F('todoCount') - 1)
                appStatus = "Specified Todo deleted successfully."
            except models.TodoList.DoesNotExist:
                appStatus = "Delete operation failed. Please make sure that Todo ID" \
                            "exists in current Todo items"

    elif request.POST["submit"] == "Mark as Done":
        todoId = request.POST['itemID']
        if todoId == "":
            appStatus = "Please choose a valid Todo"
        else:
            try:
                models.TodoItem.objects.filter(belongingList_id=listID, itemId=todoId).update(done="Yes!")
                models.TodoList.objects.filter(listId=listID).update(doneCount=F('doneCount') + 1)
                appStatus = "Specified Todo marked as done successfully."
            except models.TodoList.DoesNotExist:
                appStatus = "Marking operation failed. Please make sure that Todo ID" \
                            "exists in current Todo items"

    elif request.POST["submit"] == "Mark as Undone":
        todoId = request.POST['itemID']
        if todoId == "":
            appStatus = "Please choose a valid Todo"
        else:
            try:
                models.TodoItem.objects.filter(belongingList_id=listID, itemId=todoId).update(done="Nope")
                models.TodoList.objects.filter(listId=listID).update(doneCount=F('doneCount') - 1)
                appStatus = "Specified Todo marked as undone successfully."
            except models.TodoList.DoesNotExist:
                appStatus = "Marking operation failed. Please make sure that Todo ID" \
                            "exists in current Todo items"

    todos = models.TodoItem.objects.filter(belongingList_id=listID)
    doneTodos = models.TodoItem.objects.filter(done="Yes!")
    return render(request, "items.html", {"todos": todos, "doneTodos": doneTodos , "status": appStatus})
