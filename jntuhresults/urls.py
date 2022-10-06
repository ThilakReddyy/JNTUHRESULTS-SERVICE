from django.urls import path
from .views import multi,allResults

urlpatterns = [
    path('api/multi',multi.as_view()),
    path('api/single',allResults.as_view()),
]
