from django.db import connection

# GET All Departments
def get_departments():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_all_departments_proc()")
        departments = cursor.fetchall()
    return departments

# Add Department
def add_department(data):
    with connection.cursor() as cursor:
        cursor.execute("SELECT create_departments( %s, %s)",
                       ( data['department_type'], data['role']))
        new_department_id = cursor.fetchone()[0]
    return new_department_id

# Get Department by ID
def get_department_by_id(department_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_departments_by_id(%s)", (department_id,))
        department = cursor.fetchone()
    return department

# Update Department
def update_departments(department_id, data):
    with connection.cursor() as cursor:
        cursor.execute("SELECT update_departments(%s, %s, %s)",
                       (department_id,  data['department_type'], data['role']))

# Delete Department
def delete_departments(department_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT delete_department(%s)", (department_id,))
