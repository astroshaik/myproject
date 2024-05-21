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
        fields = ['task_id', 'roomie', 'task_type', 'description', 'start_time', 'end_time']

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ('title','description','agreement_roomie_ids','disagreement_roomie_ids','official','created_at','updated_at')

class RoomieRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roomie
        fields = ['email', 'password', 'number_of_roommates', 'roommate_ids']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        roomie = Roomie(
            email=validated_data['email'],
            number_of_roommates=validated_data['number_of_roommates'],
            roommate_ids=validated_data['roommate_ids']
        )
        roomie.set_password(validated_data['password'])
        roomie.save()
        return roomie