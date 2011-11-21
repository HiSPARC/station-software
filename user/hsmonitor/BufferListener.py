"""The BufferListener periodically polls the MySQL-buffer database.

When events are available they are immediately fetched from the database and
passed on to the Interpreter. The Interpreter processes the binary messages and
creates Events from it. The Events are passed on to the StorageManager.

"""

__author__="thevinh"
__date__ ="$14-sep-2009"

import sys
import time
import threading
import _mysql
from MySQLdb import connect, OperationalError
import hslog
from Interpreter import Interpreter
from UserExceptions import ThreadCrashError

class BufferListener(threading.Thread):
    # the instantiation operation
    def __init__(self, config, interpreter):
        # invoke constructor of parent class (threading)
        threading.Thread.__init__(self)
        self.interpreter = interpreter
        self.stop_event = threading.Event()

        # init variables here if needed
        self.config = config

        # make a connection to buffer DB
        self.conn = self.getDBConnection(self.config)

    def stop(self):
        self.stop_event.set()

    crashes = []

    def init_restart(self):
        """Support for restarting crashed threads"""

        if len(self.crashes) > 3 and time.time() - self.crashes[-3] < 60.:
            raise ThreadCrashError('Thread has crashed three times in '
                                   'less than a minute')
        else:
            super(BufferListener, self).__init__()
            self.crashes.append(time.time())

    # This function is what the thread actually runs. The required name is
    # run(). The threading.Thread.start() calls threading.Thread.run(), which
    # is always overridden.
    def run(self):
        self.interpreter.openStorage()
        hslog.log("BufferListener: Thread started")
        while not self.stop_event.isSet():
            # DF: Unfortunately, not reconnecting results in stale connections
            self.conn = self.getDBConnection(self.config)
            # select new events from buffer and pass them to the Interpreter
            # get unprocessed events
            messages = self.getBufferMessages()
            if (len(messages) > 0):
                # parse the list of events
                event_ids = self.interpreter.parseMessages(messages)
                # clear the parsed messages
                if int(self.config['keep_buffer_data']) != 1:
                    self.clearBufferMessages(event_ids)
            # wait for a polling interval
            time.sleep(int(self.config['poll_interval']))
        hslog.log("BufferListener: Thread stopped!")

    def getDBConnection(self, dbdict):
        """Get the connection to Buffer database"""
        try:
            conn = connect(host = dbdict['host'], user = dbdict['user'],
                           passwd = dbdict['password'], db = dbdict['db'])
        except OperationalError, (msg_id, msg):
            hslog.log('BufferListener: Error: %d: %s' % (msg_id, msg))
            conn = None
        else:
            hslog.log("BufferListener: Connected to the buffer database!")

        return conn

    def getMessageCount(self):
        """Get the number of event messages"""
        cursor = self.conn.cursor()
        sql = "SELECT COUNT(*) FROM message"
        hslog.log("BufferListener: Executing SQL: %s" % sql)
        cursor.execute(sql)
        hslog.log("BufferListener: Fetching SQL results...")
        count = cursor.fetchone()[0]
        hslog.log("BufferListener: Done.")
        return count

    def getBufferMessages(self):
        """Get messages from Buffer database"""
        cursor = self.conn.cursor()
        sql = "SELECT message_type_id, message, message_id FROM message ORDER "\
              "BY message_id DESC LIMIT %d" % int(self.config['poll_limit'])
        hslog.log("BufferListener: Executing SQL: %s" % sql)
        cursor.execute(sql)
        hslog.log("BufferListener: Fetching SQL results...")
        messages = cursor.fetchall()
        hslog.log("BufferListener: Selected %d messages." % len(messages))
        cursor.close()
        return messages

    def clearBufferMessages(self, message_ids):
        """Clear the parsed messages"""
        if len(message_ids) < 1:
            return 0
        cursor = self.conn.cursor()
        # if there is only one event in the list -> change the SQL syntax
        if len(message_ids) == 1:
            sql = "DELETE FROM message WHERE message_id = %s"
            numcleared = cursor.execute(sql, (message_ids))
        else:
            sql = "DELETE FROM message WHERE message_id IN %s"
            numcleared = cursor.execute(sql, (message_ids,))

        hslog.log("BufferListener: Clear %d events from buffer..." % numcleared)
        self.conn.commit()
        hslog.log("BufferListener: Done.")
        return len(message_ids)
