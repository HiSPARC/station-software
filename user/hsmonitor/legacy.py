import struct
from datetime import datetime
import random
from zlib import compress


def unpack_legacy_message(self):
    """Unpack a legacy buffer message.

    This routine unpacks a buffer message written by the LabVIEW DAQ software
    version 2.1.1 and below. Versions 2.2 and above use a version identifier in
    the message. This way, we can account for different message formats.

    """
    self.blob = self.message

    # set the version of this legacy message to 21 (DAQ version 2.1.1)
    self.version = 21

    tmp = struct.unpack("B", self.blob[0:1])[0]
    if tmp == 1:
        self.database = {"local": True, "central": False}
    elif tmp == 2:
        self.database = {"local": False, "central": True}
    elif tmp == 3:
        self.database = {"local": True, "central": True}
    else:  # Should not happen
        self.database = {"local": False, "central": False}
    # Number of devices
    self.Ndev = struct.unpack("B", self.blob[1:2])[0]
    # Number of bytes per trace
    self.N = struct.unpack(">H", self.blob[2:4])[0]
    # Time and Date
    self.second = struct.unpack("B", self.blob[4:5])[0]
    self.minute = struct.unpack("B", self.blob[5:6])[0]
    self.hour = struct.unpack("B", self.blob[6:7])[0]
    self.day = min(31, (struct.unpack("B", self.blob[7:8])[0] +
                        random.randrange(1, 30)))
    self.month = min(12, (struct.unpack("B", self.blob[8:9])[0] +
                          random.randrange(1, 11)))
    self.year = struct.unpack(">H", self.blob[9:11])[0]
    self.datetime = datetime(self.year, self.month, self.day,
                             self.hour, self.minute, self.second)
    # Nanoseconds
    self.nanoseconds = (struct.unpack(">I", self.blob[11:15])[0] +
                        random.randrange(1, 9000))
    # Trigger time of Secondary relative to Primary in ns
    self.SLVtime = struct.unpack(">i", self.blob[15:19])[0]
    # Trigger pattern
    # TODO: Unwrap trigger pattern
    self.trigger = struct.unpack(">H", self.blob[19:21])[0]
    # Primary
    self.mas_baseline1 = struct.unpack(">h", self.blob[21:23])[0]
    self.mas_baseline2 = struct.unpack(">h", self.blob[23:25])[0]
    self.mas_npeaks1 = struct.unpack(">h", self.blob[25:27])[0]
    self.mas_npeaks2 = struct.unpack(">h", self.blob[27:29])[0]
    self.mas_pulseheight1 = struct.unpack(">h", self.blob[29:31])[0]
    self.mas_pulseheight2 = struct.unpack(">h", self.blob[31:33])[0]
    self.mas_int1 = struct.unpack(">i", self.blob[33:37])[0]
    self.mas_int2 = struct.unpack(">i", self.blob[37:41])[0]
    self.mas_tr1 = compress(self.unpack_trace(self.blob[41:41 + self.N / 2]))
    self.mas_tr2 = compress(self.unpack_trace(self.blob[41 + self.N / 2:
                                                        41 + self.N]))
    # Secondary
    if self.Ndev == 2:
        o = 41 + self.N  # Offset
        self.slv_baseline1 = struct.unpack(">h", self.blob[o:o + 2])[0]
        self.slv_baseline2 = struct.unpack(">h", self.blob[o + 2:o + 4])[0]
        self.slv_npeaks1 = struct.unpack(">h", self.blob[o + 4:o + 6])[0]
        self.slv_npeaks2 = struct.unpack(">h", self.blob[o + 6:o + 8])[0]
        self.slv_pulseheight1 = struct.unpack(">h", self.blob[o + 8:o + 10])[0]
        self.slv_pulseheight2 = struct.unpack(">h", self.blob[o + 10:
                                                              o + 12])[0]
        self.slv_int1 = struct.unpack(">i", self.blob[o + 12:o + 16])[0]
        self.slv_int2 = struct.unpack(">i", self.blob[o + 16:o + 20])[0]
        self.slv_tr1 = compress(self.unpack_trace(self.blob[o + 20:o + 20 +
                                                            self.N / 2]))
        self.slv_tr2 = compress(self.unpack_trace(
            self.blob[o + 20 + self.N / 2:o + 20 + self.N]))
