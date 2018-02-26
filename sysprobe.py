#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import logging.config

import schedule

import helpers
import jobs


def main():
    """Entry point of the SysProbe application

    :return: None
    """
    flags = helpers.parser_create()
    config_data = helpers.get_config(flags.config_file)
    influxdb_config = helpers.get_influxdb_config(config_data)
    jobs_config = helpers.get_jobs_config(config_data)
    loggers_config = helpers.get_loggers_config(config_data)
    helpers.loggers_configure(loggers_config)
    logger = logging.getLogger()

    available_jobs = jobs.get_available_jobs()
    for job, interval in jobs_config.items():
        if job in available_jobs:
            job = available_jobs[job]
            schedule.every(interval).seconds.do(helpers.run_threaded, job, influxdb_config)
        else:
            logger.warning('Unknown job name: {}'.format(job))

    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
