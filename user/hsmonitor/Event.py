"""This module creates types of Events that are specified by the subclasses."""


class Event():
    # The instantiation operation
    def __init__(self):
        # init variables here if needed
        self.datetime = 0
        self.uploadCode = 0
        self.data = 0
        self.nanoseconds = 0
        self.export_values = 0

    def getEventData(self):
        pass

    def parseMessage(self):
        pass
