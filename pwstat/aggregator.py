# Aggregator class
# : contains aggregate methods

import logging
from Queue import Empty
from threading import Thread, Event

from user_agents import parse

logger = logging.getLogger('pwstat_aggregator')


class Aggregator(Thread):
    def __init__(self, queue, writer, stat_list):
        Thread.__init__(self)
        self.queue = queue
        self.writer = writer
        self.stat_list = stat_list
        # match dictionary: used in calculate function
        # example 'stat_name': self.function_name
        self.match = {'timestamp': self.get_timestamp,
                      'user-agent': self.get_user_agent,
                      }
        # validate statistics specified
        for stat in stat_list:
            assert stat in self.match, \
                "'{}' did not match any stats in aggregator. Available stats: {}".format(stat, self.match.keys())
        self._stop = Event()

    # default thread method
    def run(self):
        logger.info("Aggregator starting...")
        while True:
            try:
                # timeout after 5 seconds
                temp = self.queue.get(timeout=5)
                self.writer.write(self.calculate(temp))
            except Empty:
                pass
            if self._stop.isSet():
                logger.info("Aggregator stopping...")
                break
        return

    # thread termination method
    def stop(self):
        self._stop.set()

    # aggregate functions
    def get_timestamp(self, data):
        return str(data[2])

    def get_user_agent(self, data):
        ua_string = data[0]['user-agent']
        user_agent = parse(ua_string)
        return 'mobile' if user_agent.is_mobile else 'desktop' if user_agent.is_pc else 'other'

    # main method
    def calculate(self, data):
        # call aggregate functions and return dictionary of stats
        # data has the form (headers, body, timestamp)
        logger.info("Starting aggregation...")
        result = dict()
        for stat in self.stat_list:
            stat_function = self.match[stat]
            result[stat] = stat_function(data)
        return result
