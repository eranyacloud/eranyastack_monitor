import requests
from . import config
#import sentry_sdk
#from sentry_sdk.integrations.flask import FlaskIntegration
class GreenMonitor():
    def __init__(self,instance_id=None,start_date=None,start_time=None,end_date=None,end_time=None,step=None,metrics=[]):
        self.instance_id = instance_id
        self.metrics = metrics
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.step = step
    def request_metrics(self):
        sstep = self.step * 60
        #sentry_sdk.init( dsn="http://2d29f808e6434c4d9ed345237d14f3bb@172.20.11.10:9000/2",
            #integrations=[FlaskIntegration()],
            # Set traces_sample_rate to 1.0 to capture 100%
            # # of transactions for performance monitoring.
            # # We recommend adjusting this value in production.
            #traces_sample_rate=1.0)
        #response=requests.get(config.PROMETHEUS + '/api/v1/query', params={'query': 'libvirt_domain_state_code and changes(libvirt_domain_state_code[10m]) > 0'})
        #total_cpu = "libvirt_domain_info_virtual_cpus{host=~"$compute", job=~"prometheus-libvirt-exporter"}"
        total_cpu = 'libvirt_domain_info_virtual_cpus{instanceId="%s"}'%(self.instance_id)
        cpu_usage =  '(avg by(domain) (irate(libvirt_domain_info_cpu_time_seconds_total{instanceId=~"%s"}[30s])) * 100) / on() group_right() (libvirt_domain_info_virtual_cpus{instanceId=~"%s"} - 0)'%(self.instance_id,self.instance_id)
        total_mem = 'libvirt_domain_info_maximum_memory_bytes{instanceId="%s",job=~"prometheus-libvirt-exporter"}'%(self.instance_id)
        available_mem = 'libvirt_domain_stat_memory_unused_bytes{instanceId="%s", job=~"prometheus-libvirt-exporter"}'%(self.instance_id)
        mem_usage = 'libvirt_domain_info_maximum_memory_bytes{instanceId="%s", job=~"prometheus-libvirt-exporter"} - libvirt_domain_stat_memory_unused_bytes{instanceId="%s", job=~"prometheus-libvirt-exporter"}'%(self.instance_id,self.instance_id)
        iops_read_disk = 'rate(libvirt_domain_block_stats_read_requests_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        iops_write_disk = 'rate(libvirt_domain_block_stats_write_requests_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        troughput_read_disk = 'rate(libvirt_domain_block_stats_read_bytes_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        troughput_write_disk = 'rate(libvirt_domain_block_stats_write_bytes_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rtx_troughput = 'rate(libvirt_domain_interface_stats_receive_bytes_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_troughput = 'rate(libvirt_domain_interface_stats_transmit_bytes_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rx_packets = 'rate(libvirt_domain_interface_stats_receive_packets_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_packet = 'rate(libvirt_domain_interface_stats_transmit_packets_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rx_packet_error = 'rate(libvirt_domain_interface_stats_receive_errors_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_packet_error = 'rate(libvirt_domain_interface_stats_transmit_errors_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rx_packet_drop = 'rate(libvirt_domain_interface_stats_receive_drops_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_packet_drop = 'rate(libvirt_domain_interface_stats_transmit_drops_total{instanceId="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        querys = [total_cpu,cpu_usage,total_mem,available_mem,mem_usage,iops_read_disk,iops_write_disk,troughput_read_disk,troughput_write_disk,rtx_troughput
        ,tx_troughput,rx_packets,tx_packet,rx_packet_error,tx_packet_error,rx_packet_drop,tx_packet_drop]


        self.metrics=[]

        for i in querys:
            #print(config.PROMETHEUS + '/api/v1/query_range'+ '?start=' + self.start_date + 'T' + self.start_time + '.000Z&end=' + self.end_date + 'T' + self.end_time + '.000Z&step=60s&query=' + i )
            response=requests.get(config.PROMETHEUS + '/api/v1/query_range'+ '?start=' + self.start_date + 'T' + self.start_time + '.000Z&end=' + self.end_date + 'T' + self.end_time + '.000Z&step='+str(sstep)+'s&query='+ i)
            self.metrics.append(response.json()['data']['result'])
            #print(response.url)
        return {
            "total_cpu":self.metrics[0],
            "cpu_usage":self.metrics[1],
            "total_mem":self.metrics[2],
            "available_mem":self.metrics[3],
            "mem_usage":self.metrics[4],
            "iops_read_disk":self.metrics[5],
            "iops_write_disk":self.metrics[6],
            "troughput_read_disk":self.metrics[7],
            "troughput_write_disk":self.metrics[8],
            "rtx_troughput":self.metrics[9],
            "tx_troughput":self.metrics[10],
            "rx_packets":self.metrics[11],
            "tx_packet":self.metrics[12],
            "rx_packet_error":self.metrics[13],
            "tx_packet_error":self.metrics[14],
            "rx_packet_drop":self.metrics[15],
            "tx_packet_drop":self.metrics[16],
        }


#### Get Metrics Live (Return only one value per queyry)
def request_instant_metrics(instance_Id):
    cpu_usage_percent =  '(irate(libvirt_domain_info_cpu_time_seconds_total{instanceId="%s"}[30s]))*100  / libvirt_domain_info_virtual_cpus{instanceId="%s"}'%(instance_Id,instance_Id)
    mem_usage_percent = '(libvirt_domain_info_maximum_memory_bytes{instanceId="%s", job=~"prometheus-libvirt-exporter"} - libvirt_domain_stat_memory_unused_bytes{instanceId="%s", job=~"prometheus-libvirt-exporter"} ) / libvirt_domain_info_maximum_memory_bytes{instanceId="%s", job=~"prometheus-libvirt-exporter"} * 100'%(instance_Id,instance_Id,instance_Id)
    total_mem_bytes = 'libvirt_domain_info_maximum_memory_bytes{instanceId="%s",job=~"prometheus-libvirt-exporter"}'%(instance_Id)
    available_mem_bytes = 'libvirt_domain_stat_memory_unused_bytes{instanceId="%s", job=~"prometheus-libvirt-exporter"}'%(instance_Id)
    querys = [cpu_usage_percent,mem_usage_percent,total_mem_bytes,available_mem_bytes]


    metrics=[]
    for i in querys:
        #print(config.PROMETHEUS + '/api/v1/query_range'+ '?start=' + self.start_date + 'T' + self.start_time + '.000Z&end=' + self.end_date + 'T' + self.end_time + '.000Z&step=60s&query=' + i )
        response=requests.get(config.PROMETHEUS + '/api/v1/query?query='+ i)
        metrics.append(response.json()['data']['result'])
        #print(response.url)
    return {
        "cpu_usage_percent":metrics[0],
        "mem_usage_percent":metrics[1],
        "total_mem_bytes":metrics[2],
        "available_mem_bytes":metrics[3]
    }




    def save_to_redis(self):
        pass






def preprocess():
    pass


def byte_receives(instanceId,starttime,endtime):
    step=int((int(endtime)-int(starttime))/11000)+1
    if step < 2:
        step=2
    download=requests.get(config.PROMETHEUS + '/api/v1/query_range?query=libvirt_domain_interface_stats_receive_bytes_total{instanceId="'+str(instanceId)+'"}&start='+str(starttime)+'&end='+str(endtime)+'&step='+str(step))
    print(config.PROMETHEUS + '/api/v1/query_range?query=libvirt_domain_interface_stats_receive_bytes_total{instanceId="'+str(instanceId)+'"}&start='+str(starttime)+'&end='+str(endtime)+'&step='+str(step))
    sum=0
    try:
      for instanx in download.json()['data']['result']:
          i=0
          vector=instanx['values']
          while i < len(vector)-1:
              if int(vector[i+1][1]) >= int(vector[i][1]) :
                  sum+= int(vector[i+1][1]) - int(vector[i][1])

              else:
                  sum+= int(vector[i+1][1])
              i+=1
      return(sum)
    except:
      return(0)

def byte_transmits(instanceId,starttime,endtime):
    step=int((int(endtime)-int(starttime))/11000)+1
    if step < 2:
        step=2
    upload=requests.get(config.PROMETHEUS + '/api/v1/query_range?query=libvirt_domain_interface_stats_transmit_bytes_total{instanceId="'+str(instanceId)+'"}&start='+str(starttime)+'&end='+str(endtime)+'&step='+str(step))
    print(config.PROMETHEUS + '/api/v1/query_range?query=libvirt_domain_interface_stats_transmit_bytes_total{instanceId="'+str(instanceId)+'"}&start='+str(starttime)+'&end='+str(endtime)+'&step='+str(step))
    sum=0
    try:
      for instanx in upload.json()['data']['result']:
          i=0
          vector=instanx['values']
          while i < len(vector)-1:
              if int(vector[i+1][1]) >= int(vector[i][1]) :
                  sum+= int(vector[i+1][1]) - int(vector[i][1])

              else:
                  sum+= int(vector[i+1][1])
              i+=1
      return(sum)
    except:
      return(0)
