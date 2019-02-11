from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ordered_model.models import OrderedModel


class TodoList(OrderedModel):
    """Model definition for TodoLists"""

    listId = models.IntegerField(primary_key=True)
    name = models.TextField()
    todoCount = models.IntegerField()
    doneCount = models.IntegerField()
    createdWhen = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))

    # a Many-to-One relationship with User Model
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name="owner")

    class Meta(OrderedModel.Meta):
        # Each TodoList should be unique within its owner
        unique_together = (("listId", "owner"),)

    def __str__(self):
        return ' '.join(["List name:", self.name, ", Todo count:", str(self.todoCount), ", Done count:",
                         str(self.doneCount), ", Created on:", str(self.createdWhen),
                         ", Belongs to:", str(self.owner.username)])


class TodoItem(OrderedModel):
    """Model definition for TodoItems"""

    content = models.TextField()
    done = models.BooleanField()

    # a Many-to-One relationship with TodoList Model
    belongingList = models.ForeignKey(TodoList, blank=False, null=False,
                                      on_delete=models.CASCADE, related_name="todoList")

    class Meta(OrderedModel.Meta):
        # user can not create 2 items with the same content in same TodoList
        unique_together = (("content", "belongingList"),)

    def __str__(self):
        return ' '.join(["Content:", self.content, ", Done:", str(self.done),
                         ", Belongs to:", str(self.belongingList.name)])
