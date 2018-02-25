#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import platform
import sys
import threading

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from influxdb.exceptions import InfluxDBServerError

import psutil
import requests.exceptions
import schedule
import yaml
import yaml.parser


def parser_create():
    """Creates the arguments parser

    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", type=str, help="yaml configuration file name", required=True)
    return parser.parse_args()


def get_config(config_file):
    """Loads a .yml configuration file

    :param config_file: The path name of the yml configuration file
    :return: A dictionary of the configuration
    """
    try:
        with open(config_file, 'r') as f:
            config_yml = f.read()
        return yaml.load(config_yml)
    except FileNotFoundError:
        print('Could not find configuration file: {}'.format(config_file))
        print('Sopping')
        sys.exit(1)
    except yaml.parser.ParserError as e:
        print("Yaml parse error")
        print("{}".format(e))
        sys.exit(1)


def get_loggers_config(config_data):
    """Extracts loggers configuration from configuration data

    :param config_data: Configuration data
    :return: A dictionary of the loggers configuration
    """
    try:
        config = {k: config_data[k] for k in ('loggers',)}
        config = config['loggers']
        return config
    except KeyError:
        print('Could not find loggers section in configuration file')
        print('Sopping.')
        sys.exit(1)


def loggers_configure(loggers_config):
    """Configure the loggers

    :param loggers_config: Loggers configuration data
    :return:  None
    """
    try:
        logging.config.dictConfig(loggers_config)
    except ValueError as e:
        print('Loggers configuration error: {}'.format(e))
        sys.exit(1)


def get_influxdb_config(config_data):
    """Extracts InfluxDB configuration from configuration data

    :param config_data: Configuration data
    :return: A dictionary of the InfluxDB configuration
    """
    try:
        config = {k: config_data[k] for k in ('influxdb',)}
        config = config['influxdb']
        return config
    except KeyError:
        print('Could not find InfluxDB section in configuration file')
        print('Sopping.')
        sys.exit(1)


def get_jobs_config(config_data):
    """Extracts jobs configuration from configuration data

    :param config_data: Configuration data
    :return: A dictionary of the jobs configuration
    """
    try:
        config = {k: config_data[k] for k in ('jobs',)}
        config = config['jobs']
        return config
    except KeyError:
        print('Could not find jobs section in configuration file')
        print('Sopping.')
        sys.exit(1)


def get_host_type():
    """Get the host type

    :return: The host type
    """
    host_type = "Unknown"
    if psutil.BSD:
        host_type = "BSD"
    if psutil.FREEBSD:
        host_type = "FREBSD"
    if psutil.AIX:
        host_type = "AIX"
    if psutil.POSIX:
        host_type = "POSIX"
    if psutil.WINDOWS:
        host_type = "WINDOWS"
    if psutil.LINUX:
        host_type = "LINUX"
    if psutil.OSX:
        host_type = "OSX"
    if psutil.NETBSD:
        host_type = "NETBSD"
    if psutil.OPENBSD:
        host_type = "OPENBSD"
    if psutil.SUNOS:
        host_type = "SUNOS"
    return host_type


def get_influxdb_client(influxdb_config):
    """Get a new InfluxDB client

    :param influxdb_config: A dictionary of InfluxDB configuration
    :return: A InfluxDB client object
    """
    host = influxdb_config["host"] if "host" in influxdb_config else "localhost"
    port = influxdb_config["port"] if "port" in influxdb_config else 8086
    username = influxdb_config["username"] if "username" in influxdb_config else "root"
    password = influxdb_config["password"] if "password" in influxdb_config else "root"
    database = influxdb_config["database"] if "database" in influxdb_config else None
    ssl = influxdb_config["ssl"] if "ssl" in influxdb_config else False
    verify_ssl = influxdb_config["verify_ssl"] if "verify_ssl" in influxdb_config else False
    timeout = influxdb_config["timeout"] if "timeout" in influxdb_config else None
    retries = influxdb_config["retries"] if "retries" in influxdb_config else 3
    use_udp = influxdb_config["use_udp"] if "use_udp" in influxdb_config else False
    udp_port = influxdb_config["udp_port"] if "udp_port" in influxdb_config else 4444
    proxies = influxdb_config["proxies"] if "proxies" in influxdb_config else {}
    client = InfluxDBClient(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
            ssl=ssl,
            verify_ssl=verify_ssl,
            timeout=timeout,
            retries=retries,
            use_udp=use_udp,
            udp_port=udp_port,
            proxies=proxies,
    )
    return client


def influxdb_write_points(client, record):
    """

    :param client: A InfluxDB client object
    :param record:  A dictionary of the InfluxDB record to write
    :return: None
    """
    logger = logging.getLogger()
    try:
        client.write_points(record)
    except InfluxDBClientError:
        logger.warning("InfluxDBClientError writing {}".format(record))
    except InfluxDBServerError:
        logger.warning("InfluxDBServerError writing {}".format(record))
    except requests.exceptions.ConnectTimeout:
        logger.warning("Connection timeout writing {}".format(record))
    else:
        logger.debug("Wrote {}".format(record))


def job_cpu_count(influxdb_config):
    """Retrieve the number of cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_count()
    client = get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_count",
            "tags": {
                "host": platform.node(),
            },
            "fields": {
                "value": result,
            }
        }
    ]
    influxdb_write_points(client, record)


