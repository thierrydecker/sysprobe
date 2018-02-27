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
    """Retrieve the network io counters per NIC

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
