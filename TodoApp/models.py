from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class TodoList(models.Model):
    """Model definition for TodoLists"""

    # listId = models.IntegerField(unique=True)
    # user can not create 2 TodoLists with the same name
    name = models.CharField(primary_key=True, max_length=500)
    todoCount = models.IntegerField()
    doneCount = models.IntegerField()
    createdWhen = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))


class TodoItem(models.Model):
    """Model definition for TodoItems"""

    # user can not create 2 TodoItems with the same content
    content = models.TextField(primary_key=True)
    done = models.BooleanField()
    # importance level can be set as any number in range [0,5]
    importance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    # a Many-to-One relationship with TodoList
    belongingList = models.ForeignKey(TodoList, blank=False, null=False, on_delete="CASCADE", related_name="listName")

    class Meta:
        """ Meta class for handling the ordering of TodoItems"""

        ordering = ["-importance"]
