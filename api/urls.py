from django.urls import path, include

urlpatterns = [
    path('user/', include('api.users.urls')),
    path('exam/', include('api.exams.urls')),
]
