from django.db import models
from django.utils import timezone


class TodoList(models.Model):
    """Model definition for TodoLists"""

    listId = models.IntegerField(primary_key=True)
    # user can not create 2 TodoLists with the same name
    name = models.CharField(unique=True, max_length=500)
    todoCount = models.IntegerField()
    doneCount = models.IntegerField()
    createdWhen = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))

    # __str__


class TodoItem(models.Model):
    """Model definition for TodoItems"""

    itemId = models.IntegerField(primary_key=True)
    content = models.TextField()
    done = models.TextField()
    importance = models.TextField()

    # a Many-to-One relationship with TodoList
    belongingList = models.ForeignKey(TodoList, blank=False, null=False, on_delete="CASCADE", related_name="todoList")

    class Meta:
        """ Meta class for handling the ordering of TodoItems"""

        ordering = ["itemId"]

    # __str__