from django.shortcuts import render
from requests.auth import HTTPDigestAuth
from datetime import datetime
from .models import Employee, Record
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

def add_record_to_db(data):
    for item in data['AcsEvent']['InfoList']:
        obj, created = Record.objects.get_or_create(employee=Employee.objects.get(
            employeeTerminalNo=item['employeeNoString']), acs_time=item['time'])


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
    add_record_to_db(initial_data)

    current_position = payload_template['AcsEventCond']['maxResults']

    while current_position < total_matches:
        payload_template['AcsEventCond']['searchResultPosition'] = current_position
        data = send_request(url, payload_template, username, password)
        if data:
            add_record_to_db(data)
        current_position += payload_template['AcsEventCond']['maxResults']


def index(request):
    fetch_all_records()
    db_records = Record.objects.all()

    return render(request, 'index.html', context={'db_records': db_records})