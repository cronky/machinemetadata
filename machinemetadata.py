import csv 
import platform
import psutil
from datetime import datetime

# Get system info
cpu = platform.processor()
memory = psutil.virtual_memory().total / (1024 ** 3) # Convert bytes to GB
mtype = platform.system() + ' ' + platform.release()

# Get uptime
uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
daily = int(uptime.seconds / 86400) 
weekly = daily // 7
monthly = weekly // 4
annual = monthly // 12

# Generate timestamps  
now = datetime.now()
start = now - uptime
end = now

# Write to CSV
with open('computer_data.csv', 'w', newline='') as f:
    writer = csv.writer(f) 
    writer.writerow(['cpu', 'memory', 'type', 'start', 'end', 'daily', 'weekly', 'monthly', 'annual'])
    row = [cpu, memory, mtype, start, end, daily, weekly, monthly, annual]
    writer.writerow(row)

print('System data with uptime written to CSV')