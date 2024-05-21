from rest_framework import serializers
from .models import Roomie
from .models import Task
from .models import Rule
class RoomieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roomie
        fields = ('roomie_id','email','password','number_of_roommates','roommate_ids')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_id','roomie','tasks','start_time','end_time','task_type')

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ('title','description','agreement_roomie_ids','disagreement_roomie_ids','official','created_at','updated_at')
