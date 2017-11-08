# Receiver class
# : receives requests and parse headers, body, timestamp using processor functions
# : puts processed results in the queue

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from .processor import Processor
from datetime import datetime
import logging
import ssl

logger = logging.getLogger('pwstat_receiver')


class Receiver(object):
    # This class will handle incoming requests
    class RequestHandler(BaseHTTPRequestHandler):

        # Handler for the POST requests
        def do_POST(self):
            logger.info('POST received')
            timestamp = datetime.now()  # get timestamp for now
            headers = self.headers
            bodyfp = self.rfile
            # read body
            content_len = int(headers.getheader('content-length', 0))
            body = bodyfp.read(content_len)
            # parse headers, body, timestamp with processor
            logger.debug(Processor.process(headers, body, timestamp))
            logger.info('Data added in the queue')
            # add data to queue for aggregator
            self.queue.put(Processor.process(headers, body, timestamp))
            return

    def __init__(self, port, queue):
        # initialize server
        self.server = HTTPServer(('localhost', self.port), self.RequestHandler)
        self.port = port
        self.queue = queue
        self.RequestHandler.queue = self.queue

    def start(self):
        # create a web server and define the handler to manage the incoming request
        # HTTP
        # self.server = HTTPServer(('', self.port), self.RequestHandler) 
        # HTTPS
        self.server.socket = ssl.wrap_socket(self.server.socket, certfile='cert_localhost.pem',
                                             keyfile='key_localhost.pem', server_side=True)
        logger.info('Started httpserver on port {}'.format(self.port))
        self.server.serve_forever()

    def stop(self):
        logger.info('Shutting down the server')
        try:
            self.server
        except NameError:  # self.server not defined
            return
        self.server.server_close()
