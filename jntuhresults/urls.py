from django.urls import path
from .views import (
    AcademicAllResults,
    ClassResult,
    AcademicResult,
    Notification,
    test,
)

urlpatterns = [
    path("test", test),
    path("api/classresult", ClassResult.as_view()),
    path("api/academicallresult", AcademicAllResults.as_view()),
    path("api/academicresult", AcademicResult.as_view()),
    path("api/notifications", Notification.as_view()),
]
