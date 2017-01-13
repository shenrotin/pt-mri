'''
Created on 6 dec. 2016

@author: shenrot
'''

class ChannelConfig(object):
    '''
    This class is used to store the configuration of a channel
    '''

    def __init__(self, name, v_range=5.0, probe_attenuation=1.0, coupling="DC", enabled=True):
        '''
        Constructor
        '''
        self.name=name
        self.v_range=v_range
        self.probe_attenuation=probe_attenuation
        self.enabled=enabled
        self.coupling=coupling