from django.shortcuts import render
from requests.auth import HTTPDigestAuth
from datetime import datetime
from .models import Employees
import requests

def send_request(url, payload, username, password):
    try:
        auth = HTTPDigestAuth(username, password)
        response = requests.post(url, json=payload, auth=auth)
        response.raise_for_status()
        print(response.request.body)
        print(response.request.headers)
        return response.json()
    except requests.RequestException as e:
        print(f'Помилка запиту: {e}')
        return None

def add_to_dict(data_from_api, dict_to_add):
    for record in data_from_api['AcsEvent']['InfoList']:
        employee_no = record['employeeNoString']
        login_time = record['time']
        dict_to_add[employee_no] = login_time

def fetch_all_records():
    today = datetime.now().strftime('%Y-%m-%d')
    start_time = f'{today}T08:00:00+02:00'
    end_time = f'{today}T21:00:00+02:00'

    url = 'http://192.168.8.39/ISAPI/AccessControl/AcsEvent?format=json'
    username = 'admin'
    password = 'K04032000t'
    payload_template = {
        'AcsEventCond': {
            'searchID': 'access_control',
            'searchResultPosition': 0,
            'maxResults': 10,
            'major': 5,
            'minor': 38,
            'startTime': start_time,
            'endTime': end_time
        }
    }

    initial_data = send_request(url, payload_template, username, password)
    total_matches = initial_data['AcsEvent']['totalMatches']

    records_dict = {}

    add_to_dict(initial_data, records_dict)

    current_position = payload_template['AcsEventCond']['maxResults']

    while current_position < total_matches:
        payload_template['AcsEventCond']['searchResultPosition'] = current_position

        data = send_request(url, payload_template, username, password)

        add_to_dict(data, records_dict)

        current_position += payload_template['AcsEventCond']['maxResults']
    return records_dict


def index(request):
    api_records = fetch_all_records()
    db_employees = Employees.objects.all()

    comparison_result = []
    for employee in db_employees:
        if str(employee.employeeTerminalNo) in api_records:
            comparison_result.append({'employeeStringNo': employee.employeeTerminalNo, 'employeeName': employee.employeeName, 'status': 'Пікнувся'})
        else:
            comparison_result.append({'employeeStringNo': employee.employeeTerminalNo, 'employeeName': employee.employeeName, 'status': 'Не пікнувся'})

    return render(request, 'index.html', context={'comp_res': comparison_result})