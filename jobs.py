# -*- coding: utf-8 -*-

#
# Standard library imports
#
import platform
#
# Third party imports
#
import psutil
#
# Project's imports
#
import helpers


def cpu_times(influxdb_config):
    """Retrieve the cpu times

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_times(percpu=False)
    host_type = helpers.get_host_type()
    #
    # TODO -> Add platform specific counters
    #
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_times",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "user": result.user,
                "system": result.system,
                "idle": result.idle,
            }
        }
    ]
    helpers.influxdb_write_points(client, record)


def cpu_times_percpu(influxdb_config):
    """Retrieve the cpu times per cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_times(percpu=True)
    host_type = helpers.get_host_type()
    #
    # TODO -> Add platform specific counters
    #
    client = helpers.get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_times_percpu",
                    "tags": {
                        "host_type": host_type,
                        "host_name": platform.node(),
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "user": result.user,
                        "system": result.system,
                        "idle": result.idle,
                    }
                }
        )
    helpers.influxdb_write_points(client, records)


def cpu_percent(influxdb_config):
    """Retrieve the cpu usage in percent

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_percent(interval=.1, percpu=False)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_percent",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "current": result,
            }
        }
    ]
    helpers.influxdb_write_points(client, record)


def cpu_percent_percpu(influxdb_config):
    """Retrieve the cpu usage of each cpu in percent

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_percent(interval=.1, percpu=True)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_percent_percpu",
                    "tags": {
                        "host_type": host_type,
                        "host_name": platform.node(),
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "current": result,
                    }
                }
        )
    helpers.influxdb_write_points(client, records)


def cpu_times_percent(influxdb_config):
    """Retrieve the cpu times percent

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_times_percent(interval=0.1, percpu=False)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_times_percent",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "user": result.user,
                "system": result.system,
                "idle": result.idle,
            }
        }
    ]
    helpers.influxdb_write_points(client, record)


def cpu_times_percent_percpu(influxdb_config):
    """Retrieve the cpu times percent per cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_times_percent(interval=.1, percpu=True)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_times_percent_percpu",
                    "tags": {
                        "host_type": host_type,
                        "host_name": platform.node(),
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "user": result.user,
                        "system": result.system,
                        "idle": result.idle,
                    }
                }
        )
    helpers.influxdb_write_points(client, records)


def cpu_count(influxdb_config):
    """Retrieve the number of cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_count()
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_count",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "value": result,
            }
        }
    ]
    helpers.influxdb_write_points(client, record)


def cpu_stats(influxdb_config):
    """Retrieve the cpu statistics

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_stats()
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_stats",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "ctx_switches": result.ctx_switches,
                "interrupts": result.interrupts,
                "soft_interrupts": result.soft_interrupts,
                "syscalls": result.syscalls,
            }
        }
    ]
    helpers.influxdb_write_points(client, record)


def cpu_freq(influxdb_config):
    """Retrieve the cpu frequency

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_freq(percpu=False)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_freq",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "current": result.current,
                "min": result.min,
                "max": result.max,
            }
        }
    ]
    helpers.influxdb_write_points(client, record)


def cpu_freq_percpu(influxdb_config):
    """Retrieve the frequency of each cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_freq(percpu=True)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_freq_percpu",
                    "tags": {
                        "host_type": host_type,
                        "host_name": platform.node(),
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "current": result.current,
                        "min": result.min,
                        "max": result.max,
                    }
                }
        )
    helpers.influxdb_write_points(client, records)


def network_io_counters(influxdb_config):
    """Retrieve the network io counters

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.net_io_counters(pernic=False)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "network_io_counters",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "bytes_sent": result.bytes_sent,
                "bytes_recv": result.bytes_recv,
                "bytes_total": result.bytes_sent + result.bytes_recv,
                "packets_sent": result.packets_sent,
                "packets_recv": result.packets_recv,
                "packets_total": result.packets_sent + result.packets_recv,
                "errors_in": result.errin,
                "errors_out": result.errout,
                "errors_total": result.errin + result.errout,
                "drops_in": result.dropin,
                "drops_out": result.dropout,
                "drops_total": result.dropin + result.dropout,

            }
        }
    ]
    helpers.influxdb_write_points(client, record)


def network_io_counters_pernic(influxdb_config):
    """Retrieve the network io counters per nic card

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.net_io_counters(pernic=True)
    host_type = helpers.get_host_type()
    client = helpers.get_influxdb_client(influxdb_config)
    records = []
    for nic, counters in results.items():
        records.append(
                {
                    "measurement": "network_io_counters_pernic",
                    "tags": {
                        "host_type": host_type,
                        "host_name": platform.node(),
                        "nic_name": nic,
                    },
                    "fields": {
                        "bytes_sent": counters.bytes_sent,
                        "bytes_recv": counters.bytes_recv,
                        "bytes_total": counters.bytes_sent + counters.bytes_recv,
                        "packets_sent": counters.packets_sent,
                        "packets_recv": counters.packets_recv,
                        "packets_total": counters.packets_sent + counters.packets_recv,
                        "errors_in": counters.errin,
                        "errors_out": counters.errout,
                        "errors_total": counters.errin + counters.errout,
                        "drops_in": counters.dropin,
                        "drops_out": counters.dropout,
                        "drops_total": counters.dropin + counters.dropout,
                    }
                }
        )
    helpers.influxdb_write_points(client, records)
