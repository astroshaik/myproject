from rest_framework import serializers
from .models import Roomie

class RoomieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roomie
        fields = ('roomie_id','email','password','number_of_roommates','roommate_ids')
