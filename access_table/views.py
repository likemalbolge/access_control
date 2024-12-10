from datetime import datetime

from django.shortcuts import render
import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime

def get_records_from_terminal():
    today = datetime.now().strftime('%Y-%m-%d')
    start_time = f'{today}T08:00:00+02:00'
    end_time = f'{today}T21:00:00+02:00'

    url = 'http://192.168.8.39/ISAPI/AccessControl/AcsEvent?format=json'
    auth = HTTPDigestAuth('admin', 'K04032000t')
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

    initial_response = requests.post(url, auth=auth, data=json.dumps(payload_template))
    print(initial_response.status_code)
    initial_data = json.loads(initial_response.text)
    total_matches = initial_data['AcsEvent']['totalMatches']

    records_dict = {}
    current_position = 0

    while current_position < total_matches:
        payload_template['AcsEventCond']['searchResultPosition'] = current_position
        response = requests.post(url, auth=auth, data=json.dumps(payload_template))
        print(response.status_code)
        data = json.loads(response.text)

        for record in data['AcsEvent']['InfoList']:
            employee_no = record.get('employeeNoString', 'unknown')
            time = record.get('time', 'unknown')
            records_dict[employee_no] = time

        current_position += payload_template['AcsEventCond']['maxResults']

    print(records_dict)
    return records_dict

def index(request):
    return render(request, 'index.html', context={'records': get_records_from_terminal()})