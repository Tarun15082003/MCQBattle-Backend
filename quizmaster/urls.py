from django.urls import path
from .views import QuizQuestionAPIView

urlpatterns =[
    path('questions/',QuizQuestionAPIView.as_view(),name='questions'),
    path('questions/<int:question_id>/',QuizQuestionAPIView.as_view(),name='quiz_question_update_delete')
]