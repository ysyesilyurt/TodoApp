from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



class TodoList(models.Model):
    """Model definition for TodoLists"""

    # user can not create 2 TodoLists with the same name
    name = models.TextField()
    listId = models.IntegerField(primary_key=True)
    todoCount = models.IntegerField()
    doneCount = models.IntegerField()
    createdWhen = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))

    # a Many-to-One relationship with user
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name="owner")

    class Meta:
        unique_together = (("listId", "owner"),)

    def __str__(self):
        return ' '.join(["List name:", self.name, ", Todo count:", str(self.todoCount), ", Done count:",
                         str(self.doneCount), ", Created on:", str(self.createdWhen),
                         ", Belongs to:", str(self.owner.username)])


class TodoItem(models.Model):
    """Model definition for TodoItems"""

    content = models.TextField()
    done = models.BooleanField()

    # a Many-to-One relationship with TodoList
    belongingList = models.ForeignKey(TodoList, blank=False, null=False,
                                      on_delete=models.CASCADE, related_name="todoList")

    class Meta:
        # user can not create 2 items with the same content in same TodoList
        unique_together = (("content", "belongingList"),)

    def __str__(self):
        return ' '.join(["Content:", self.content, ", Done:", str(self.done),
                         ", Belongs to:", str(self.belongingList.name)])
