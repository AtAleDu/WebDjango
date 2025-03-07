# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('', views.book_list, name='book_list'),
    path('book/new/', views.book_new, name='book_new'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
]