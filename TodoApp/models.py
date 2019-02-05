from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class TodoList(models.Model):
    """Model definition for TodoLists"""

    name = models.CharField(max_length=500)
    todoCount = models.IntegerField()
    doneCount = models.IntegerField()
    createdWhen = models.DateField(default=timezone.now().strftime("%d-%m-%Y"))


class TodoItem(models.Model):
    """Model definition for TodoItems"""

    content = models.TextField()
    dueDate = models.DateField(default=timezone.now().strftime("%d-%m-%Y"), blank=True)
    done = models.BooleanField()
    # importance level can be set as any number in range [0,5]
    importance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    # a Many-to-One relationship with TodoList
    belongingList = models.ForeignKey(TodoList, blank=False, null=False, on_delete="CASCADE")

    class Meta:
        """ Meta class for handling the ordering of TodoItems"""

        ordering = ["-importance"]
