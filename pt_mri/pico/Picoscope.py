'''
Created on 6 dec. 2016

@author: shenrot
'''
from picoscope import ps5000a
import time
from pt_mri.pico.ChannelConfig import ChannelConfig

class Picoscope(object):
    '''
    This class handle the picoscope 5444B
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.picoscope= ps5000a.PS5000a(connect=False)
        self.channel_configs={}

    def connect(self, frequency, nb_points, channels_configs):
        self.picoscope.open()
        self.configure_sampling_frequency(frequency, nb_points)
        
        for channel_config in channels_configs:
            self.configure_channel(channel_config)
    
    def disconnect(self):
        self.picoscope.close()
    
    def get_traces(self, trigger=0, threshold=0):
        if (type(trigger)==ChannelConfig):
            self.picoscope.setSimpleTrigger(trigger.name, threshold, "Rising", 0, 0, True)

        self.picoscope.runBlock()
        while(self.picoscope.isReady() == False): time.sleep(0.01)
        
        return [self.picoscope.getDataV(channel_config.name, self.nb_points) for name,channel_config in self.channel_configs.items() if channel_config.enabled]
    
    def configure_channel(self, channel_config):
        self.channel_configs[channel_config.name]=channel_config
        if (channel_config.enabled):
            self.picoscope.setChannel(channel_config.name,
                                      coupling=channel_config.coupling,
                                      VRange=channel_config.v_range, 
                                      probeAttenuation=channel_config.probe_attenuation)
        else:
            self.picoscope.setChannel(channel_config.name,enabled=channel_config.enabled)
    
    def configure_sampling_frequency(self, frequency, nb_points):
        self.frequency_setpoint=frequency
        self.nb_points=nb_points
        res = self.picoscope.setSamplingFrequency(frequency, nb_points)
        self.frequency_effective=res[0]
        self.nb_points_effective=res[1]
        
        if (res[0]!=self.frequency_setpoint):
            print("Warning, frequency not exactly what was requested. {0}!={1}".format(self.frequency_setpoint,self.frequency_effective))
        
