"""This module creates types of Events that are specified by the subclasses."""

import struct
import base64
import logging

import EventExportValues

logger = logging.getLogger('hsmonitor.event')


class BaseEvent(object):

    """Base class for processing events from the buffer

    This module processes messages from buffer database and gets out all
    available data. This data is stored to then be uploaded to the
    datastore.

    """

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


class BaseHiSPARCEvent(BaseEvent):

    """Process HiSPARC messages from a buffer."""

    def __init__(self, message):
        """Determines message type from the argument.

        Check if this might be a legacy message.
        Proceed to unpack the message.

        """
        super(BaseHiSPARCEvent, self).__init__()

        # get the message field in the message table
        self.message = message[1]

    def check_trailing_bytes(self):
        """Check if the struct_offset reached the end of the message

        Use in combination with ``unpackSeqMessage``. When (you think)
        you have read the entire message this will check if there any
        bytes left.

        """
        if len(self.message[self._struct_offset:]):
            raise Exception('Not entire message was parsed, %d bytes left.' %
                            len(self.message[self._struct_offset:]))

    def unpackMessage(self):
        """This needs to be defined separately for each message type"""
        pass

    def parseMessage(self):
        self.unpackMessage()
        self.check_trailing_bytes()

        # get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]

        return self.getEventData()

    def getEventData(self):
        """Get all event data necessary for an upload.

        This function parses the export_values variable declared in the
        EventExportValues and figures out what data to collect for an
        upload to the datastore. It returns a list of dictionaries, one
        for each data element.

        """

        eventdata = []
        for value in self.export_values:
            data_uploadcode = value[0]

            try:
                data = self.__getattribute__(value[1])
            except AttributeError:
                # This is not a legacy message. Therefore, it should contain
                # all exported variables, but alas, it apparently doesn't.
                # if not self.version == 21:
                #     print 'I missed this variable: ', value[2]
                continue

            if data_uploadcode in ['TR1', 'TR2', 'TR3', 'TR4']:
                # Encode compressed binary traces for transport over http.
                # The pickled data stream is ascii-safe, but the binary
                # compressed traces are not. At the server side, the
                # blobvalues are base64-decoded.
                data = base64.b64encode(data)

            eventdata.append({"data_uploadcode": data_uploadcode,
                              "data": data})

        return eventdata

    def unpackSeqMessage(self, fmt=None):
        """Sequentially unpack message with a format.

        This method is used to read from the same buffer multiple times,
        sequentially. A private variable will keep track of the current offset.
        This is more convenient than keeping track of it yourself multiple
        times, or hardcoding offsets.

        """
        if not fmt:
            # This is an initialization call
            self._struct_offset = 0
            return

        if fmt == 'LVstring':
            # Request for a labview string. That is, first a long for the
            # length, then the string itself.
            length = self.unpackSeqMessage('>L')[0]
            fmt = ">%ds" % length

        # For debugging, keeping track of trailing bytes
        # print len(self.message[self._struct_offset:]), struct.calcsize(fmt)

        data = struct.unpack_from(fmt, self.message,
                                  offset=self._struct_offset)
        self._struct_offset += struct.calcsize(fmt)

        return data


class BaseWeatherEvent(BaseEvent):

    """Process weather station messages from a buffer."""

    def __init__(self, message):
        super(BaseWeatherEvent, self).__init__()
        self.message = message[1]

    def fix_boolean(self, datastring):
        if datastring == 'TRUE':
            return True
        elif datastring == 'FALSE':
            return False
        else:
            raise ValueError('Value is neither TRUE or FALSE.')

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        if name == "date":
            return self.datetime.date().isoformat()
        elif name == "time":
            return self.datetime.time().isoformat()
        else:
            raise AttributeError(name)

    def getEventData(self):
        """Get all event data necessary for an upload.

        This function parses the export_values variable declared in the
        EventExportValues and figures out what data to collect for an
        upload to the datastore. It returns a list of dictionaries, one
        for each data element.

        """

        eventdata = []
        for value in self.export_values:
            eventdata.append({"data_uploadcode": value[0],
                              "data": self.__getattribute__(value[1])})

        return eventdata


class BaseLightningEvent(BaseWeatherEvent):

    """Process lightning detector messages from a buffer."""

    pass
