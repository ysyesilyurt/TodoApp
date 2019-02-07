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

    def __str__(self):
        return ' '.join([self.name, str(self.todoCount), str(self.doneCount), str(self.createdWhen)])


class TodoItem(models.Model):
    """Model definition for TodoItems"""

    # user can not create 2 items with the same content
    content = models.TextField()
    done = models.BooleanField()

    # a Many-to-One relationship with TodoList
    belongingList = models.ForeignKey(TodoList, blank=False, null=False, on_delete="CASCADE", related_name="todoList")

    class Meta:
        unique_together = (("content", "belongingList"),)

    def __str__(self):
        return ' '.join([self.content, str(self.done)])
