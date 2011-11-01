from startStop import *
from hslog import *

path='%s:' %os.getenv("HISPARC_DRIVE")
def stop():
	setLogMode(MODE_BOTH)
	
	try:
		log('\nStopping Admin-Mode applications...')
		#stop TightVNC
		log('Stopping TightVNC service...')
		tightVNCHandler=StartStop()
		tightVNCHandler.serviceName='tvnserver'
		resTightVNC=tightVNCHandler.stopService()
		if resTightVNC==0:
			log('Status:running')
		elif resTightVNC==1:
			log('Status:stopped')
		else:
			log('The service was not found!')
	except:
		log('An exception was generated while stopping TightVNC:' +str(sys.exc_info()[1]))
		

	try:
		#stop Nagios Service
		log('Stopping Nagios Service')
		nagiosServHandler=StartStop()
		nagiosServHandler.serviceName= "NSClientpp"
		resNagios=nagiosServHandler.stopService()
		if resNagios==0:
			log('Status:running')
		elif resNagios==1:
			log('Status:stopped')
		else:
			log('The service was not found!')
	except:
		log('An exception was generated while stopping Nagios Service:' +str(sys.exc_info()[1]))
		
		
	try:
		#stop OpenVpn Service
		log('Stopping OpenVPN Service')
		openVpnServHandler=StartStop()
		openVpnServHandler.serviceName= "OpenVPNService"
		resOpenVpn=openVpnServHandler.stopService()
		if resOpenVpn==0:
			log('Status:running')
		elif resOpenVpn==1:
			log('Status:stopped')
		else:
			log('The service was not found!')
	except:
		log('An exception was generated while stopping OpenVPN Service:' +str(sys.exc_info()[1]))
	
stop()