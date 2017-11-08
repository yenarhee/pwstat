# Writer class
# : saves data in a file

import csv
import logging

logger = logging.getLogger('pwstat_writer')


class Writer(object):
    def __init__(self, filename):
        self.filename = filename
        logger.info("Writer for {} initiated".format(self.filename))

    def write(self, my_dict):
        with open('{}'.format(self.filename), 'a+') as f:  # Just use 'w' mode in 3.x
            logger.info("Opened file")
            f.seek(0)  # jump to the beginning of the file
            try:
                header = csv.reader(f).next()
                logger.info("Header found")
                dict_writer = csv.DictWriter(f, header)
            except StopIteration:
                dict_writer = csv.DictWriter(f, my_dict.keys())
                dict_writer.writeheader()
                logger.info("Header written")
            f.seek(0, 2)  # jump back to the end of the file
            try:
                dict_writer.writerow(my_dict)
                logger.info("Written to file")
            except ValueError:
                # TODO: key not found in header
                logger.error('Header does not contain all keys for: {}'.format(my_dict))
                return False
            return True
