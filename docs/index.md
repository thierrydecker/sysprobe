## SysProbe

    A Python system monitor agent

### Introduction

    SysProbe collects system informations and logs them to a InfluxDB database.

### Trackable counters

    Number of CPUs
    CPU Frequencies (Including all CPUs in one value)
    CPU Frequencies (Per CPU)
    CPU usage percent (Including all CPUs)
    CPU usage percent (Per CPU)
    CPU statistics (Seconds spent in context switches, interrupts, soft interrupts, syscalls)

    More to come...

### Tested on

    Python v3.6
    

### Main dependencies


    PyYAML v3.12
    schedule v0.5.0
    psutil v5.4.3
    influxdb v5.0.0