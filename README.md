## SysProbe

A Python system monitor agent

### Introduction

SysProbe collects system informations and logs them to a InfluxDB database.

### Trackable counters

- CPU times (user, system, idle)
- CPU times per CPU (user, system, idle)
- CPU percent (usage percent)
- CPU percent per CPU (usage percent)
- CPU times percent (user, system, idle)
- CPU times percent per CPU (user, system, idle
- CPU count (number of CPUs)
- CPU statistics (ctx_switches, interrupts, soft_interrupts, syscalls)
- CPU frequencies (current, min, max)
- CPU frequencies per CPU (current, min, max)

More to come...

### Developped on

- Windows 10
- Python v3.6
- InfluxDB v1.4

### Main dependencies

- PyYAML v3.12
- schedule v0.5.0
- psutil v5.4.3
- influxdb v5.0.0
    
### Code of conduct

Checkout our [Code of conduct](CODE_OF_CONDUCT.md).

### SysProbe's Wiki

Checkout our [Wiki](https://github.com/thierrydecker/sysprobe/wiki).

### Contributing to the project

Checkout our [Contributing section](CONTRIBUTING)