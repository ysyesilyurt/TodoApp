import json
import re

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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
    owner = models.Owner.objects.filter(username=request.user)[0]

    if request.method == "GET":
        todoLists = models.TodoList.objects.filter(owner=owner)
        orderList = models.Owner.objects.filter(username=request.user).values('orderList')[0]['orderList']
        if orderList != "":
            orderList = orderList.split(',')
            sortedLists = []
            for listName in orderList:
                sortedLists.append(todoLists.get(name=listName))
            return render(request, "index.html", {"todoLists": sortedLists})
        else:
            return render(request, "index.html", {"todoLists": todoLists})

    elif request.POST["submit"] == "Create":
        listName = request.POST['listName']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
            result = "Fail"
        elif models.TodoList.objects.filter(owner=owner, name=listName).exists():
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
                                               listId=newListId, owner=owner)

                oldOrderList = models.Owner.objects.filter(username=request.user).values('orderList')[0]['orderList']
                if oldOrderList != "":
                    newOrderList = oldOrderList + ',' + listName
                    models.Owner.objects.filter(username=request.user).update(orderList=newOrderList)

            except IntegrityError:
                appStatus = "Create operation failed. Please make sure that your TodoList name " \
                            "does not exist in current TodoLists"
                result = "Fail"

    elif request.POST["submit"] == "Delete":
        listName = request.POST['listName']
        if listName == "":
            appStatus = "Please choose a valid TodoList name"
            result = "Fail"
        else:
            try:
                models.TodoList.objects.filter(owner=owner).get(name=listName).delete()
                oldOrderList = models.Owner.objects.filter(username=request.user).values('orderList')[0]['orderList']
                newOrderList = re.sub(listName + ',', "", oldOrderList)
                if len(oldOrderList) == len(newOrderList):
                    newOrderList = re.sub(',' + listName, "", oldOrderList)
                models.Owner.objects.filter(username=request.user).update(orderList=newOrderList)

            except models.TodoList.DoesNotExist:
                appStatus = "Delete operation failed. Please make sure that your TodoList name " \
                            "exists in current TodoLists"
                result = "Fail"

    elif request.POST["submit"] == "Edit":
        listName = request.POST['listName']
        newName = request.POST['newName']
        try:
            models.TodoList.objects.filter(owner=owner, name=listName).update(name=newName)
            oldOrderList = models.Owner.objects.filter(username=request.user).values('orderList')[0]['orderList']
            newOrderList = oldOrderList.replace(listName, newName)
            models.Owner.objects.filter(username=request.user).update(orderList=newOrderList)

        except IntegrityError:
            appStatus = "Edit operation failed. Please make sure that your TodoList name " \
                        "does not exists in current TodoLists"
            result = "Fail"

    elif request.POST["submit"] == "listSort":
        orderList = request.POST['orderList']
        try:
            orderList = json.loads(orderList)
            models.Owner.objects.filter(username=request.user).update(orderList=orderList)
        except models.Owner.DoesNotExist:
            appStatus = "Sorting operation failed. Please make sure that owner " \
                        "exists in TodoApp system"
            result = "Fail"

    if result == "":
        result = "Success"

    todoLists = models.TodoList.objects.filter(owner=owner)
    orderList = models.Owner.objects.filter(username=request.user).values('orderList')[0]['orderList']
    if orderList != "":
        orderList = orderList.split(',')
        sortedLists = []
        for listName in orderList:
            sortedLists.append(todoLists.get(name=listName))
        todoLists = sortedLists

    return responseTodoLists(result, appStatus, todoLists)


