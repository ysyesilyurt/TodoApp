# Generated by Django 2.1.5 on 2019-02-08 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('done', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('listId', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('todoCount', models.IntegerField()),
                ('doneCount', models.IntegerField()),
                ('createdWhen', models.DateField(default='2019-02-08')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='todoitem',
            name='belongingList',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todoList', to='TodoApp.TodoList'),
        ),
        migrations.AlterUniqueTogether(
            name='todolist',
            unique_together={('listId', 'owner')},
        ),
        migrations.AlterUniqueTogether(
            name='todoitem',
            unique_together={('content', 'belongingList')},
        ),
    ]