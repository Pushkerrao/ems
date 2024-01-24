from rest_framework.response import Response
from django.http import JsonResponse
from departments.departmentdboperations import *
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse
import json
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render


#API'S for departments
@api_view(['GET'])
def get_all_departments(request):
    try:
        departments = get_departments()
        return JsonResponse({"status": 1, "statusCode": 200, "message": "Data Fetched Successfully", "data": departments})
    except Exception as error:
        return JsonResponse({"status": 0, "statusCode": 500, "message": str(error)})

@api_view(['POST'])
def create_departments(request):
    try:
        # Assuming the request data contains department information
        data = request.data
        new_department_id = add_department(data)
        return JsonResponse({"status": 1, "statusCode": 200, "message": "Department added successfully", "data": data})
    except Exception as error:
        return JsonResponse({"status": 0, "statusCode": 500, "message": str(error)})


@api_view(['GET'])
def get_department(request, department_id):
    try:
        department = get_department_by_id(department_id)
        return JsonResponse({"status": 1, "statusCode": 200, "message": "Data Fetched Successfully", "data": department})
    except Exception as error:
        return JsonResponse({"status": 0, "statusCode": 500, "message": str(error)})

@api_view(['PUT'])
def api_update_department(request, department_id):
    try:
        
        # Assuming the request data contains updated department information
        data = request.data
        # Check if the department with the given ID exists
        existing_department = get_department_by_id(department_id)
        if not existing_department:
            return Response({"status": 0, "statusCode": 404, "message": f"Department with ID {department_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the update_department function to perform the update
        update_departments(department_id, data)

        return Response({"status": 1, "statusCode": 200, "message": f"Department with ID {department_id} updated successfully."}, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"status": 0, "statusCode": 500, "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def api_delete_department(request, department_id):
    
    try:
        # Check if the department with the given ID exists
        existing_department = get_department_by_id(department_id)
        if not existing_department:
            return Response({"status": 0, "statusCode": 404, "message": f"Department with ID {department_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the delete_department function to perform the deletion
        delete_departments(department_id)

        return Response({"status": 1, "statusCode": 200, "message": f"Department with ID {department_id} deleted successfully."}, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"status": 0, "statusCode": 500, "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Web methods for   Departments
@login_required
def departments(request):
    departments_list = get_departments()
    context = {
        'departments': departments_list,
    }
    return render(request, 'employee/departments.html', context)


@login_required
def manage_departments(request):
    department = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            department = get_department_by_id(id)

    context = {
        'department': department
    }
    return render(request, 'employee/manage_departments.html', context)


@login_required
def save_department(request):
    data = request.POST
    resp = {'status': 'failed'}
    
    
    try:
        department_id = data.get('department_id')  # Assuming 'department_id' is present in the data
        department_type = data.get('department_type')
        role = data.get('role')

        if department_id and department_id.isnumeric() and int(department_id) > 0:
            update_department(department_id, {
                'department_type': department_type,
                'role': role,
            })
        else:
            add_department({
                'department_type': department_type,
                'role': role,
            })

        resp['status'] = 'success'
    except Exception as e:
        resp['status'] = 'failed'
        print(e)

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_department(request):
    data = request.POST
    resp = {'status': 'failed'}
    
    try:
        if data.get('id'):
            delete_departments(data.get('id'))
            resp['status'] = 'success'
    except Exception as e:
        resp['status'] = 'failed'
        print(e)

    return HttpResponse(json.dumps(resp), content_type="application/json")
