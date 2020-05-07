from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Mood


class MoodSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Mood
        fields = ('id', 'user', 'mood', 'details', 'created_at',)


class ReportSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(source='id')
    moods = MoodSerializer(many=True, read_only=True)

    moods_count = serializers.SerializerMethodField(method_name='_moods_count')

    def _moods_count(self, obj):
        moods = Mood.objects.filter(user=self.context['request'].user)
        return len(moods)

    newest_streak = serializers.SerializerMethodField(method_name='_newest_streak')

    def _newest_streak(self, obj):
        newest_streak = 1

        today = datetime.today()
        entry_dates = list(Mood.objects.values("created_at")
                           .filter(user=self.context['request'].user, created_at__lte=today)
                           .order_by("-created_at"))
        length = len(entry_dates)

        if length == 0:
            return 0
        elif length == 1:
            return 1
        else:
            i = 0
            newest_streak_broken = False
            while i < length - 1:
                delta = entry_dates[i]['created_at'].date() - entry_dates[i+1]['created_at'].date()
                if delta.days == 1 and not newest_streak_broken:
                    newest_streak += 1
                elif delta.days == 0 and not newest_streak_broken:
                    newest_streak += 0  # pass
                else:
                    newest_streak_broken = True
                i += 1

        return newest_streak

    longest_streak = serializers.SerializerMethodField(method_name='_longest_streak')

    def _longest_streak(self, obj):
        current_streak = 1
        longest_streak = 1

        today = datetime.today()
        entry_dates = list(Mood.objects.values("created_at")
                           .filter(user=self.context['request'].user, created_at__lte=today)
                           .order_by("-created_at"))
        length = len(entry_dates)

        if length == 0:
            return 0
        elif length == 1:
            return 1
        else:
            i = 0
            while i < length - 1:
                delta = entry_dates[i]['created_at'].date() - entry_dates[i + 1]['created_at'].date()
                if delta.days == 1:
                    current_streak += 1
                    if current_streak > longest_streak:
                        longest_streak = current_streak
                elif delta.days == 0:
                    current_streak += 0  # pass
                else:
                    current_streak = 1
                i += 1

        return longest_streak

    streak_percentile = serializers.SerializerMethodField(method_name='_streak_percentile')

    def _streak_percentile(self, obj):
        today = datetime.today()
        my_current_streak = 1
        my_longest_streak = 1
        entry_dates = list(Mood.objects.values("created_at")
                           .filter(user=self.context['request'].user, created_at__lte=today)
                           .order_by("-created_at"))
        length = len(entry_dates)
        if length == 0:
            my_longest_streak = 0
        elif length == 1:
            my_longest_streak = 1
        else:
            i = 0
            while i < length - 1:
                delta = entry_dates[i]['created_at'].date() - entry_dates[i + 1]['created_at'].date()
                if delta.days == 1:
                    my_current_streak += 1
                    if my_current_streak > my_longest_streak:
                        my_longest_streak = my_current_streak
                elif delta.days == 0:
                    my_current_streak += 0  # pass
                else:
                    my_current_streak = 1
                i += 1

        users = get_user_model().objects.all()
        others_longest_streaks = []
        for u in users:
            others_current_streak = 1
            others_longest_streak = 1
            if u.id != self.context['request'].user.id:
                entry_dates = list(Mood.objects.values("created_at")
                                   .filter(user=u, created_at__lte=today)
                                   .order_by("-created_at"))
                length = len(entry_dates)
                if length == 0:
                    others_longest_streak = 0
                elif length == 1:
                    others_longest_streak = 1
                else:
                    i = 0
                    while i < length - 1:
                        delta = entry_dates[i]['created_at'].date() - entry_dates[i + 1]['created_at'].date()
                        if delta.days == 1:
                            others_current_streak += 1
                            if others_current_streak > others_longest_streak:
                                others_longest_streak = others_current_streak
                        elif delta.days == 0:
                            others_current_streak += 0  # pass
                        else:
                            others_current_streak = 1
                        i += 1
                others_longest_streaks.append(others_longest_streak)

        avg_others_longest_streak = 0
        for x in others_longest_streaks:
            avg_others_longest_streak += x
        avg_others_longest_streak = avg_others_longest_streak / len(others_longest_streaks)
        streak_percentile_decimal = ((my_longest_streak - avg_others_longest_streak) / avg_others_longest_streak)

        return round(streak_percentile_decimal, 2)

    class Meta:
        model = get_user_model()
        fields = (
            'user_id',
            'username',
            'moods_count',
            'newest_streak',
            'longest_streak',
            'streak_percentile',
            'moods',
        )
