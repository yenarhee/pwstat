import Queue
import logging
import sys
import traceback

from . import receiver, aggregator, writer


def main(output_file, stat_list, port):
    logger = logging.getLogger('pwstat_main')
    logger.info('Starting...')
    try:
        q = Queue.Queue()
        w = writer.Writer(output_file)
        a = aggregator.Aggregator(q, w, stat_list)
        a.start()
        # TODO: receiver as a thread (start, stop)
        r = receiver.Receiver(port, queue=q)
        r.start()
    except:
        traceback.print_exc()
        try:
            r.stop()
            a.stop()
        except NameError:
            pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Gathers password statistics in a csv file.')
    parser.add_argument('statistics', type=str,
                        help='comma separated statistics list, e.g. user-agent,timestamp')
    parser.add_argument('--port', type=int, default=8088,
                        help='listen port, default=8088')
    parser.add_argument('--output', type=str, default='output.csv',
                        help='output file name, default=output.csv')
    args = parser.parse_args()

    # set up logging to file
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_string)
    logging.basicConfig(level=logging.DEBUG,
                        format=format_string,
                        filename='pwstat.log',
                        filemode='a')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # run main function
    sys.exit(main(args.output, args.statistics.split(','), args.port))
