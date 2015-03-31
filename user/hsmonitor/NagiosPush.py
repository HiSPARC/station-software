import logging

logger = logging.getLogger('hsmonitor.nagiospush')

from time import sleep, time
from subprocess import Popen, PIPE

TIMEOUT = 10


class TimeoutException(Exception):
    pass


class NagiosPush:
    def __init__(self, config):
        self.host = config["host"]
        self.port = int(config["port"])
        self.machine_name = config["machine_name"]

    def sendToNagios(self, nagiosResult):
        reportMessage = {}
        reportMessage['reportCode'] = nagiosResult.status_code
        reportMessage['textMessage'] = nagiosResult.description
        reportMessage['send_nscaPath'] = "data\\send_nsca_win32\\"
        reportMessage['nagiosServer'] = self.host  # Server IP
        reportMessage['serverPort'] = self.port
        reportMessage['hostComputer'] = self.machine_name  # On Nagios server
        reportMessage['serviceName'] = nagiosResult.serviceName

        send_nsca_command = ("echo %s,%s,%s,%s | %ssend_nsca -H %s -p %d -c "
                             "%ssend_nsca.cfg -d ," %
                             (reportMessage['hostComputer'],
                              reportMessage['serviceName'],
                              reportMessage['reportCode'],
                              reportMessage['textMessage'],
                              reportMessage['send_nscaPath'],
                              reportMessage['nagiosServer'],
                              reportMessage['serverPort'],
                              reportMessage['send_nscaPath']))

        v = Popen(send_nsca_command, shell=True, stdout=PIPE)
        t0 = time()
        try:
            while v.poll() is None:
                elapsed_time = time() - t0
                if elapsed_time >= TIMEOUT:
                    raise TimeoutException("Process won't quit!")
                sleep(1)
        except TimeoutException:
            v.kill()
            res = "send_nsca_command failed"
        else:
            res = v.communicate()[0]
        logger.debug('Check %s: Status code: %i, Status description: %s.\n'
                     '\t %s.' % (nagiosResult.serviceName,
                                 nagiosResult.status_code,
                                 nagiosResult.description, res))
