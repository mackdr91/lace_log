from . import views as inv_views
from django.urls import path


app_name = 'inventory'

urlpatterns = [
    path('', inv_views.inventory, name='inventory'),
    path('delete_sneaker/<int:pk>', inv_views.delete_sneaker, name='delete_sneaker'),
    path('download-qr-codes/', inv_views.download_qr_codes, name='download_qr_codes'),
    path('download-sneaker-spreadsheet/', inv_views.generate_sneaker_spreadsheet, name='download_sneaker_spreadsheet'),
    path('add-sneaker/', inv_views.add_sneaker, name='add_sneaker'),

]