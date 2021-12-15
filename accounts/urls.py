from django.urls import path
from . import views


app_name= 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user-create/', views.user_create, name='user_create'),
]


handler500 = views.mycustomized_sever_error