# V2 with CPU util and output to screen. 

import csv
import platform
import gpuinfo
import psutil
from datetime import datetime

# Get GPU info 
gpu = gpuinfo.get_gpu_info()

# Get disk info
disks = psutil.disk_partitions()  
disk_usage = psutil.disk_usage('/')

# Get system info
cpu = platform.processor()
cpu_util = psutil.cpu_percent(interval=1) 
memory = psutil.virtual_memory().total / (1024 ** 3) 

arch = platform.architecture()
machine = platform.machine()
system = platform.system()

# Get uptime info
uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
daily = int(uptime.seconds / 86400)
weekly = daily // 7 
monthly = weekly // 4
annual = monthly // 12

# Generate timestamps
now = datetime.now()
start = now - uptime
end = now

# Print results   
print(f"System: {system}")
print(f"Machine: {machine}")
print(f"Architecture: {arch}")  
print(f"CPU: {cpu}")
print(f"CPU Utilization: {cpu_util}%") 
print(f"Memory: {memory} GB")
print(f"Uptime: {uptime}")  

# Print results 
print(f"GPU: {gpu['model']}")

print("Disks:")
for disk in disks:
    print(disk.device, disk.fstype)

print(f"Disk Usage: {disk_usage.total/2**30} GB") 

# Write rows to CSV
#rows.append([gpu['model'], disk.device, disk.fstype, disk_usage.total/2**30])


# Write to CSV
rows = [[cpu, memory, start, end, daily, weekly, monthly, annual, cpu_util]]

with open('computer_data-v2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['cpu', 'memory', 'start', 'end', 'daily', 'weekly', 'monthly', 'annual', 'cpu_util']) 
    writer.writerows(rows)
    
print('System data with utilization written to CSV')