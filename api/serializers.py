from rest_framework import serializers
from .models import Roomie
from .models import Task
from .models import Rule
from .models import Allergy

class RoomieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roomie
        fields = ('roomie_id','email','password','number_of_roommates','roommate_ids','name')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_id','roomie','tasks','start_time','end_time','task_type','roommate_ids')

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ('title','description','agreement_roomie_ids','disagreement_roomie_ids','official','created_at','updated_at','roommate_ids')

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ('name','description','roomie_ids')
