from django.urls import path
from . import views


app_name= 'todo'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.todo_detail, name='todo_detail'),
    path('create/', views.todo_create, name='todo_create'),
    path('update/<int:pk>/', views.todo_update, name='todo_update'),
    path('delete/<int:pk>/', views.todo_delete, name='todo_delete'),
]