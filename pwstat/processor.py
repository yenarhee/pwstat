# Processor class with static methods
# : gets headers, body, timestamp
# : returns header and body data
#    e.g. POST form variables, cookies, keyword parameters

import re
from Cookie import SimpleCookie as cookie


class Processor(object):
    def __init__(self):
        return

    # main function
    @staticmethod
    def process(headers, body, timestamp):
        # process
        return Processor.process_headers(headers), Processor.process_body(body), timestamp

    # helper functions
    @staticmethod
    def process_headers(headers):
        # process header data and return useful info as a dictionary
        headers_dict = dict(headers)
        # parse cookie
        try:
            cookiestring = headers_dict['cookie']
            c = cookie()
            cookie_dict = {}
            c.load(cookiestring)
            for key in c:
                cookie_dict[key] = c[key].value
            headers_dict['cookie'] = cookie_dict
        except KeyError:
            # there is no cookie
            pass
        return headers_dict

    @staticmethod
    def process_body(body):
        # process body data and return POST form variables as a dictionary
        result = {}
        regex = r"^(\w*)=(\w*)(?:&(\w*)=(\S*))*"
        match = re.match(regex, body)
        if match:
            it = iter(match.groups())
            for key in it:
                result[key] = next(it)

        return result
