import wmi
import MySQLdb
from socket import gethostbyname
import ConfigParser

CONFIG_INI1 = "../../user/hsmonitor/data/config.ini"
CONFIG_INI2 = "../../user/hsmonitor/data/config-password.ini"

OK = 0
WARNING = 1
CRITICAL = 2

localhost = gethostbyname("127.0.0.1")


def check_bufferdb(warn=None, crit=None):
    if warn:
        wmin, wmax = warn
    if crit:
        cmin, cmax = crit

    config = ConfigParser.ConfigParser()

    try:
        config.read([CONFIG_INI1, CONFIG_INI2])
        host = config.get('BufferDB', 'Host')
        user = config.get('BufferDB', 'Username')
        pwd = config.get('BufferDB', 'Password')
        db = config.get('BufferDB', 'DB')
    except:
        print 'Could not read config.ini file!'
        return CRITICAL

    try:
        dbcon = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db)
    except MySQLdb.OperationalError, (errid, errmsg):
        print '%s (Error %d)' % (errmsg, errid)
        return CRITICAL

    cursor = dbcon.cursor()
    cursor.execute("SHOW TABLE STATUS LIKE 'message'")
    idx = [x[0] for x in cursor.description].index('Rows')
    num_events = cursor.fetchone()[idx]
    dbcon.close()
    print 'Buffer DB contains %d events' % num_events

    if crit:
        if not cmin <= num_events <= cmax:
            return CRITICAL
    if warn:
        if not wmin <= num_events <= wmax:
            return WARNING
    return OK


def check_lvusage(warn, crit):
    """
    Check the memory using Labview and also immediately give the cpu time.

    """
    w = wmi.WMI()
    wmin, wmax = warn
    cmin, cmax = crit
    LABVIEW_CAPTIONS = ['HiSPARC DAQ.exe', 'HISPAR~1.EXE']

    for p in w.Win32_Process():
        if p.Name in LABVIEW_CAPTIONS:
            mem = float(p.WorkingSetSize) / (1024. * 1024.)
            cpu = (float(p.UserModeTime) + float(p.KernelModeTime)) / 1e7

            print 'Memory usage: %.1f Mb' % mem
            print 'CPU time: %.2fs' % cpu

            if not cmin < mem < cmax:
                return CRITICAL
            elif not wmin < mem < wmax:
                return WARNING
            else:
                return OK

    # The process is not running.
    print 'Labview is not running'
    return CRITICAL
