import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models


@login_required
def index(request):
    """Home page view that displays active TodoLists and their related information along with available operations."""

    result = ""
    appStatus = ""

    if request.method == "GET":
        todoLists = models.TodoList.objects.filter(owner=request.user)
        return render(request, "index.html", {"todoLists": todoLists})

    elif request.POST["submit"] == "listSort":
        listName = request.POST['listName']
        newIndex = request.POST['newIndex']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
        else:
            try:
                todoList = models.TodoList.objects.filter(owner=request.user).get(name=listName)
                todoList.to(int(newIndex))
            except models.TodoList.DoesNotExist:
                appStatus = "Sorting operation failed. Please make sure that your TodoList name " \
                            "exists in current TodoLists"
                result = "Fail"

    elif request.POST["submit"] == "Create":
        listName = request.POST['listName']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
            result = "Fail"
        elif models.TodoList.objects.filter(owner=request.user, name=listName).exists():
            # User can not create 2 TodoLists with same name
            appStatus = "Please choose a TodoList name which does not exists in your current set of TodoLists."
            result = "Fail"
        else:
            try:
                if models.TodoList.objects.count() == 0:
                    newListId = 0
                else:
                    newListId = models.TodoList.objects.latest('listId').listId + 1
                models.TodoList.objects.create(name=listName, todoCount=0, doneCount=0,
                                               listId=newListId, owner=request.user)
            except IntegrityError:
                appStatus = "Create operation failed. Please make sure that your TodoList name " \
                            "does not exist in current TodoLists"
                result = "Fail"

    elif request.POST["submit"] == "Delete":
        listName = request.POST['listName']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
        else:
            try:
                models.TodoList.objects.filter(owner=request.user).get(name=listName).delete()
            except models.TodoList.DoesNotExist:
                appStatus = "Delete operation failed. Please make sure that your TodoList name " \
                            "exists in current TodoLists"
                result = "Fail"

    elif request.POST["submit"] == "Edit":
        listName = request.POST['listName']
        newName = request.POST['newName']
        try:
            models.TodoList.objects.filter(owner=request.user, name=listName).update(name=newName)
        except IntegrityError:
            appStatus = "Edit operation failed. Please make sure that your TodoList name " \
                        "does not exists in current TodoLists"
            result = "Fail"

    if result == "":
        result = "Success"
    todoLists = models.TodoList.objects.filter(owner=request.user)
    return responseTodoLists(result, appStatus, todoLists)


