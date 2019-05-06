from multiprocessing import Process
import time
import signal
import sys


class Checker(Process):
    def __init__(self, log):
        self.log = log
        super().__init__()

    def run(self):
        self.init_signals()
        self.log.info(f'Booting checker with pid: {self.pid}')

        # some task instead of loop
        while True:
            time.sleep(1)

    def init_signals(self):
        signal.signal(signal.SIGTERM, self.handle_exit)

    def handle_exit(self, sig, frame):
        self.log.info(f'Checker exiting (pid: {self.pid})')
        time.sleep(0.1)
        sys.exit(0)
