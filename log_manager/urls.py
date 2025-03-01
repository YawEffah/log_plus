from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('dashboard', dashboard_view, name='dashboard'),
    path('employees', employees_view, name='employees'),
    path('statistics', statistics_view, name='statistics'),
    # path('add_employee/', add_employee_view, name='add_employee'),
    path('edit_employee/<int:employee_id>', edit_employee_view, name='edit_employee'),
    path('delete_employee/<int:employee_id>', delete_employee_view, name='delete_employee'),
]
