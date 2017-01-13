'''
Created on 6 dec. 2016

@author: shenrot
'''
import telnetlib

class Agilent33500B(object):
    '''
    This class handle the communication with the Agilent 33500B, using a HTTP Socket
    '''

    def __init__(self, ip, port):
        '''
        Constructor
        '''
        self.telnet=telnetlib.Telnet(host=ip,port=port)
    
    def set_output(self,active,output):
        self._write(':OUTP{0} {1}'.format(output,"ON" if active else "OFF"))

    def get_output(self, output):
        return (self._read(':OUTP{0}?'.format(output))==b'1\n')
        
    def set_frequency(self,output, frequency):
        self._write(':SOUR{0}:FREQ {1}'.format(output,frequency))
        
    def get_frequency(self,output):
        return (float(self._read(':SOUR{0}:FREQ?'.format(output))))
    
    def set_pulse_mode(self,output):
        self._write('SOUR{0}:APPL:PULS'.format(output))
    
    def set_voltage_high(self,output,voltage):
        self._write('SOUR{0}:VOLT:HIGH {1:.3f}'.format(output,voltage))

    def set_voltage_low(self,output,voltage):
        self._write('SOUR{0}:VOLT:LOW {1:.3f}'.format(output,voltage))

    def get_voltage_high(self,output):
        return (float(self._read(':SOUR{0}:VOLT:HIGH?'.format(output))))

    def get_voltage_low(self,output):
        return (float(self._read(':SOUR{0}:VOLT:LOW?'.format(output))))
    
    def set_pulse_width(self,output,width):
        self._write('SOUR{0}:FUNC:PULS:WIDT {1:e}'.format(output,width))
                
    def get_pulse_width(self,output):
        return (float(self._read('SOUR{0}:FUNC:PULS:WIDT?'.format(output))))
    
    def close(self):
        self.telnet.close()
    
    def _write(self,message):
        self.telnet.write((message+";\n").encode(encoding='ascii'))
    
    def _read(self, message):
        self._write(message)
        return self.telnet.read_until(b"\n")
    