def job_cpu_freq(influxdb_config):
    """Retrieve the cpu frequency

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_freq(percpu=False)
    client = get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_freq",
            "tags": {
                "host": platform.node(),
            },
            "fields": {
                "current": result.current,
                "min": result.min,
                "max": result.max,
            }
        }
    ]
    influxdb_write_points(client, record)


def job_cpu_freq_percpu(influxdb_config):
    """Retrieve the frequency of each cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_freq(percpu=True)
    client = get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_freq_percpu",
                    "tags": {
                        "host": platform.node(),
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "current": result.current,
                        "min": result.min,
                        "max": result.max,
                    }
                }
        )
    influxdb_write_points(client, records)


def job_cpu_percent(influxdb_config):
    """Retrieve the cpu usage in percent

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_percent(interval=.1, percpu=False)
    client = get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_percent",
            "tags": {
                "host": platform.node(),
            },
            "fields": {
                "current": result,
            }
        }
    ]
    influxdb_write_points(client, record)


def job_cpu_percent_percpu(influxdb_config):
    """Retrieve the cpu usage of each cpu in percent

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_percent(interval=.1, percpu=True)
    client = get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_percent_percpu",
                    "tags": {
                        "host": platform.node(),
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "current": result,
                    }
                }
        )
    influxdb_write_points(client, records)


def job_cpu_stats(influxdb_config):
    """Retrieve the cpu statistics

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_stats()
    client = get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_stats",
            "tags": {
                "host": platform.node(),
            },
            "fields": {
                "ctx_switches": result.ctx_switches,
                "interrupts": result.interrupts,
                "soft_interrupts": result.soft_interrupts,
                "syscalls": result.syscalls,
            }
        }
    ]
    influxdb_write_points(client, record)


def job_cpu_times(influxdb_config):
    """Retrieve the cpu times

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_times(percpu=False)
    host_type = get_host_type()
    #
    # TODO -> Add platform specific counters
    #
    client = get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_times",
            "tags": {
                "host": platform.node(),
                "host_type": host_type,
            },
            "fields": {
                "ctx_switches": result.user,
                "interrupts": result.system,
                "soft_interrupts": result.idle,
            }
        }
    ]
    influxdb_write_points(client, record)


def job_cpu_times_percpu(influxdb_config):
    """Retrieve the cpu times per cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_times(percpu=True)
    host_type = get_host_type()
    #
    # TODO -> Add platform specific counters
    #
    client = get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_times_percpu",
                    "tags": {
                        "host": platform.node(),
                        "host_type": host_type,
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "ctx_switches": result.user,
                        "interrupts": result.system,
                        "soft_interrupts": result.idle, }
                }
        )
    influxdb_write_points(client, records)


def job_cpu_times_percent(influxdb_config):
    """Retrieve the cpu times percent

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    result = psutil.cpu_times_percent(interval=0.1, percpu=False)
    client = get_influxdb_client(influxdb_config)
    record = [
        {
            "measurement": "cpu_times_percent",
            "tags": {
                "host": platform.node(),
            },
            "fields": {
                "current": result,
            }
        }
    ]
    influxdb_write_points(client, record)


def job_cpu_times_percent_percpu(influxdb_config):
    """Retrieve the cpu times percent per cpu

    :param influxdb_config: A dictionary of InfluxDB to connect to
    :return: None
    """
    results = psutil.cpu_times_percent(interval=.1, percpu=True)
    client = get_influxdb_client(influxdb_config)
    records = []
    for cpu_num, result in enumerate(results):
        records.append(
                {
                    "measurement": "cpu_times_percent_percpu",
                    "tags": {
                        "host": platform.node(),
                        "cpu_num": cpu_num,
                    },
                    "fields": {
                        "current": result,
                    }
                }
        )
    influxdb_write_points(client, records)


def get_available_jobs():
    """Returns the availables jobs

    Creates a mapping of jobs names to functions to call to perform the jobs

    :return: A dictionary of the available jobs
    """
    available_jobs = {
        'cpu_count': job_cpu_count,
        'cpu_freq': job_cpu_freq,
        'cpu_freq_percpu': job_cpu_freq_percpu,
        'cpu_percent': job_cpu_percent,
        'cpu_percent_percpu': job_cpu_percent_percpu,
        'cpu_stats': job_cpu_stats,
        'cpu_times': job_cpu_times,
        'cpu_times_percpu': job_cpu_times_percpu,
        'cpu_times_percent': job_cpu_times_percent,
        'cpu_times_percent_percpu': job_cpu_times_percent_percpu,
    }
    return available_jobs


def run_threaded(job_function, influxdb_config):
    """Call a function in a new thread

    :param job_function: The function to be called in a new thread
    :param influxdb_config: The InfluxDB configuration
    :return: None
    """
    job_thread = threading.Thread(target=job_function, daemon=True, args=(influxdb_config,))
    job_thread.start()


def main():
    """Entry point of the SysProbe application

    :return: None
    """
    flags = parser_create()
    config_data = get_config(flags.config_file)
    influxdb_config = get_influxdb_config(config_data)
    jobs_config = get_jobs_config(config_data)
    loggers_config = get_loggers_config(config_data)
    loggers_configure(loggers_config)
    logger = logging.getLogger()

    available_jobs = get_available_jobs()
    for job, interval in jobs_config.items():
        if job in available_jobs:
            job = available_jobs[job]
            schedule.every(interval).seconds.do(run_threaded, job, influxdb_config)
        else:
            logger.warning('Unknown job name: {}'.format(job))

    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
