#!/bin/python
# Simple script, which gathers information about GPUs and puts it into a file to expose it for node-exporter
from __future__ import print_function
from pynvml import *
import sys, traceback

try:
  nvmlInit()
  try:
    driverVersion = nvmlSystemGetDriverVersion()
    try:
      gpuNum = nvmlDeviceGetCount()
      for i in range(gpuNum):
        try:
          filename = "/etc/node-exporter/gpu_%d.prom" % (i,)
          with open(filename,"w") as file:
            handle = nvmlDeviceGetHandleByIndex(i)
            info = nvmlDeviceGetMemoryInfo(handle)
            device_name = nvmlDeviceGetName(handle)
            try:
              utilization = nvmlDeviceGetUtilizationRates(handle)
              file.write ("node_gpu_%d_util{device_name=\"%s\", device_id=\"%d\"} %d\n" %(i,device_name,i,utilization.gpu))
            except NVMLError as error:
              traceback.print_exc(file=sys.stderr)
              print("Failed nvmlDeviceGetUtilizationRates", file=sys.stderr)
            file.write ("node_gpu_%d_total_memory{device_name=\"%s\", device_id=\"%d\"} %d\n" %(i,device_name,i,info.total))
            file.write ("node_gpu_%d_used_memory{device_name=\"%s\", device_id=\"%d\"} %d\n" %(i,device_name,i,info.used))
            file.write ("node_gpu_%d_core_temp{device_name=\"%s\", device_id=\"%d\"} %d\n" %(i,device_name,i,nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)))


        except NVMLError as error:
          traceback.print_exc(file=sys.stderr)
          with open("/etc/node-exporter/gpu_issues.prom", "w") as file:
            file.write("node_gpu_errors 1\n")
          exit(1)
      with open("/etc/node-exporter/gpu_issues.prom", "w") as file:
        file.write("node_gpu_errors 0\n")
      exit(0)
    except NVMLError as error:
      traceback.print_exc(file=sys.stderr)
      with open("/etc/node-exporter/gpu_issues.prom","w") as file:
        file.write("node_gpu_errors 1\n")
      exit(1)
  except NVMLError as error:
    traceback.print_exc(file=sys.stderr)
    with open("/etc/node-exporter/gpu_issues.prom","w") as file:
      file.write("node_gpu_errors 1\n")
    exit(1)
except NVMLError as error:
  traceback.print_exc(file=sys.stderr)
  with open("/etc/node-exporter/gpu_issues.prom","w") as file:
    file.write("node_gpu_errors 1\n")
  exit(1)
