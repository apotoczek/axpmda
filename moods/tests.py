from django.test import TestCase
from django.contrib.auth.models import User
from .models import Mood


class MoodapiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser123 = User.objects.create_user(username='testuser123', password='pass123')
        testuser123.save()
        test_mood = Mood.objects.create(
            user=testuser123, mood='Optimistic', details='Feeling good')
        test_mood.save()

    def test_moods(self):
        obj = Mood.objects.get(id=1)
        user = f'{obj.user}'
        mood = f'{obj.mood}'
        details = f'{obj.details}'

        self.assertEqual(user, 'testuser123')
        self.assertEqual(mood, 'Optimistic')
        self.assertEqual(details, 'Feeling good')
