from rest_framework import serializers
from .models import Mood


class MoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mood
        fields = ('id', 'user', 'mood', 'details', 'created_at',)
