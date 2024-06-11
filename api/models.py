from django.db import models
import logging
from django.contrib.postgres.fields import JSONField  # This is specific to PostgreSQL.
import random
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from datetime import timedelta
import threading
import datetime
from django.utils import timezone

logger = logging.getLogger(__name__)
active_timers = {}
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


    def send_notification(self):
            try:
                subject = "Upcoming Task Reminder"
                from_email = 'noreply@yourdomain.com'
                if self.task_type == 0:  # Chore specific to a roomie
                    message = f"Reminder: You have a chore '{self.tasks}' starting at {self.start_time.strftime('%Y-%m-%d %H:%M')}"
                    recipient_list = [self.roomie.email]
                else:  # For other task types, notify all roommates
                    message = f"Reminder: There's an upcoming event '{self.tasks}' at {self.start_time.strftime('%Y-%m-%d %H:%M')}"
                    roomies = Roomie.objects.filter(roomie_id__in=self.roommate_ids)
                    recipient_list = [roomie.email for roomie in roomies]
                
                send_mail(subject, message, from_email, recipient_list)
                logger.info(f"Notification sent for task {self} to {recipient_list}")
            except Exception as e:
                logger.error(f"Failed to send notification for task {self}: {e}")


    def save(self, *args, **kwargs):
            print(f"Current time (timezone.now()): {timezone.now()}")
            print(f"Scheduled start time (self.start_key): {self.start_time}")
            self.send_notification()

            # Continue with saving as usual
            super().save(*args, **kwargs)

            # Calculate delay with timezone awareness
            delay = (self.start_time - timezone.now() - timedelta(minutes=15)).total_seconds()
            print(f"Calculated delay (seconds): {delay}")
            if delay > 0:
                timer = threading.Timer(delay, self.send_notification)
                timer.start()
                active_timers[self.task_id] = timer
            else:
                logger.warning(f"Notification for task {self} not scheduled because delay is non-positive")


    def __str__(self):
        return f"Task {self.task_id} for Roomie {self.roomie.roomie_id}"
    
    def delete(self, *args, **kwargs):
        self.delete_notification()
        super().delete(*args, **kwargs)
        
    def delete_notification(self):
        timer = active_timers.pop(self.task_id, None)
        if timer:
            timer.cancel()
            print(f"Notification timer cancelled for task {self.task_id}")
            
    
    
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
        return (f"Rule: {self.title}, Description: {self.description}, "
                f"Agree: {self.agreement_roomie_ids}, Disagree: {self.disagreement_roomie_ids}, "
                f"Official: {'Yes' if self.official else 'No'}, Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}, "
                f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')}, Roommate IDs: {self.roommate_ids}")
    
class Allergy(models.Model):
    name = models.CharField(max_length=255,default="")  # A brief title for the allergy
    description = models.TextField()  # Detailed description of the allergy
    roomie_ids = models.JSONField(default=list)  # JSON field to store IDs of roomies who have this allergy

    def __str__(self):
        return f"Allergy: {self.name}, Description: {self.description}, Roomie IDs: {self.roomie_ids}"
