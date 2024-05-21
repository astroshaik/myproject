from django.db import models
from django.contrib.postgres.fields import JSONField  # This is specific to PostgreSQL.
import random


# Define the Roomie model, which represents a roommate in the system.
# Auto-incrementing ID for Roomie, serves as the primary key.
# Email field that must be unique.
# Password field, consider using Django's authentication system for better security.
# Integer field to store the number of roommates.
# JSON field to store IDs of roommates, allowing for flexible data structures.
class Roomie(models.Model):
    roomie_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Consider Django's built-in User model for handling passwords securely.
    number_of_roommates = models.IntegerField(default=0)
    roommate_ids = models.JSONField()  # Stores JSON data, now using the generic field.
# String representation of the model returns the roomie ID.
    def __str__(self):
        return str(self.roomie_id)

# Define the Task model, which represents tasks assigned to roommates.
# Auto-incrementing ID for Task, serves as the primary key.
# ForeignKey to associate a task with a Roomie.
# JSON field to store detailed task information.
# DateTime field to store the start time of the task.
# DateTime field to store the end time of the task.
# Integer field to store the type of task.
class Task(models.Model):
    # Choices for types of tasks.
    TASK_TYPES = (
        (0, 'Chore'),
        (1, 'Visitor'),
        (2, 'Reservation'),
    )
    task_id = models.AutoField(primary_key=True)
    roomie = models.ForeignKey(Roomie, on_delete=models.CASCADE, related_name="tasks")
    task_type = models.IntegerField(choices=TASK_TYPES, default=0)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
# String representation of the model.
    def __str__(self):
        return f"{self.get_task_type_display()} on {self.start_time.strftime('%Y-%m-%d')} for {self.roomie.email}"

# Define the Rule model, which represents rules agreed upon by roommates.
# CharField to store the title of the rule.
# TextField to store a detailed description of the rule.
# JSON field to store IDs of roomies who agree with the rule.
# JSON field to store IDs of roomies who disagree with the rule.
# Boolean field to indicate if the rule is officially accepted.
# DateTime field to store the creation time of the rule.
# DateTime field to store the last update time of the rule.
class Rule(models.Model):
    title = models.CharField(max_length=255)  # A brief title for the rule
    description = models.TextField()  # Detailed description of the rule
    agreement_roomie_ids = models.JSONField()  # IDs of roomies who agree with the rule
    disagreement_roomie_ids = models.JSONField()  # IDs of roomies who disagree with the rule
    official = models.BooleanField(default=False)  # Indicates if it is an official rule
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved.
# String representation of the model.
    def __str__(self):
        return f"{self.title} (Official: {'Yes' if self.official else 'No'})"
