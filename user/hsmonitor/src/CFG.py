""" 
	Process HiSPARC messages from a buffer.
    This module processes the CFG event message 
"""

__author__="thevinh"
__date__ ="$17-sep-2009"

import datetime
from HiSparc2Event import HiSparc2Event

class CFG(HiSparc2Event):	
	def __init__(self, message):
		""" Initialization
			Proceed to unpack the message.
		"""		
		# invoke constructor of parent class
		HiSparc2Event.__init__(self, message)	
	
	#--------------------------End of __init__--------------------------#	
	
	def unpackMessage(self):
		"""	Unpack a configuration message
			This routine unpacks the configuration messages which are written
			to the buffer every time the LabVIEW DAQ software enters DAQ mode.
		"""
		# Initialize sequential reading mode
		self.unpackSeqMessage()

		self.version, self.database_id, \
		gps_second, gps_minute, gps_hour, gps_day, gps_month, gps_year, \
		self.cfg_gps_longitude, self.cfg_gps_latitude, \
		self.cfg_gps_altitude = self.unpackSeqMessage('>2B5BH3d')
		#self.cfg_gps_altitude = self.unpackSeqMessage('>BBBBBBBHddd')

		self.datetime = datetime.datetime(gps_year, gps_month, gps_day,
										  gps_hour, gps_minute, gps_second)
		self.nanoseconds = 0

		self.cfg_mas_version, = self.unpackSeqMessage('LVstring')
		self.cfg_slv_version, = self.unpackSeqMessage('LVstring')

		self.cfg_trig_low_signals, self.cfg_trig_high_signals, \
		self.cfg_trig_external, self.cfg_trig_and_or, \
		self.cfg_precoinctime, self.cfg_coinctime, \
		self.cfg_postcoinctime, self.cfg_detnum = \
		self.unpackSeqMessage('>3LB3dH')
		#self.unpackSeqMessage('>LLLBdddH')

		self.cfg_password, = self.unpackSeqMessage('LVstring')

		self.cfg_spare_bytes, self.cfg_use_filter, \
		self.cfg_use_filter_threshold, self.cfg_reduce_data = \
		self.unpackSeqMessage('>4B')
		#self.unpackSeqMessage('>BBBB')

		self.cfg_buffer, = self.unpackSeqMessage('LVstring')

		self.cfg_startmode, self.cfg_delay_screen, self.cfg_delay_check, \
		self.cfg_delay_error = self.unpackSeqMessage('>B3d')
		#self.cfg_delay_error = self.unpackSeqMessage('>Bddd')

		self.cfg_mas_ch1_thres_low, self.cfg_mas_ch1_thres_high, \
		self.cfg_mas_ch2_thres_low, self.cfg_mas_ch2_thres_high, \
		self.cfg_mas_ch1_inttime, self.cfg_mas_ch2_inttime, \
		self.cfg_mas_ch1_voltage, self.cfg_mas_ch2_voltage, \
		self.cfg_mas_ch1_current, self.cfg_mas_ch2_current, \
		self.cfg_mas_comp_thres_low, self.cfg_mas_comp_thres_high, \
		self.cfg_mas_max_voltage, self.cfg_mas_reset, \
		self.cfg_mas_ch1_gain_pos, self.cfg_mas_ch1_gain_neg, \
		self.cfg_mas_ch2_gain_pos, self.cfg_mas_ch2_gain_neg, \
		self.cfg_mas_ch1_offset_pos, self.cfg_mas_ch1_offset_neg, \
		self.cfg_mas_ch2_offset_pos, self.cfg_mas_ch2_offset_neg, \
		self.cfg_mas_internal_voltage, self.cfg_mas_common_offset, \
		self.cfg_mas_ch1_adc_gain, self.cfg_mas_ch1_adc_offset, \
		self.cfg_mas_ch2_adc_gain, self.cfg_mas_ch2_adc_offset, \
		self.cfg_mas_ch1_comp_gain, self.cfg_mas_ch1_comp_offset, \
		self.cfg_mas_ch2_comp_gain, self.cfg_mas_ch2_comp_offset = \
		self.unpackSeqMessage('>13dB8B2B8d')

		self.cfg_slv_ch1_thres_low, self.cfg_slv_ch1_thres_high, \
		self.cfg_slv_ch2_thres_low, self.cfg_slv_ch2_thres_high, \
		self.cfg_slv_ch1_inttime, self.cfg_slv_ch2_inttime, \
		self.cfg_slv_ch1_voltage, self.cfg_slv_ch2_voltage, \
		self.cfg_slv_ch1_current, self.cfg_slv_ch2_current, \
		self.cfg_slv_comp_thres_low, self.cfg_slv_comp_thres_high, \
		self.cfg_slv_max_voltage, self.cfg_slv_reset, \
		self.cfg_slv_ch1_gain_pos, self.cfg_slv_ch1_gain_neg, \
		self.cfg_slv_ch2_gain_pos, self.cfg_slv_ch2_gain_neg, \
		self.cfg_slv_ch1_offset_pos, self.cfg_slv_ch1_offset_neg, \
		self.cfg_slv_ch2_offset_pos, self.cfg_slv_ch2_offset_neg, \
		self.cfg_slv_internal_voltage, self.cfg_slv_common_offset, \
		self.cfg_slv_ch1_adc_gain, self.cfg_slv_ch1_adc_offset, \
		self.cfg_slv_ch2_adc_gain, self.cfg_slv_ch2_adc_offset, \
		self.cfg_slv_ch1_comp_gain, self.cfg_slv_ch1_comp_offset, \
		self.cfg_slv_ch2_comp_gain, self.cfg_slv_ch2_comp_offset = \
		self.unpackSeqMessage('>13dB8B2B8d')
		
	#--------------------------End of unpackMessage--------------------------#	