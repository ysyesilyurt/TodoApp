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
    """Home page that displays active TodoLists and their related information."""

    result = ""
    appStatus = ""

    if request.method == "GET":
        todoLists = models.TodoList.objects.filter(owner=request.user)
        return render(request, "index.html", {"todoLists": todoLists})

    elif request.POST["submit"] == "Create":
        listName = request.POST['listName']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
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

    if result == "":
        result = "Success"
    todoLists = models.TodoList.objects.filter(owner=request.user)
    return responseTodoLists(result, appStatus, todoLists)


@login_required
def items(request, listID=None):
    """List item page that displays entries and related information that specified TodoList contains."""

    result = ""
    appStatus = ""

    if request.method == "GET":
        todos = models.TodoItem.objects.filter(belongingList_id=listID, done=False)
        doneTodos = models.TodoItem.objects.filter(belongingList_id=listID, done=True)
        return render(request, "items.html", {"todos": todos, "doneTodos": doneTodos})

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
    return responseTodos(result, appStatus, todos, doneTodos)


def signup(request):
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


# Return a TodoList request result in JSON HttpResponse
def responseTodoLists(result, statusMsg, todoLists):
    todoLists = serializers.serialize("json", todoLists)
    return HttpResponse(json.dumps({'result': result, 'appStatus': statusMsg,
                                    'todoLists': todoLists}), 'text/json')


# Return a TodoItem request result in JSON HttpResponse
def responseTodos(result, statusMsg, todos, doneTodos):
    todos = serializers.serialize("json", todos)
    doneTodos = serializers.serialize("json", doneTodos)
    return HttpResponse(json.dumps({'result': result, 'appStatus': statusMsg,
                                    'todos': todos, 'doneTodos': doneTodos}), 'text/json')


