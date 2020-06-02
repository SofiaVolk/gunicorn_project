from multiprocessing import Process
import time
import signal
import select
import errno
import sys
import os

from gunicorn.checker import dataset

SIZE_MAX = 512  # one page


class Checker(Process):
    def __init__(self, ppid, log, pipe):
        self.log = log
        self.pipe = pipe
        self.ppid = ppid
        self.workers = []
        self.file_changed = False
        self.file_ctime = 0
        super().__init__()

    def run(self):
        self.init_signals()
        self.log.info(f'Booting checker with pid: {self.pid}')

        while True:
            self.sleep()
            self.file_changed, self.file_ctime = dataset.maybe_update_dataset(self.file_ctime)
            if self.file_changed:
                for worker_pid in self.workers:
                    try:
                        os.kill(worker_pid, signal.SIGUSR2)
                    except OSError as e:
                        if e.errno != errno.ESRCH:  # otherwise checker terminates
                            raise

            if not self.is_master_alive():
                time.sleep(0.1)
                sys.exit(0)

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

    def is_master_alive(self):
        """
         Shut down if master changed or ended ungracefully
        """
        if self.ppid != os.getppid():
            self.log.info("Master changed, shutting down: %s", self)
            return False
        return True

