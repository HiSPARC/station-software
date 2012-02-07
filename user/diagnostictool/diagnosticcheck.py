from definitions import status


class DiagnosticCheck:
    status = status.HASNT_RUN
    results = None
    message = None
    name = None

    def run(self):
        self.status = self._check()
        if self.status is None:
            self.message = "Unknown failure. Please report."
            self.status = status.FAIL

    def __str__(self):
        return self.name
