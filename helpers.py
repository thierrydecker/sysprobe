import argparse
import logging
import logging.config
import sys
import threading

import yaml
import yaml.parser
import psutil
import requests.exceptions

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from influxdb.exceptions import InfluxDBServerError


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


def run_threaded(job_function, influxdb_config):
    """Call a function in a new thread

    :param job_function: The function to be called in a new thread
    :param influxdb_config: The InfluxDB configuration
    :return: None
    """
    job_thread = threading.Thread(target=job_function, daemon=True, args=(influxdb_config,))
    job_thread.start()


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


def get_host_type():
    """Get the host type

    :return: The host type
    """
    if psutil.BSD:
        host_type = "BSD"
    elif psutil.FREEBSD:
        host_type = "FREBSD"
    elif psutil.AIX:
        host_type = "AIX"
    elif psutil.POSIX:
        host_type = "POSIX"
    elif psutil.WINDOWS:
        host_type = "WINDOWS"
    elif psutil.LINUX:
        host_type = "LINUX"
    elif psutil.OSX:
        host_type = "OSX"
    elif psutil.NETBSD:
        host_type = "NETBSD"
    elif psutil.OPENBSD:
        host_type = "OPENBSD"
    elif psutil.SUNOS:
        host_type = "SUNOS"
    else:
        host_type = "UNKNOWN"
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
    """Write points to InfluxDB

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