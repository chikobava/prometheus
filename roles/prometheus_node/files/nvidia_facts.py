#!/bin/python
from pynvml import *
try:
    nvmlInit()
    gpuNum = nvmlDeviceGetCount()
    file = open("/etc/ansible/facts.d/nvidia.fact","w")
    file.write("{\"nvidia_gpu_number\" : \"%d\"}" %(gpuNum))
    file.close
    exit(0)
except NVMLError as error:
    file = open("/etc/ansible/facts.d/nvidia.fact","w")
    file.write("{\"nvidia_gpu_number\" : \"0\"}")
    file.close
    exit(0)
exit(0)

