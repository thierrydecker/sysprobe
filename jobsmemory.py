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


def memory_virtual_memory(influxdb_config):
    """Retrieve the system memory usage

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.virtual_memory()
    host_type = helpers.get_host_type()
    #
    # TODO -> Add platform specific counters
    #
    client = helpers.get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "virtual_memory",
            "tags": {
                "host_type": host_type,
                "host_name": platform.node(),
            },
            "fields": {
                "total": result.total,
                "available": result.available,
                "used": result.used,
                "free": result.free,
            }
        }
    ]
    helpers.influxdb_write_points(client, record)
