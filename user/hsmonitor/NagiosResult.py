"""Define the Nagios result structure."""


class NagiosResult(object):
    def __init__(self, status_code=None, description=None, serviceName=None):
        self.status_code = status_code
        self.description = description
        self.serviceName = serviceName
