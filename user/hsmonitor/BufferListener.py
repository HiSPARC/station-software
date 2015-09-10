"""The BufferListener periodically polls the MySQL-buffer database.

When events are available they are immediately fetched from the database and
passed on to the Interpreter. The Interpreter processes the binary messages and
creates Events from it. The Events are passed on to the StorageManager.

"""

from time import sleep, time
import threading
import logging

from MySQLdb import connect, OperationalError

from UserExceptions import ThreadCrashError

logger = logging.getLogger('hsmonitor.bufferlistener')


class BufferListener(threading.Thread):

    def __init__(self, config, interpreter):
        super(BufferListener, self).__init__(name='BufferListener')

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

        if len(self.crashes) > 3 and time() - self.crashes[-3] < 60.:
            raise ThreadCrashError('Thread has crashed three times in '
                                   'less than a minute')
        else:
            super(BufferListener, self).__init__()
            self.crashes.append(time())

    # This function is what the thread actually runs. The required name is
    # run(). The threading.Thread.start() calls threading.Thread.run(), which
    # is always overridden.
    def run(self):
        """Main loop that continuously looks for new messages in the buffer.

        New messages are parsed by the interpreter and sent to the storage.

        """
        self.interpreter.openStorage()
        logger.debug('Thread started')
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
            sleep(int(self.config['poll_interval']))
        logging.warning('Thread stopped!')

    def getDBConnection(self, dbdict):
        """Get the connection to Buffer database"""
        try:
            conn = connect(host=dbdict['host'], user=dbdict['user'],
                           passwd=dbdict['password'], db=dbdict['db'])
        except OperationalError, (msg_id, msg):
            logger.error('%d: %s' % (msg_id, msg))
            conn = None
        else:
            logger.debug('Connected to the buffer database!')
        return conn

    def getMessageCount(self):
        """Get the number of event messages"""
        cursor = self.conn.cursor()
        sql = "SELECT COUNT(*) FROM message"
        logger.debug('Executing SQL: %s' % sql)
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        return count

    def getBufferMessages(self):
        """Get messages from Buffer database"""
        cursor = self.conn.cursor()
        sql = ("SELECT message_type_id, message, message_id FROM message "
               "ORDER BY message_id DESC LIMIT %d" %
               int(self.config['poll_limit']))
        logger.debug('Getting messages from buffer database.')
        cursor.execute(sql)
        messages = cursor.fetchall()
        logger.debug('Selected %d messages.' % len(messages))
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

        logger.debug('Clear %d events from buffer...' % numcleared)
        self.conn.commit()
        return len(message_ids)
