from django.urls import path
from . import views
from .views import UserRetrieveUpdateAPIView, RegistrationAPIView, LoginAPIView, TODOListAPIView
from  .views import TODODetail

app_name = 'main'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('api/user/', UserRetrieveUpdateAPIView.as_view()),
    path('api/users/', RegistrationAPIView.as_view()),
    path('api/users/login', LoginAPIView.as_view()),
    path('api/show', views.home2),
    path('api/completed/<int:todo_id>', views.api_completed_todo_detail),
    path('api/completed', views.api_completed_todo),
    path('add_todo', views.add_todo , name = 'add_todo'),
    path('delete_todo', views.delete_todo , name = 'delete_todo'),
    path('delete_todoOne', views.delete_todoOne),
    path('completed_todo', views.completed_todo , name = 'completed_todo'),
    path('check/<int:todo_id>', views.check ),
    path('task/<int:pk>/', TODODetail.as_view(), name = 'task-detail')
]