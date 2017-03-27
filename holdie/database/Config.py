'''
Created on Jan 26, 2016

@author: fidji
'''
from holdie.database.IniFile import IniFile
from holdie.meta.Singleton import Singleton


class Config(IniFile, metaclass = Singleton):
    '''
    classdocs
    '''

    # Constants
    # Ini file structure
    STR__HOLDIE_INI__TIMING = "timing"
    STR__HOLDIE_INI__TIMING__STARTUP_GRACE = "startup_grace"
    STR__HOLDIE_INI__TIMING__NORMAL_LOOP = "normal_loop"
    STR__HOLDIE_INI__TIMING__SHUTDOWN_GRACE = "shutdown_grace"
    
    STR__HOLDIE_INI__HOLDER = "holder"
    STR__HOLDIE_INI__HOLDER__GROUP = "group"
    STR__HOLDIE_INI__HOLDER__COOKIE_PATH = "cookie_path"

    # Ini file structure
    STR__HOLDIE_INI__DEBUG = "debug"
    STR__HOLDIE_INI__DEBUG__ENABLE = "enable"
    STR__HOLDIE_INI__DEBUG__SYSTEM_UPTIME = "system_uptime"
    STR__HOLDIE_INI__DEBUG__SYSTEM_GMTIME = "system_gmtime"
    STR__HOLDIE_INI__DEBUG__SHUTDOWN_ENABLE = "shutdown"

    
    def __init__(self):
        '''
        Constructor
        '''
        super(Config,self).__init__()

        # TODO magic number
        retval = self.inifile.read("/home/users/fidji/Documents/LiClipse Workspace/holdie/etc/holdie.ini")

        if not retval:
            print("Could not read ini file")
            exit(-1)

    def getStartupGrace(self):
        return int(self.inifile.get(self.STR__HOLDIE_INI__TIMING, self.STR__HOLDIE_INI__TIMING__STARTUP_GRACE))

    def getNormalLoop(self):
        return int(self.inifile.get(self.STR__HOLDIE_INI__TIMING, self.STR__HOLDIE_INI__TIMING__NORMAL_LOOP))
    
    def getShutdownGrace(self):
        return int(self.inifile.get(self.STR__HOLDIE_INI__TIMING, self.STR__HOLDIE_INI__TIMING__SHUTDOWN_GRACE))
    
    def getPath2Cookie(self):
        return self.inifile.get(self.STR__HOLDIE_INI__HOLDER, self.STR__HOLDIE_INI__HOLDER__COOKIE_PATH)
    
    def isDebugEnabled(self):
        try:
            return self.inifile.getboolean(self.STR__HOLDIE_INI__DEBUG, self.STR__HOLDIE_INI__DEBUG__ENABLE)
        except:
            return False
    
    def getDebugSystemUptime(self):
        return int(self.inifile.get(self.STR__HOLDIE_INI__DEBUG, self.STR__HOLDIE_INI__DEBUG__SYSTEM_UPTIME))
        
    def getDebugSystemGMTimeStr(self):
        return self.inifile.get(self.STR__HOLDIE_INI__DEBUG, self.STR__HOLDIE_INI__DEBUG__SYSTEM_GMTIME)

    def isShutdownEnabled(self):
        # By default the shutdown is enabled
        bShutdownEnabled = True
        
        if (True == self.isDebugEnabled()):
            try:
                bShutdownEnabled = self.inifile.getboolean(self.STR__HOLDIE_INI__DEBUG, self.STR__HOLDIE_INI__DEBUG__SHUTDOWN_ENABLE)
            except:
                pass
            
        return bShutdownEnabled

    def getHolderGroup(self):
        return self.inifile.get(self.STR__HOLDIE_INI__HOLDER, self.STR__HOLDIE_INI__HOLDER__GROUP)
            
