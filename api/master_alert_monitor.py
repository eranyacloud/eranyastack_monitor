import os
from jinja2 import Environment, FileSystemLoader
from scp import SCPClient
from typing import Union
from pydantic import BaseModel, Field
from paramiko import SSHClient
from api import config
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse

env = Environment(loader=FileSystemLoader('templates'))

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(config.prometheus_ip, config.prometheus_port)

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())


class Alert(BaseModel):
    project_name: str
    instance_id: str
    cpu_value: Union[int, None] = Field(default=None, example=80)
    memory_value: Union[int, None] = Field(default=None, example=70)
    network_receive_value: Union[int, None] = Field(default=None, example=10240)
    network_transmit_value: Union[int, None] = Field(default=None, example=20480)
    iops_read_value: Union[int, None] = Field(default=None, example=10)
    iops_write_value: Union[int, None] = Field(default=None, example=10)

class KubernetesAlert(BaseModel):
    nodegroup_id: Union[str, None] = Field(default=None, example="NG1")
    instances: Union[list, None] = Field(default=None)
    cpu_min: Union[int, None] = Field(default=None, example=10)
    cpu_max: Union[int, None] = Field(default=None, example=90)
    memory_min: Union[int, None] = Field(default=None, example=20)
    memory_max: Union[int, None] = Field(default=None, example=80)
    check_time: Union[str, None] = Field(default=None, example="5m")


class GreenAlert():
    def create_or_modify_alert(self,project_name=None,instance_id=None,cpu_value=None,memory_value=None,
            network_receive_value=None,network_transmit_value=None,iops_read_value=None,iops_write_value=None):

        filename = project_name+"-"+instance_id+".yaml"
        template = env.get_template('alert.yaml')
        output = template.render(project_name=project_name,instance_id=instance_id,cpu_value=cpu_value,memory_value=memory_value,network_receive_value=network_receive_value,network_transmit_value=network_transmit_value,iops_read_value=iops_read_value,iops_write_value=iops_write_value)
        with open('rules/'+filename, 'w') as f:
            f.write(output)
        scp.put('rules/'+filename, remote_path='/etc/prometheus/instance_alerts/')
        ssh.exec_command('systemctl reload prometheus.service')
        scp.close()
        return {"Alert Create or Updated.": instance_id}

    def view_instance_alerts(self,project_name=None,instance_id=None):
        try:
            scp.get("/etc/prometheus/instance_alerts/"+project_name+"-"+instance_id+".yaml","rules/"+project_name+"-"+instance_id+".yaml")
        except:
            return JSONResponse(status_code=404,content="Alerts not exists")
        if os.path.exists("rules/"+project_name+"-"+instance_id+".yaml"):
            return FileResponse("rules/"+project_name+"-"+instance_id+".yaml")
        else:
            return JSONResponse(status_code=404,content="Not Found")

class KubernetesAlerts():
    def create_or_modify_kubernetes_alert(self,instances=None,cpu_min=None,cpu_max=None,memory_min=None,memory_max=None,check_time=None,nodegroup_id=None):
        filename = nodegroup_id+".yaml"
        template = env.get_template('kubernetes_alert.yaml')
        context = {'instances': instances,'cpu_min': cpu_min,'cpu_max': cpu_max,'memory_min': memory_min,'memory_max': memory_max,'check_time': check_time,'nodegroup_id': nodegroup_id}
        output = template.render(context)
        with open('rules/'+filename, 'w') as f:
            f.write(output)
        scp.put('rules/'+filename, remote_path='/etc/prometheus/kubernetes_alerts/')
        ssh.exec_command('systemctl reload prometheus.service')
        scp.close()
        return {"Alert Create or Updated.": nodegroup_id}

    def delete_kubernetes_alert(self,nodegroup_id):
        filename = nodegroup_id+".yaml"
        ssh.exec_command(f"mv /etc/prometheus/kubernetes_alerts/{filename} /etc/prometheus/kubernetes_alerts/deleted/")
        ssh.exec_command("systemctl reload prometheus.service")
        return {"Alert Deleted.": nodegroup_id}
