import sys
from startStop import StartStop
from hslog import log, setLogMode, MODE_BOTH


def start():
    setLogMode(MODE_BOTH)
    log('\nStarting Admin-Mode applications...')

    try:
        # start tightVNC
        log('Starting TightVNC service...')
        tightVNCHandler = StartStop()
        tightVNCHandler.serviceName = 'tvnserver'
        resTightVNC = tightVNCHandler.startService()
        if resTightVNC == 0:
            log('Status:running')
        elif resTightVNC == 1:
            log('Status:stopped')
        else:
            log('The service was not found!')
    except:
        log('An exception was generated while starting TightVNC:' +
            str(sys.exc_info()[1]))

    try:
        # start Nagios Service
        log('Starting Nagios Service')
        nagiosServHandler = StartStop()
        nagiosServHandler.serviceName = "NSClientpp"
        resNagios = nagiosServHandler.startService()
        if resNagios == 0:
            log('Status:running')
        elif resNagios == 1:
            log('Status:stopped')
        else:
            log('The service was not found!')
    except:
        log('An exception was generated while starting the Nagios Service:' +
            str(sys.exc_info()[1]))

    try:
        # start OpenVPN Service
        log('Starting OpenVPN Service')
        openVpnServHandler = StartStop()
        openVpnServHandler.serviceName = "OpenVPNService"
        resOpenVpn = openVpnServHandler.startService()
        if resOpenVpn == 0:
            log('Status:running')
        elif resOpenVpn == 1:
            log('Status:stopped')
        else:
            log('The service was not found!')
    except:
        log('An exception was generated while starting the OpenVPN Service:' +
            str(sys.exc_info()[1]))


if __name__ == "__main__":
    start()
