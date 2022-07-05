import logging


class Logging_operations():
    def __init__(self, filename='log.txt'):
        self.logging_config(filename=filename)

    def logging_config(self, filename):
        # creating logging file
        logging.basicConfig(filename=filename, level=logging.DEBUG,
                            format="%(asctime)s %(message)s")

    def error(self, e):
        logging.error(e)

    def info(self, e):
        logging.info(e)
