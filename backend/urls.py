from django.urls import path
from .views import projectAPI, contactAPI,LoginView,RegisterView

urlpatterns = [
     path('project/', projectAPI.as_view(), name='project'),
     path('project/<int:pk>/', projectAPI.as_view(), name='project-delete'), 
     path('contacts/', contactAPI.as_view(), name='contact'), 
     path('contacts/<int:pk>/', contactAPI.as_view(), name='contact-delete'),
     path('login/', LoginView.as_view(), name='login'),
     path('register/', RegisterView.as_view(), name='register')
      
]