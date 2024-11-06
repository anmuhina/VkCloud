from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('create/', views.note_create, name='note_create'),
    path('edit/<int:pk>/', views.note_edit, name='note_edit'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]