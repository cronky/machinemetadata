## Fetch local machine metadata to populate CCF On premise
# CSV file format as defined here https://www.cloudcarbonfootprint.org/docs/on-premise/
# V3 with CPU util PLUS GPU and output to screen. 
# Will require pip installs to satisfy dependencies. (TODO List these)

import csv
import os
import platform
import psutil
import cpuinfo
import socket
import GPUtil
from datetime import datetime
import locale

# Record when we started for script duration calculation
processStartTime = datetime.now()
# Check CPU Utilisation at the start in case running checks effects usage?
cpu_util = psutil.cpu_percent(interval=1) 

# HDD and SSD counting - currently broken
def count_disks():
  hdd_count = 0
  ssd_count = 0

  for partition in psutil.disk_partitions():
    if 'cdrom' in partition.opts or partition.fstype == '':
      continue

    disk_info = partition.device

   # if disk_info.drive_type == psutil.DISK_TYPE_SSD:
    #  ssd_count += 1
    # elif disk_info.drive_type == psutil.DISK_TYPE_HDD:
    #  hdd_count += 1

  return ssd_count, hdd_count

# Detect OS
system = platform.system()
# Better on Windows?
cpu = cpuinfo.get_cpu_info()['brand_raw']
if(cpu =="") : 
    print("CPU was blank taking secondary")
    cpu = platform.processor()

memory = round(psutil.virtual_memory().total / (1024 ** 3)) 

# These aren't needed for CCF but might be useful additional meta data
arch = platform.architecture() # e.g. 64bit, WindowsPE
machine = platform.machine()   # e.g. AMD64

if(socket.getfqdn != ''):
    hostname = socket.getfqdn()
else :
    hostname =  hostname = socket.gethostname()

user = os.getlogin()

# Get uptime info
uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
daily = int(uptime.seconds / 86400)
# The below are placeholders that need fixing (or blanking)
weekly = daily // 7 
monthly = weekly // 4
annual = monthly // 12

# Generate timestamps
now = datetime.now()
start = now - uptime
end = now

# Print System results   
print(f"User: {user}")
print(f"Operating System: {system}")
print(f"Machine: {machine}")
print(f"Architecture: {arch}")  
print(f"CPU: {cpu}")
print(f"Memory: {memory} GB")
print(f"Uptime: {uptime}")  
print(f"CPU Utilization: {cpu_util}%") 

# Latest more reliable GPU code using GPUtil
gpu = GPUtil.getGPUs()
# If we have GPUs then output details (and add them to the file?)
gpuCount = len(gpu)
if(gpuCount < 1):
    print("No GPU detected")
else:
    print(f" {gpuCount} GPU(s) found")
    for g in gpu:
        print(f"GPU: {g.name} Memory:{g.memoryTotal} {round(g.memoryTotal/g.memoryUsed)}% used Load: {g.load} ")


# Get disk info - commented out for now
# ssd_count, hdd_count = count_disks()

#print(f"SSDs: {ssd_count}")
#print(f"HDDs: {hdd_count}")

# disks = psutil.disk_partitions() 
 
#disk_usage = psutil.disk_usage('/')

#print("Disks:")
#for disk in disks:
#    print(disk.device, disk.fstype)

#print(f"Disk Usage: {round(disk_usage.used/2**30)} of {round(disk_usage.total/2**30)} GB") 

# Work out location info - start with Locale information 
# using the locale information is a bit of hack but will do for now
country = locale.getlocale()[0].split('_')[1]
region = locale.getlocale()[0].split('_')[0]

# TO DO Add the extra details to seperate CSV
# i.e. disk.device, disk.fstype, disk_usage.total/2**30


# Write to CSV - perhaps 2 versions - 1 CCF compatible and a more comprehensive version?
# CCF Format:
# cpuDescription	string	Central processing unit description
# memory	number	Number of gigabytes of memory usage
# machineType	string	Machine type (Ie. server, laptop, desktop)
# startTime	Date	Timestamp recording the start day/time of usage
# endTime	Date	Timestamp recording end day/time of usage
# country	string	Country where server was located
# region	string	Region or state within country server was located
# machineName?	string	Physical host name
# cost?	number	The amount of cost associated with each row
# cpuUtilization?	number	Specific server utilization percentage (Ie. 50% = 50)
# powerUsageEffectiveness?	number	Power usage effectiveness for data center
# dailyUptime	number	Active usage hours in the last day
# weeklyUptime	number	Active usage hours in the last week
# monthlyUptime	number	Active usage hours in the last month
# annualUptime	number	Active usage hours in the last year

# TODO put in an average cost per computer type?
cost = 0
pue = ''

ccfRowHeadings = ['cpuDescription', 'memory', 'start', 'end', 'country', 'region', 'machineName', 'cost', 'cpuUtilization', 'powerUsageEffectiveness', 'daily', 'weekly', 'monthly', 'annual']
rows = [[cpu, memory, start, end, country, region, hostname, cost, cpu_util, pue, daily, weekly, monthly, annual]]
# pprint(rows)

fileName = "mmd_" + str(hostname) + "_" + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + ".csv"

with open(fileName, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(ccfRowHeadings) 
    writer.writerows(rows)
    
print('System data written to CCF CSV: ' + os.path.dirname(os.path.abspath(fileName)) + "\\" + fileName)
processEndTime = datetime.now()
duration =  processEndTime - processStartTime
print('Script Duration: ' + str(duration.seconds) + ' seconds')