@login_required
def todos(request, listID=None):
    """TodoItem page view that displays related TodoItems and their information, which specified TodoList contains,
    along with the available operations."""

    result = ""
    appStatus = ""
    listName = models.TodoList.objects.filter(owner=request.user, listId=listID).values('name')[0]['name']

    if request.method == "GET":
        todos = models.TodoItem.objects.filter(belongingList_id=listID, done=False)
        doneTodos = models.TodoItem.objects.filter(belongingList_id=listID, done=True)
        return render(request, "todos.html", {"todos": todos, "doneTodos": doneTodos, "listName": listName})

    elif request.POST["submit"] == "itemSort":
        itemContent = request.POST['itemContent']
        newIndex = request.POST['newIndex']
        try:
            item = models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent)[0]
            item.to(int(newIndex))
        except models.TodoItem.DoesNotExist:
            appStatus = "Sorting operation failed, no TodoItem seems to exist as not done with this content."
            result = "Fail"

    elif request.POST["submit"] == "doneItemSort":
        itemContent = request.POST['itemContent']
        newIndex = request.POST['newIndex']
        try:
            item = models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent, done=True)[0]
            item.to(int(newIndex))
        except models.TodoItem.DoesNotExist:
            appStatus = "Deleting all operation failed, no TodoItem seems to exist as done with this content."
            result = "Fail"

    elif request.POST["submit"] == "Create":
        itemContent = request.POST['itemContent']
        if itemContent == "":
            appStatus = "Please specify a valid Todo."
            result = "Fail"
        else:
            try:
                models.TodoItem.objects.create(content=itemContent, done=False, belongingList_id=listID)
                models.TodoList.objects.filter(listId=listID, owner=request.user).update(todoCount=F('todoCount') + 1)
            except IntegrityError:
                appStatus = "Create operation failed. Please make sure that your Todo content " \
                            "does not exist in current or done Todos."
                result = "Fail"

    elif request.POST["submit"] == "Delete":
        itemContent = request.POST['itemContent']
        if itemContent == "":
            appStatus = "Need a valid Todo item."
            result = "Fail"
        else:
            try:
                models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent).delete()
                models.TodoList.objects.filter(listId=listID, owner=request.user).update(todoCount=F('todoCount') - 1)
                models.TodoList.objects.filter(listId=listID, owner=request.user).update(doneCount=F('doneCount') - 1)
            except models.TodoItem.DoesNotExist:
                appStatus = "Delete operation failed. Please make sure that selected Todo " \
                            "exists in current Todo items."
                result = "Fail"

    elif request.POST["submit"] == "Undone":
        itemContent = request.POST['itemContent']
        if itemContent == "":
            appStatus = "Need a valid Todo item."
            result = "Fail"
        else:
            try:
                models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent).update(done=False)
                models.TodoList.objects.filter(listId=listID, owner=request.user).update(doneCount=F('doneCount') - 1)
            except models.TodoItem.DoesNotExist:
                appStatus = "Marking operation failed. Please make sure that selected Todo " \
                            "exists in current Todo items."
                result = "Fail"

    elif request.POST["submit"] == "Edit":
        itemContent = request.POST['itemContent']
        newContent = request.POST['newContent']
        try:
            models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent).update(content=newContent)
        except IntegrityError:
            appStatus = "Create operation failed. Please make sure that your new Todo content " \
                        "does not exist in current or done Todos."
            result = "Fail"

    elif request.POST["submit"] == "Mark as Done":
        itemContent = request.POST['itemContent']
        if itemContent == "":
            appStatus = "Need a valid Todo item."
            result = "Fail"
        else:
            try:
                models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent).update(done=True)
                models.TodoList.objects.filter(listId=listID, owner=request.user).update(doneCount=F('doneCount') + 1)
            except models.TodoItem.DoesNotExist:
                appStatus = "Marking operation failed. Please make sure that selected Todo " \
                            "exists in current Todo items."
                result = "Fail"

    elif request.POST["submit"] == "Mark all as Done":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID).update(done=True)
            models.TodoList.objects.filter(listId=listID, owner=request.user).update(doneCount=F('todoCount'))
        except models.TodoItem.DoesNotExist:
            appStatus = "Marking operation failed, no TodoItem seems to exist as undone."
            result = "Fail"

    elif request.POST["submit"] == "Mark all as Undone":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID).update(done=False)
            models.TodoList.objects.filter(listId=listID, owner=request.user).update(doneCount=0)
        except models.TodoItem.DoesNotExist:
            appStatus = "Marking operation failed, no TodoItem seems to exist as done."
            result = "Fail"

    elif request.POST["submit"] == "Delete all Done":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID, done=True).delete()
            models.TodoList.objects.filter(listId=listID, owner=request.user).update(todoCount=F('todoCount') - F('doneCount'))
            models.TodoList.objects.filter(listId=listID, owner=request.user).update(doneCount=0)
        except models.TodoItem.DoesNotExist:
            appStatus = "Deleting all operation failed, no TodoItem seems to exist as done."
            result = "Fail"

    elif request.POST["submit"] == "Delete all Undone":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID, done=False).delete()
            models.TodoList.objects.filter(listId=listID, owner=request.user).update(todoCount=F('doneCount'))
        except models.TodoItem.DoesNotExist:
            appStatus = "Deleting all operation failed, no TodoItem seems to exist as done."
            result = "Fail"

    if result == "":
        result = "Success"
    todos = models.TodoItem.objects.filter(belongingList_id=listID, done=False)
    doneTodos = models.TodoItem.objects.filter(belongingList_id=listID, done=True)
    return responseTodos(result, appStatus, todos, doneTodos, listName)


def signup(request):
    """SignUp page view that signs up new user to the system, according to given information."""

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return redirect('index')
        except IntegrityError:
            appStatus = "Oops! It seems like this username is taken, please choose another username."
            return render(request, 'signup.html', {'status': appStatus})
    else:
        return render(request, 'signup.html')


def responseTodoLists(result, statusMsg, todoLists):
    """Helper function for returning a TodoList request result in JSON HttpResponse"""

    todoLists = serializers.serialize("json", todoLists)
    return HttpResponse(json.dumps({'result': result, 'appStatus': statusMsg,
                                    'todoLists': todoLists}), 'text/json')


def responseTodos(result, statusMsg, todos, doneTodos, listName):
    """Helper function for returning a TodoItem request result in JSON HttpResponse"""

    todos = serializers.serialize("json", todos)
    doneTodos = serializers.serialize("json", doneTodos)
    return HttpResponse(json.dumps({'result': result, 'appStatus': statusMsg,
                                    'todos': todos, 'doneTodos': doneTodos, 'listName': listName}), 'text/json')


