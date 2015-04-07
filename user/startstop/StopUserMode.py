"""Stop the HiSPARC user executables.

These applications are stopped:
HiSPARC Detector, HiSPARC Weather, MySQL, HiSPARC Monitor, HiSPARC Updater

"""

from startStop import StartStop, CMDStartStop, status
from hslog import log, setLogMode, MODE_BOTH


def stop_executable(name, exe_name, title=None):
    """Stop an executable

    :param name: common name for the program
    :param exe_name: name of the process
    :param title: specific name of the window to stop

    """
    try:
        log("Stopping %s..." % name)
        if title is None:
            handler = StartStop()
        else:
            handler = CMDStartStop()
            handler.title = title
        handler.exeName = exe_name
        result = handler.stopProcess()
        log("Status: " + status(result))
    except:
        log("An exception was generated while stopping %s!" % name)


def stop_executables():
    """Stop the user executables"""

    setLogMode(MODE_BOTH)
    log("Stopping User-Mode applications...")

    stop_executable('HiSPARC Detector', 'hisparcdaq.exe')
    stop_executable('HiSPARC Weather', 'HiSPARC Weather Station.exe')
    stop_executable('MySQL', 'mysqld.exe')
    stop_executable('HiSPARC Monitor', 'python.exe',
                    'HISPARC MONITOR: hsmonitor')
    stop_executable('HiSPARC Updater', 'python.exe',
                    'HISPARC Updater: updater')


if __name__ == "__main__":
    stop_executables()
