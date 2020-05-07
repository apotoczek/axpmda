from django.urls import path
from .views import MoodList, MoodDetail, MoodReportViewSet


urlpatterns = [
    path('moods/<int:pk>/', MoodDetail.as_view()),
    path('moods/', MoodList.as_view()),
    path('', MoodReportViewSet.as_view({'get': 'list'}))
]
