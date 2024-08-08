from django.urls import path
from django.contrib.auth import views as auth
from django.conf import settings
from . import views as core_views

app_name = 'core'

urlpatterns = [
    path('login/', auth.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('home/', core_views.home, name='home'),
    path('add_sneaker/', core_views.add_sneaker, name='add_sneaker'),
    path('add_collection/', core_views.add_collection, name='add_collection'),
    path('collection/<int:pk>/', core_views.collection_detail, name='collection_detail'),
    path('sneaker/<int:pk>', core_views.sneaker_detail, name='sneaker_detail'),
    path('edit_sneaker/<int:pk>', core_views.edit_sneaker, name='edit_sneaker'),
    path('collection/<int:pk>/edit', core_views.edit_collection, name='edit-collection'),
    path('collection/<int:collection_pk>/remove-sneaker/<int:sneaker_pk>/', core_views.remove_sneaker_from_collection, name='remove_sneaker_from_collection'),
    path('collection/<int:pk>/delete/', core_views.delete_collection, name='delete_collection'),
    path('register/', core_views.register, name='register'),
    path('profile/', core_views.create_profile, name='profile'),
]