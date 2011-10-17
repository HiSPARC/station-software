# define the nagios result struct
class NagiosResult(object):
    def __init__(self, status_code = None, description = None, serviceName = None):
        self.status_code = status_code
        self.description = description
        self.serviceName = serviceName
