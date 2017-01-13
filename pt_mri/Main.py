'''
Created on 6 dec. 2016

@author: shenrot
'''
from pt_mri.pico.Picoscope import Picoscope
from pt_mri.pico.ChannelConfig import ChannelConfig


if __name__ == '__main__':
    channels_configs=[]
    channels_configs.append(ChannelConfig("A"))
    channels_configs.append(ChannelConfig("B"))
    channels_configs.append(ChannelConfig("C"))
    channels_configs.append(ChannelConfig("D"))
    
    pico=Picoscope()
    pico.connect(10000, 20, channels_configs)
    traces=pico.get_traces(channels_configs[0], 1.5)
    
    pico.disconnect()