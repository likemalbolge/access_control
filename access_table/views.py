from django.shortcuts import render
from requests.auth import HTTPDigestAuth
from datetime import datetime
from .models import Employees
import requests


def send_request(url, payload, username, password):
    try:
        response = requests.post(url, json=payload, auth=HTTPDigestAuth(username, password))
        response.raise_for_status()
        print(response.request.body)
        return response.json()
    except requests.RequestException as e:
        print(f'Помилка запиту: {e}')
        return None


def parse_records(data_from_api):
    return {
        record['employeeNoString']: record['time']
        for record in data_from_api.get('AcsEvent', {}).get('InfoList', [])
    }


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
    if not initial_data:
        return {}

    total_matches = initial_data.get('AcsEvent', {}).get('totalMatches', 0)
    records_dict = parse_records(initial_data)

    current_position = payload_template['AcsEventCond']['maxResults']

    while current_position < total_matches:
        payload_template['AcsEventCond']['searchResultPosition'] = current_position
        data = send_request(url, payload_template, username, password)
        if data:
            records_dict.update(parse_records(data))
        current_position += payload_template['AcsEventCond']['maxResults']

    return records_dict


def index(request):
    api_records = fetch_all_records()
    db_employees = Employees.objects.all()

    comparison_result = [
        {
            'employeeStringNo': employee.employeeTerminalNo,
            'employeeName': employee.employeeName,
            'status': 'Пікнувся' if str(employee.employeeTerminalNo) in api_records else 'Не пікнувся'
        }
        for employee in db_employees
    ]

    return render(request, 'index.html', context={'comp_res': comparison_result})
