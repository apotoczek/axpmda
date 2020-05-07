from django.contrib.auth import get_user_model, get_user
from rest_framework import serializers
from .models import Mood


class MoodSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    mood_id = serializers.IntegerField(source='id')

    class Meta:
        model = Mood
        fields = ('mood_id', 'user', 'mood', 'details', 'created_at',)


class ReportSerializer(serializers.ModelSerializer):

    moods = MoodSerializer(many=True, read_only=True)
    moods_count = serializers.SerializerMethodField(method_name='_moods_count')

    def _moods_count(self, instance):
        moods = Mood.objects.filter(user=self.context['request'].user)
        return len(moods)

    user_id = serializers.IntegerField(source='id')

    class Meta:
        model = get_user_model()
        fields = ('user_id', 'username', 'moods_count', "moods",)
