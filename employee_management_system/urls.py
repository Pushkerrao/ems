from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path
from employee.views import *
from departments.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login/', auth_views.LoginView.as_view(template_name = 'employee/login.html',redirect_authenticated_user=True), name="login"),
    path('', home, name="home-page"),
    path('userlogin',login_user, name="login-user"),
    path('api/employees-list/', get_all_employees, name='get_all_employees'),
    path('employees/add/', create_employee, name='create_employee'),
    path('employees/<int:employee_id>/', get_employee, name='get_employee'),
    path('employees/<int:employee_id>/update/', api_update_employee, name='update_employee'),
    path('employees/<int:employee_id>/delete/', api_delete_employee, name='delete_employee'),
    path('api/departments-list/',get_all_departments, name='get_all_departments'),
    path('departments/add/', create_departments, name='create_departments'),
    path('departments/<int:department_id>/', get_department, name='get_department'),
    path('departments/<int:department_id>/update/', api_update_department, name='update_department'),
    path('departments/<int:department_id>/delete/', api_delete_department, name='delete_department'),
    path('logout', logoutuser, name="logout"),
    path('employees', employees, name="employee-page"),
    path('departments', departments, name="department-page"),
    path('manage_employees', manage_employees, name="manage_employees"),
    path('save_employee', save_employee, name="save-employee"),
    path('view_employee', view_employee, name="view-employee"),
    path('delete_employee', delete_employee, name="delete-employee"),
    path('manage_departments', manage_departments, name="manage_departments-page"),
    path('save_department', save_department, name="save-department-page"),
    path('delete_department', delete_department, name="delete-department"),

]