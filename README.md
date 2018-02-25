# SysProbe

A Python system probe

SysProbe collects system informations and logs them to a InfluxDB database.

The following informations can be collected:

- #### CPUs counters

    - Number of CPUs
    - CPU Frequencies (Including all CPUs in one value)
    - CPU Frequencies (Per CPU) 
    - CPU usage percent (Including all CPUs)
    - CPU usage percent (Per CPU)
    - CPU statistics (Seconds spent in context switches, interrupts, soft interrupts, syscalls)

- #### More to come...

### InfluxDB:

Sysprobe is currently developped with InfluxDB v1.4.3

### Main dependencies: