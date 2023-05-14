from django.urls import path
from .views import StudentCreateAPIView, StudentSeatAPIView

urlpatterns = [
    path('student/create/', StudentCreateAPIView.as_view(), name='student-create'),
    path('student/seat/', StudentSeatAPIView.as_view(), name='student-seat'),
]
