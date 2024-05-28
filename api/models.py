from django.db import models
from django.contrib.postgres.fields import JSONField  # This is specific to PostgreSQL.
import random
from django.contrib.auth.hashers import make_password, check_password

class Roomie(models.Model):
    roomie_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Consider Django's built-in User model for handling passwords securely.
    number_of_roommates = models.IntegerField(default=0)
    roommate_ids = models.JSONField(default=list) # Stores JSON data, now using the generic field.
    name = models.CharField(max_length=255,default="")  # Adding a name field to store the roomie's name.

    
    def __str__(self):
        return f"Password: {self.password}, Roomie ID: {self.roomie_id}, Name: {self.name}, Email: {self.email}, Roommates: {self.number_of_roommates}, Roommate IDs: {self.roommate_ids}"
    
    def save(self, *args, **kwargs):
        if not self.roommate_ids:
            self.roommate_ids = [0]
        super().save(*args, **kwargs)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Task(models.Model):
    TASK_TYPES = (
        (0, 'Chore'),
        (1, 'Visitor'),
        (2, 'Reservation'),
    )
    task_id = models.AutoField(primary_key=True)
    roomie = models.ForeignKey(Roomie, on_delete=models.CASCADE, related_name="tasks")
    tasks = models.TextField()  # Stores tasks as JSON, using the generic field.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task_type = models.IntegerField(choices=TASK_TYPES, default=0)
    roommate_ids = models.JSONField(default=list) # Stores JSON data, now using the generic field.


    

    def __str__(self):
        return f"Task {self.task_id} for Roomie {self.roomie.roomie_id}"
    
class Rule(models.Model):
    title = models.CharField(max_length=255)  # A brief title for the rule
    description = models.TextField()  # Detailed description of the rule
    agreement_roomie_ids = models.JSONField(default=list)  # IDs of roomies who agree with the rule
    disagreement_roomie_ids = models.JSONField(default=list)  # IDs of roomies who disagree with the rule
    official = models.BooleanField(default=False)  # Indicates if it is an official rule
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved.
    roommate_ids = models.JSONField(default=list) # Stores JSON data, now using the generic field.



    def __str__(self):
        return f"{self.title} (Official: {'Yes' if self.official else 'No'})"
    
class Allergy(models.Model):
    name = models.CharField(max_length=255,default="")  # A brief title for the allergy
    description = models.TextField()  # Detailed description of the allergy
    roomie_ids = models.JSONField(default=list)  # JSON field to store IDs of roomies who have this allergy

    def __str__(self):
        return f"Allergy: {self.name}"
