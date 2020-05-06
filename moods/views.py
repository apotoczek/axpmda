from rest_framework import generics, permissions
from .models import Mood
from .serializers import MoodSerializer


class MoodList(generics.ListCreateAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer


class MoodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
