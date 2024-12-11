from django.shortcuts import render
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
import json
import time




def send_request(url, payload, username, password):
    response = requests.post(
        url,
        auth=HTTPDigestAuth(username, password),
        json=payload
    )
    response.raise_for_status()
    print(response.request.body)
    print(response.request.headers)
    return response.json()  # Парсинг JSON відповіді


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
    current_position = 0

    while current_position < total_matches:
        payload_template['AcsEventCond']['searchResultPosition'] = current_position

        data = send_request(url, payload_template, username, password)

        for record in data['AcsEvent']['InfoList']:
            employee_no = record['employeeNoString']
            login_time = record['time']
            records_dict[employee_no] = login_time

        current_position += payload_template['AcsEventCond']['maxResults']
        time.sleep(5)

    return records_dict


def index(request):
    return render(request, 'index.html', context={'terminal_data': fetch_all_records()})