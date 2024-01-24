from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse
from django.shortcuts import redirect
import json
from django.db import connection
import base64
from django.core.files.base import ContentFile
from employee.employeedboperations import * 
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from rest_framework import status
import os

#API'S for employees 
@api_view(['GET'])
def get_all_employees(request):
    try:
        employees = get_employees()
        return JsonResponse({"status": 1, "statusCode": 200, "message": "Data Fetched Successfully", "data": employees})
    except Exception as error:
        return JsonResponse({"status": 0, "statusCode": 500, "message": str(error)})


def save_uploaded_file(uploaded_file, folder='uploads'):
    # Ensure the folder exists
    folder_path = os.path.join('docs', folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the file to the specified folder
    file_path = default_storage.save(os.path.join(folder_path, uploaded_file.name), ContentFile(uploaded_file.read()))
    
    # Return the relative URL of the saved file
    return default_storage.url(file_path)
    
@api_view(['POST'])
def create_employee(request):
    try:
        # Assuming the request data contains employee information
        data = request.data
        uploaded_file = request.FILES.get('document')
        file_path = save_uploaded_file(uploaded_file)

        new_employee_id = add_employees(data, file_path)
        return JsonResponse({"status": 1, "statusCode": 200, "message": "Employee added successfully"})
    except Exception as error:
        return JsonResponse({"status": 0, "statusCode": 500, "message": str(error)})



@api_view(['GET'])
def get_employee(request, employee_id):
    try:
        employee = get_employee_by_id(employee_id)
        return JsonResponse({"status": 1, "statusCode": 200, "message": "Data Fetched Successfully", "data": employee})
    except Exception as error:
        return JsonResponse({"status": 0, "statusCode": 500, "message": str(error)})

@api_view(['PUT'])
def api_update_employee(request, employee_id):
    try:
        # Assuming the request data contains updated employee information
        data = request.data

        existing_employee = get_employee_by_id(employee_id)
        if not existing_employee:
            return Response({"status": 0, "statusCode": 404, "message": f"Employee with ID {employee_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the update_employee function to perform the update
        update_employee(employee_id, data)

        return Response({"status": 1, "statusCode": 200, "message": f"Employee with ID {employee_id} updated successfully."}, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"status": 0, "statusCode": 500, "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def api_delete_employee(request, employee_id):
    try:
        # Check if the employee with the given ID exists
        existing_employee = get_employee_by_id(employee_id)
        if not existing_employee:
            return Response({"status": 0, "statusCode": 404, "message": f"Employee with ID {employee_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the delete_employee function to perform the deletion
        delete_employees(employee_id)

        return Response({"status": 1, "statusCode": 200, "message": f"Employee with ID {employee_id} deleted successfully."}, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"status": 0, "statusCode": 500, "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#logout
def logoutuser(request):
    logout(request)
    return redirect('/')

#home page
@login_required
def home(request):
    with connection.cursor() as cursor:
        # Count total departments
        cursor.execute("SELECT COUNT(*) FROM department")
        total_department = cursor.fetchone()[0]

        # Count total employees
        cursor.execute("SELECT COUNT(*) FROM employees")
        total_employee = cursor.fetchone()[0]

    context = {
        'page_title': 'Home',
        'total_department': total_department,
        'total_employee': total_employee,
    }
    return render(request, 'employee/home.html', context)


# Web methods for employees 
@login_required
def employees(request):
    employees = get_employees()
    context = {
        'employees': employees,
    }

    return render(request, 'employee/employees.html', context)


@login_required
def manage_employees(request):
    employees = get_employees()
    context = {
        'employees': employees,
    }
    return render(request, 'employee/manage_employee.html', context)


@login_required
def save_employee(request):
    data = request.POST
    file_path = None

    try:
        employee_id = data.get("id")
        code = data.get('code', '')

        # Assuming your PostgreSQL functions handle the logic for adding and updating
        if employee_id:
            # Update existing employee
            update_employee(employee_id, data)

            # Check if a new document is provided for updating
            

            document_data = data.get('document', '')
            if document_data:
                document_content = base64.b64decode(document_data)
                # Assuming your PostgreSQL function handles file save
                save_uploaded_file(code, document_content)

        else:

            # Add a new employee
            uploaded_file = request.FILES.get('document')
            file_path = save_uploaded_file(uploaded_file)

            # file_path = save_uploaded_file(code, base64.b64decode(data.get('document', '')))
            new_employee_id = add_employees(data, file_path)

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failed', 'msg': 'An error occurred.'})

    return JsonResponse({'status': 'success'})


@login_required
def delete_employee(request):
    data =  request.POST
    resp = {'status':''}
    try:
        if data['id']:
            delete_employees(data['id'])
            resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_employee(request):
    employee = {}
    if request.method == 'GET':
        data = request.GET
        # Assuming get_employee_by_id is a PostgreSQL function
        employee = get_employee_by_id(data['id'])

    context = {
        'employee': employee,
    }
    return render(request, 'employee/view_employee.html', context)