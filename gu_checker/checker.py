from multiprocessing import Process
import time
import signal
import select
import errno
import sys
import os

from gunicorn.checker import picklefile

SIZE_MAX = 512  # one page


class Checker(Process):
    def __init__(self, log, pipe):
        self.log = log
        self.pipe = pipe
        self.workers = []
        super().__init__()

    def run(self):
        self.init_signals()
        self.log.info(f'Booting checker with pid: {self.pid}')

        while True:
            self.sleep()
            if picklefile.test_pickle():
                for worker_pid in self.workers:
                    try:
                        os.kill(worker_pid, signal.SIGUSR2)
                    except OSError as e:
                        if e.errno != errno.ESRCH:  # otherwise checker terminates
                            raise

    def init_signals(self):
        signal.signal(signal.SIGTERM, self.handle_exit)

    def handle_exit(self, sig, frame):
        self.log.info(f'Checker exiting (pid: {self.pid})')
        time.sleep(0.1)
        sys.exit(0)

    def sleep(self):
        try:
            ready = select.select([self.pipe], [], [], 1.0)  # wait 1 sec for info in pipe
            if not ready[0]:
                return
            self.workers = [int(x) for x in os.read(self.pipe, SIZE_MAX).decode('utf-8').split()]
        except (select.error, OSError) as e:
            error_number = getattr(e, 'errno', e.args[0])
            if error_number not in [errno.EAGAIN, errno.EINTR]:
                raise
        except KeyboardInterrupt:
            sys.exit()

