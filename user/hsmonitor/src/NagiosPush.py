import subprocess
from Check import *
import sys
from hslog import log
import time

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
        reportMessage['reportCode'] = nagiosResult.status_code      # Report code to send to Nagios
        reportMessage['textMessage'] = nagiosResult.description     # Message string to send to Nagios
        reportMessage['send_nscaPath'] = "../data/send_nsca_win32/" # Path to the send_nsca.exe
        reportMessage['nagiosServer'] = self.host                   # Nagios server IP address
        reportMessage['serverPort'] = self.port                     # Server port
        reportMessage['hostComputer'] = self.machine_name           # On nagios server
        reportMessage['serviceName'] = nagiosResult.serviceName     # Service name on Nagios server

        send_nsca_command = "echo %s,%s,%s,%s | %ssend_nsca -H %s -p %d -c %ssend_nsca.cfg -d ," % \
                            (reportMessage['hostComputer'], reportMessage['serviceName'],
                            reportMessage['reportCode'], reportMessage['textMessage'],
                            reportMessage['send_nscaPath'], reportMessage['nagiosServer'],
                            reportMessage['serverPort'], reportMessage['send_nscaPath'])
        v = subprocess.Popen(send_nsca_command, shell=True, stdout=subprocess.PIPE)
        t0 = time.time()
        try:
            while v.poll() is None:
                elapsed_time = time.time() - t0
                if elapsed_time >= TIMEOUT:
                    raise TimeoutException("Process won't quit!")
                time.sleep(1)
        except TimeoutException:
            v.kill()
            res = "send_nsca_command failed"
        else:
            res = v.communicate()[0]
        log("Check %s: Status code: %i, Status description: %s.\n\t %s." %
            (nagiosResult.serviceName, nagiosResult.status_code,
             nagiosResult.description, res))
