from django.urls import path
from .views import ClassResult,AcademicResult,Notification

urlpatterns = [
    path('api/classresult',ClassResult.as_view()),
    path('api/academicresult',AcademicResult.as_view()),
    path('api/notifications',Notification.as_view())
]
