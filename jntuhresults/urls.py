from django.urls import path
from .views import multi,allResults,academicResult

urlpatterns = [
    path('api/multi',multi.as_view()),
    path('api/single',academicResult.as_view()),
    path('api/academicresult',academicResult.as_view())
]
