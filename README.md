## SysProbe

    A Python system probe

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

    psutil v5.4.3

    influxdb v5.0.0

    schedule v0.5.0

    PyYAML v3.12