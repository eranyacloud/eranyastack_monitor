import pytest
import requests
import json


def test_health_check():
    url = "http://172.20.12.1:9191/"
    response = requests.request("GET", url)
    assert response.status_code == 200


def test_getalerts_valid():
    url = "http://172.20.12.1:9191/alerts/gcloud/af766182-101f-48be-8c80-0027b72c51f6"
    response = requests.request("GET", url)
    assert response.status_code == 200

def test_getalerts_invalid():
    url = "http://172.20.12.1:9191/alerts/xxxxxx/af766xxxx182-101f-48bxxxe-8c80-0027b72c51f6"
    response = requests.request("GET", url)
    assert response.status_code == 404




def test_create_alerts_valid():
    url = "http://172.20.12.1:9191/alerts"
    payload = json.dumps({
  "project_name": "gcloud",
  "instance_id": "af766182-101f-48be-8c80-0027b72c51f6",
  "cpu_value": 80,
  "memory_value": 70,
  "network_receive_value": 10240,
  "network_transmit_value": 20480,
  "iops_read_value": 10,
  "iops_write_value": 10
})
    headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
     }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200

def test_create_alerts_invalid():
    url = "http://172.20.12.1:9191/alerts"
    payload = json.dumps({
  "cpu_value": 80,
  "memory_value": 70,
  "network_receive_value": 10240,
  "network_transmit_value": 20480,
  "iops_read_value": 10,
  "iops_write_value": 10
})
    headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
     }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert response.status_code == 422



def test_get_metrics_valid():
    url = "http://172.20.12.1:9191/get_metrics"
    payload = json.dumps({
  "server": {
    "instance_id": "af766182-101f-48be-8c80-0027b72c51f6"
  },
  "date": {
    "start_date": "2022-08-29",
    "start_time": "20:10:30",
    "end_date": "2022-08-29",
    "end_time": "22:10:30"
  }
})
    headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
     }

    response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200

def test_get_metrics_invalid():
    url = "http://172.20.12.1:9191/get_metrics"
    payload = json.dumps({
  "date": {
    "start_time": "20:10:30",
    "end_date": "2022-08-29",
    "end_time": "22:10:30"
  }
})
    headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
     }
    response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200 and response.content.decode() == "null"
