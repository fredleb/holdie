'''
Created on Jan 27, 2016

@author: fidji
'''

import configparser # for the ini file

class IniFile(object):
    '''
    Base class for ini file manipulation
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
        '''Object wide attributes'''
        self.inifile = configparser.ConfigParser()
        
    def dump(self):
        for section in self.inifile.sections():
            print(section)
            for option in self.inifile.options(section):
                print (" ", option, "=", self.inifile.get(section, option))

