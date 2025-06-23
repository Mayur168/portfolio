from django.urls import path
from .views import ProjectAPI, contactAPI,LoginView,RegisterView

urlpatterns = [
     path('project/', ProjectAPI.as_view(), name='project'),
     path('project/<int:pk>/', ProjectAPI.as_view(), name='project-delete'), 
     path('contacts/', contactAPI.as_view(), name='contact'), 
     path('contacts/<int:pk>/', contactAPI.as_view(), name='contact-delete'),
     path('login/', LoginView.as_view(), name='login'),
     path('register/', RegisterView.as_view(), name='register')
      
]