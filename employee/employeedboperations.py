from django.db import connection


#GET All Employees
def get_employees():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_employees()")
        employees = cursor.fetchall()
    return employees

#Adding/Creating employees
def add_employees(data, file_path):
    with connection.cursor() as cursor:
        cursor.execute("SELECT create_employee(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (data['code'], data['firstname'], data['middlename'], data['lastname'], data['gender'],
                        data['dob'], data['contact'], data['address'], data['email'], data['date_hired'],
                        file_path, data['manager_name'], data['salary'], data['status']))
        new_employee_id = cursor.fetchone()[0]
    return new_employee_id

#Fetching employee by  id
def get_employee_by_id(employee_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_employee(%s)", (employee_id,))
        employee = cursor.fetchone()
    return employee
        
#updating employee by id
def update_employee(employee_id, data):
    with connection.cursor() as cursor:
        cursor.execute("SELECT update_employee(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (employee_id, data['code'], data['firstname'], data['middlename'], data['lastname'],
                        data['gender'], data['dob'], data['contact'], data['address'], data['email'],
                        data['date_hired'], data['document'], data['manager_name'], data['salary'], data['status']))
#delete employee by id 
def delete_employees(employee_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT delete_employee(%s)",(employee_id,))
