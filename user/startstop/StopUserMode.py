"""Stop the HiSPARC user executables.

These applications are stopped:
LabVIEW Detector, LabVIEW Weather, MySQL, HiSPARC Monitor, HiSPARC Updater

"""
from startStop import StartStop, CMDStartStop, status
from hslog import log, setLogMode, MODE_BOTH


def stop():
    setLogMode(MODE_BOTH)
    log("\nStopping User-Mode applications...")

    try:
        # stop LabVIEW detector
        log("Stopping LabVIEW detector...")
        handler = StartStop()
        handler.exeName = "hisparcdaq.exe"

        res = handler.stopProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while stopping LabVIEW detector!")

    try:
        # stop LabVIEW weather
        log("Stopping LabVIEW weather...")
        handler = StartStop()
        handler.exeName = "HiSPARC Weather Station.exe"

        res = handler.stopProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while stopping LabVIEW weather!")

    try:
        # stop MySQL
        log("Stopping MySQL...")
        handler = StartStop()
        handler.exeName = "mysqld.exe"

        res = handler.stopProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while stopping MySQL!")

    try:
        # stop HSMonitor
        log("Stopping HSMonitor...")
        handler = CMDStartStop()
        handler.exeName = "python.exe"
        handler.title = "HISPARC MONITOR: hsmonitor"

        res = handler.stopProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while stopping HSMonitor!")

    try:
        # stop Updater
        log("Stopping Updater...")
        handler = CMDStartStop()
        handler.exeName = "python.exe"
        handler.title = "HISPARC Updater: updater"

        res = handler.stopProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while stopping the Updater!")


if __name__ == "__main__":
    stop()
