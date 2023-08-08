# machinemetadata
Collecting Metadata and metrics from an on premise machine for CCF. This output could be aggregated and imported into CCF.

Example output (in addition to a CSV file output)

User: [username]
Operating System: Windows
Machine: AMD64
Architecture: ('64bit', 'WindowsPE')
CPU: AMD Ryzen 9 5900HS with Radeon Graphics
Memory: 15 GB
Uptime: 10 days, 1:59:57.999999
CPU Utilization: 0.0%
 1 GPU(s) found
GPU: NVIDIA GeForce GTX 1650 with Max-Q Design Memory:4096.0 25% used Load: 0.09
System data written to CCF CSV: [PATH]\mmd_[HOSTNAME]_2023_8_8.csv
Script Duration: 4 seconds


Example CSV File Output:

cpuDescription,memory,start,end,country,region,machineName,cost,cpuUtilization,powerUsageEffectiveness,daily,weekly,monthly,annual
AMD Ryzen 9 5900HS with Radeon Graphics,15,2023-07-29 15:25:40.649405,2023-08-08 17:25:38.649404,United Kingdom,English,hostname,0,0.0,,0,0,0,0
