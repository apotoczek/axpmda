from django.urls import path
from .views import MoodList, MoodDetail


urlpatterns = [
    path('<int:pk>/', MoodDetail.as_view()), path('', MoodList.as_view()),
]
