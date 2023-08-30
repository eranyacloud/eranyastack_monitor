# EranyaCloud Monitor
## How to Run Project
`uvicorn main:app --reload --host 0.0.0.0 --port 9191`

## Systemd Service 
```
[Unit]
Description=GreenAlert Service
After=network.target
[Service]
WorkingDirectory=/opt/greenmonitor
ExecStart=uvicorn main:app --reload --host 0.0.0.0 --port 9191
[Install]
WantedBy=multi-user.target

```

## Sample CURLs For Using API

### Get Instance Metrics
```
curl -X 'GET'   'http://127.0.0.1:9191/get_metrics'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "server": {
    "instance_id": "af766182-101f-48be-8c80-0027b72c51f6"
  },
  "date": {
    "start_date": "2022-08-01",
    "start_time": "12:10:30",
    "end_date": "2022-08-02",
    "end_time": "23:10:30",
    "step": 15
  }
}' 
```

### Create or Modify Instance Alerts
```
curl -X 'POST' \
  'http://127.0.0.1:9191/alerts' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "project_name": "gc-project-127001",
  "instance_id": "F87CV-JFLD45848478121578",
  "cpu_value": 80,
  "memory_value": 70,
  "network_receive_value": 10240,
  "network_transmit_value": 20480,
  "iops_read_value": 10,
  "iops_write_value": 10
}'
```

### View Current Instance Alerts

```
curl -X 'GET' \
  'http://172.20.8.6:9191/alerts/gc-project-127001/F87CV-JFLD45848478121578' \
  -H 'accept: text/plain'
```

### Service Health Check

```
curl -X 'GET' \
  'http://172.20.8.6:9191/' \
  -H 'accept: application/json'
```


### Get Bandwidth Usage

```
curl -X 'GET' \
  'http://172.20.12.1:9191/bandwidth_usage/3e0cc509-05fb-4e5c-8569-076cdb928e50?starttime=1670297400&endtime=1670301000' \
  -H 'accept: application/json'
```