@login_required
def todos(request, listID=None):
    """TodoItem page view that displays related TodoItems and their information, which specified TodoList contains,
    along with the available operations."""

    result = ""
    appStatus = ""
    owner = models.Owner.objects.filter(username=request.user)[0]
    listName = models.TodoList.objects.filter(owner=owner, listId=listID).values('name')[0]['name']

    if request.method == "GET":
        todos = models.TodoItem.objects.filter(belongingList_id=listID, done=False)
        doneTodos = models.TodoItem.objects.filter(belongingList_id=listID, done=True)
        todoOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
        doneOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('doneOrderList')[0]['doneOrderList']

        if todoOrderList != "":
            todoOrderList = todoOrderList.split(',')
            sortedTodos = []
            for content in todoOrderList:
                sortedTodos.append(todos.get(content=content))
            todos = sortedTodos

        if doneOrderList != "":
            doneOrderList = doneOrderList.split(',')
            sortedDoneTodos = []
            for content in doneOrderList:
                sortedDoneTodos.append(doneTodos.get(content=content))
            doneTodos = sortedDoneTodos

        return render(request, "todos.html", {"todos": todos, "doneTodos": doneTodos, "listName": listName})

    elif request.POST["submit"] == "itemSort":
        orderList = request.POST['orderList']
        try:
            orderList = json.loads(orderList)
            models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList=orderList)
        except models.TodoList.DoesNotExist:
            appStatus = "Sorting operation failed. Please make sure that Todo List " \
                        "exists in TodoApp system"
            result = "Fail"

    elif request.POST["submit"] == "doneItemSort":
        orderList = request.POST['orderList']
        try:
            orderList = json.loads(orderList)
            models.TodoList.objects.filter(listId=listID, owner=owner).update(doneOrderList=orderList)
        except models.TodoList.DoesNotExist:
            appStatus = "Sorting done items operation failed. Please make sure that Todo List " \
                        "exists in TodoApp system"
            result = "Fail"

    elif request.POST["submit"] == "Create":
        itemContent = request.POST['itemContent']
        if itemContent == "":
            appStatus = "Please specify a valid Todo."
            result = "Fail"
        else:
            try:
                models.TodoItem.objects.create(content=itemContent, done=False, belongingList_id=listID)
                models.TodoList.objects.filter(listId=listID, owner=owner).update(todoCount=F('todoCount') + 1)
                oldOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
                if oldOrderList != "":
                    newOrderList = oldOrderList + ',' + itemContent
                    models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList=newOrderList)
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
                models.TodoList.objects.filter(listId=listID, owner=owner).update(todoCount=F('todoCount') - 1)
                models.TodoList.objects.filter(listId=listID, owner=owner).update(doneCount=F('doneCount') - 1)
                oldOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('doneOrderList')[0]['doneOrderList']
                newOrderList = re.sub(itemContent + ',', "", oldOrderList)
                if len(oldOrderList) == len(newOrderList):
                    newOrderList = re.sub(',' + itemContent, "", oldOrderList)
                models.TodoList.objects.filter(listId=listID, owner=owner).update(doneOrderList=newOrderList)
            except models.TodoList.DoesNotExist:
                appStatus = "Delete operation failed. Please make sure that selected Todo " \
                            "exists in current Todo items."
                result = "Fail"

    elif request.POST["submit"] == "Edit":
        itemContent = request.POST['itemContent']
        newContent = request.POST['newContent']
        try:
            models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent).update(content=newContent)
            oldTodoOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
            newTodoOrderList = oldTodoOrderList.replace(itemContent, newContent)
            models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList=newTodoOrderList)

        except IntegrityError:
            appStatus = "Create operation failed. Please make sure that your new Todo content " \
                        "does not exist in current or done Todos."
            result = "Fail"

    elif request.POST["submit"] == "Undone":
        itemContent = request.POST['itemContent']
        if itemContent == "":
            appStatus = "Need a valid Todo item."
            result = "Fail"
        else:
            try:
                models.TodoItem.objects.filter(belongingList_id=listID, content=itemContent).update(done=False)
                models.TodoList.objects.filter(listId=listID, owner=owner).update(doneCount=F('doneCount') - 1)
                oldDoneOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('doneOrderList')[0]['doneOrderList']
                newDoneOrderList = re.sub(itemContent + ',', "", oldDoneOrderList)
                if len(oldDoneOrderList) == len(newDoneOrderList):
                    newDoneOrderList = re.sub(',' + itemContent, "", oldDoneOrderList)
                models.TodoList.objects.filter(listId=listID, owner=owner).update(doneOrderList=newDoneOrderList)

                oldTodoOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
                if oldTodoOrderList != "":
                    newTodoOrderList = oldTodoOrderList + ',' + itemContent
                    models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList=newTodoOrderList)

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
                models.TodoList.objects.filter(listId=listID, owner=owner).update(doneCount=F('doneCount') + 1)
                oldTodoOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
                newTodoOrderList = re.sub(itemContent + ',', "", oldTodoOrderList)
                if len(oldTodoOrderList) == len(newTodoOrderList):
                    newTodoOrderList = re.sub(',' + itemContent, "", oldTodoOrderList)
                models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList=newTodoOrderList)

                oldDoneOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('doneOrderList')[0]['doneOrderList']
                if oldDoneOrderList != "":
                    newDoneOrderList = oldDoneOrderList + ',' + itemContent
                    models.TodoList.objects.filter(listId=listID, owner=owner).update(doneOrderList=newDoneOrderList)

            except models.TodoItem.DoesNotExist:
                appStatus = "Marking operation failed. Please make sure that selected Todo " \
                            "exists in current Todo items."
                result = "Fail"

    elif request.POST["submit"] == "Mark all as Done":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID).update(done=True)
            models.TodoList.objects.filter(listId=listID, owner=owner).update(doneCount=F('todoCount'))
            oldTodoOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
            models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList="")

            oldDoneOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('doneOrderList')[0]['doneOrderList']
            if oldTodoOrderList != "" and oldTodoOrderList[-1] == ",":
                oldTodoOrderList = oldTodoOrderList[:-1]
            if oldDoneOrderList != "":
                newDoneOrderList = oldDoneOrderList + ',' + oldTodoOrderList
                models.TodoList.objects.filter(listId=listID, owner=owner).update(doneOrderList=newDoneOrderList)

        except models.TodoItem.DoesNotExist:
            appStatus = "Marking operation failed, no TodoItem seems to exist as undone."
            result = "Fail"

    elif request.POST["submit"] == "Mark all as Undone":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID).update(done=False)
            models.TodoList.objects.filter(listId=listID, owner=owner).update(doneCount=0)
            oldDoneOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('doneOrderList')[0]['doneOrderList']
            models.TodoList.objects.filter(listId=listID, owner=owner).update(doneOrderList="")

            oldTodoOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
            if oldDoneOrderList != "" and oldDoneOrderList[-1] == ",":
                oldTodoOrderList = oldTodoOrderList[:-1]
            if oldTodoOrderList != "":
                newTodoOrderList = oldTodoOrderList + ',' + oldDoneOrderList
                models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList=newTodoOrderList)

        except models.TodoItem.DoesNotExist:
            appStatus = "Marking operation failed, no TodoItem seems to exist as done."
            result = "Fail"

    elif request.POST["submit"] == "Delete all Done":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID, done=True).delete()
            models.TodoList.objects.filter(listId=listID, owner=owner).update(todoCount=F('todoCount') - F('doneCount'))
            models.TodoList.objects.filter(listId=listID, owner=owner).update(doneCount=0)
            models.TodoList.objects.filter(listId=listID, owner=owner).update(doneOrderList="")
        except models.TodoItem.DoesNotExist:
            appStatus = "Deleting all operation failed, no TodoItem seems to exist as done."
            result = "Fail"

    elif request.POST["submit"] == "Delete all Undone":
        try:
            models.TodoItem.objects.filter(belongingList_id=listID, done=False).delete()
            models.TodoList.objects.filter(listId=listID, owner=owner).update(todoCount=F('doneCount'))
            models.TodoList.objects.filter(listId=listID, owner=owner).update(todoOrderList="")
        except models.TodoItem.DoesNotExist:
            appStatus = "Deleting all operation failed, no TodoItem seems to exist as done."
            result = "Fail"

    if result == "":
        result = "Success"

    todos = models.TodoItem.objects.filter(belongingList_id=listID, done=False)
    doneTodos = models.TodoItem.objects.filter(belongingList_id=listID, done=True)
    todoOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('todoOrderList')[0]['todoOrderList']
    doneOrderList = models.TodoList.objects.filter(listId=listID, owner=owner).values('doneOrderList')[0]['doneOrderList']

    if todoOrderList != "":
        todoOrderList = todoOrderList.split(',')
        sortedTodos = []
        for content in todoOrderList:
            sortedTodos.append(todos.get(content=content))
        todos = sortedTodos

    if doneOrderList != "":
        doneOrderList = doneOrderList.split(',')
        sortedDoneTodos = []
        for content in doneOrderList:
            sortedDoneTodos.append(doneTodos.get(content=content))
        doneTodos = sortedDoneTodos

    return responseTodos(result, appStatus, todos, doneTodos, listName)


def signup(request):
    """SignUp page view that signs up new user to the system, according to given information."""

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = models.Owner.objects.create_user(username, email, password)
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


