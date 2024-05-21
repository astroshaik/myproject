from django.db import models
from django.contrib.postgres.fields import JSONField  # This is specific to PostgreSQL.
import random

class Roomie(models.Model):
    roomie_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Consider Django's built-in User model for handling passwords securely.
    number_of_roommates = models.IntegerField(default=0)
    roommate_ids = models.JSONField()  # Stores JSON data, now using the generic field.
    
    def __str__(self):
        return str(self.roomie_id)

class Task(models.Model):
    TASK_TYPES = (
        (0, 'Chore'),
        (1, 'Visitor'),
        (2, 'Reservation'),
    )
    task_id = models.AutoField(primary_key=True)
    roomie = models.ForeignKey(Roomie, on_delete=models.CASCADE, related_name="tasks")
    tasks = models.JSONField()  # Stores tasks as JSON, using the generic field.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task_type = models.IntegerField(choices=TASK_TYPES, default=0)
    

    def __str__(self):
        return f"Task {self.task_id} for Roomie {self.roomie.roomie_id}"
    
class Rule(models.Model):
    title = models.CharField(max_length=255)  # A brief title for the rule
    description = models.TextField()  # Detailed description of the rule
    agreement_roomie_ids = models.JSONField()  # IDs of roomies who agree with the rule
    disagreement_roomie_ids = models.JSONField()  # IDs of roomies who disagree with the rule
    official = models.BooleanField(default=False)  # Indicates if it is an official rule
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved.

    def __str__(self):
        return f"{self.title} (Official: {'Yes' if self.official else 'No'})"
