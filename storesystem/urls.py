from django.urls import path, include
from storesystem import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('api/', include([
        path('db-status/', views.get_db_status, name='sstm.api.status'),
        path('get-items/', views.get_items, name='sstm.api.items'),
        path('create-users/', views.create_users, name='sstm.api.create_users'),
        path('create-invoice/', views.create_invoice, name='sstm.api.create_users'),
        path('create-user-by-json/', views.create_user_by_json, name='sstm.api.create_user_by_json'),
        path('create-stock-by-json/', views.create_stock_by_json, name='sstm.api.create_stock_by_json'),
        path('edit-users/', views.set_users, name='sstm.api.set_users'),
        path('update-profile/', views.update_profile, name='sstm.api.update_profile'),
        path('get-users/', views.get_users, name='sstm.api.users'),
        path('get-customers/', views.get_customers, name='sstm.api.customers'),
        path('get-invoices/', views.get_invioces, name='sstm.api.invoices'),
        path('get-all-invoices/', views.get_all_invioces, name='sstm.api.all_invoices'),
        path('login/', views.login, name='sstm.api.login'),
        path('register/', views.register, name='sstm.api.register'),
        path('delete-user/', views.delete_user, name='sstm.api.delete_user'),
        path('items-in-invoice/', view=views.get_items_in_invoice, name='sstm.api.items_in_invoice'),
        path('add-items-to-invoice/', view=views.add_items_to_invoice, name='sstm.api.add_items_to_invoice'),
        path('save-items-to-invoice/', view=views.save_items_to_invoice, name='sstm.api.save_items_to_invoice'),
        path('confirm-invoice/', view=views.confirm_invoice, name='sstm.api.confirm_invoice'),
        path('upload-stock-csv/', view=views.upload_stock_csv, name='sstm.api.upload_stock_csv'),
    ])),
]