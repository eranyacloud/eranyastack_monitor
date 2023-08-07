from sqlite3 import Date
from api.master_green_monitor import *
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, Field
from api.master_alert_monitor import Alert, KubernetesAlert,KubernetesAlerts, GreenAlert
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse
import requests

app = FastAPI(
    title="GreenMonitor",
    description="GreenWebCloud Instances Monitoring and Alerting Service",
    version="0.5.1",
)


# This function get Metrics from prometheus to customer or client
class server_model(BaseModel):
    instance_id: Union[str, None] = Field(default=None, example="af766182-101f-48be-8c80-0027b72c51f6")

class date_model(BaseModel):
    start_date: Union[str, None] = Field(default=None, example="2022-08-02")
    start_time: Union[str, None] = Field(default=None, example="20:10:30")
    end_date: Union[str, None] = Field(default=None, example="2022-08-02")
    end_time: Union[str, None] = Field(default=None, example="22:10:30")
    step: Union[int, None] = Field(default=1, example="1")

class monitor_model(BaseModel):
    server: Union[server_model, None] = None
    date: Union[date_model, None] = None

@app.get("/")
def health_check():
    return {"Status": "Ok"}

@app.get("/alerts/{project_name}/{instance_id}", response_class=PlainTextResponse)
def view_instance_alerts(project_name: str,instance_id: str):
    green_alert = GreenAlert()
    response_alert = green_alert.view_instance_alerts(project_name,instance_id)
    return response_alert

@app.post("/alerts")
def create_modify_alert(data: Alert):
    try:
        print(data)
        green_alert = GreenAlert()
        response_alert = green_alert.create_or_modify_alert(data.project_name,data.instance_id,data.cpu_value,data.memory_value,
            data.network_receive_value,data.network_transmit_value,data.iops_read_value,data.iops_write_value)
        return response_alert
    except Exception as err:
        print(err)

@app.post("/kubernetes_alerts")
def create_modify_alert(data: KubernetesAlert):
    try:
        print(data)
        kubernetes_alert = KubernetesAlerts()
        response_alert = kubernetes_alert.create_or_modify_kubernetes_alert(data.instances,data.cpu_min,data.cpu_max,data.memory_min,data.memory_max,data.check_time,data.nodegroup_id)
        return response_alert
    except Exception as err:
        print(err)

@app.delete("/kubernetes_alerts/{nodegroup_id}")
def delete_alert(nodegroup_id: str):
    try:
        kubernetes_alert = KubernetesAlerts()
        response_alert =kubernetes_alert.delete_kubernetes_alert(nodegroup_id)
        return response_alert
    except Exception as err:
        print(err)

@app.get("/get_metrics")
def get_metrics(data: monitor_model):
    try:
        green_monitor = GreenMonitor(data.server.instance_id,
                data.date.start_date,data.date.start_time,
                data.date.end_date,data.date.end_time,data.date.step)
        response_metrics = green_monitor.request_metrics()
        return response_metrics
    except Exception as err:
        print(err)

@app.get("/get_instant_metrics/{instance_Id}")
def get_instant_metrics(instance_Id):
    try:
        response_instant_metrics = request_instant_metrics(instance_Id)
        return response_instant_metrics
    except Exception as err:
        print(err)

@app.get("/bandwidth_usage/{instance_id}")
def view_instance_bandwidth(instance_id: str,starttime: str,endtime: str):
    download=byte_receives(instance_id,starttime,endtime)
    upload=byte_transmits(instance_id,starttime,endtime)
    try:
      return {"download": str(download) ,"upload": str(upload)}
    except:
      return JSONResponse(status_code=404,content="Data not found. Please check date and instanceId")
