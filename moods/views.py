from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from .models import Mood
from .permissions import IsAuthorOrReadOnly
from .serializers import MoodSerializer, ReportSerializer


class MoodList(generics.ListCreateAPIView):
    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)

    queryset = Mood.objects.all()
    serializer_class = MoodSerializer


class MoodDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)

    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer


class MoodReportViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return get_user_model().objects.filter(username=self.request.user.username)

    queryset = get_user_model().objects.all()
    serializer_class = ReportSerializer
