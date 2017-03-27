'''
Created on Jan 27, 2016

@author: fidji
'''

from holdie.database.IniFile import IniFile
from holdie.meta.Singleton import Singleton
from holdie.database.Config import Config
import time #from time import gmtime, strftime


class Cookie(IniFile, metaclass = Singleton):
    '''
    classdocs
    '''
    
    # Constants
    # Ini file structure
    STR__HOLDIE_COOKIE_INI__COOKIE = "cookie"
    STR__HOLDIE_COOKIE_INI__COOKIE__LAST_CHECK = "last_check"
    STR__HOLDIE_COOKIE_INI__COOKIE__LAST_UPTIME = "last_uptime"
    STR__HOLDIE_COOKIE_INI__COOKIE__LAST_HOLD = "last_hold"
    
    STR__HOLDIE_COOKIE__TIME_FORMAT = "%Y%m%d-%H%M%S"
    
    def __init__(self):
        '''
        Constructor
        '''
        super(Cookie,self).__init__()
        
        # Load the cookie if it exists
        # TODO magic number
        retval = self.inifile.read(Config().getPath2Cookie())

        if not retval:
            # No file, not a problem, just create one
            
            # Create the necessary section(s)
            self.inifile[self.STR__HOLDIE_COOKIE_INI__COOKIE] = {}

            # Update and commit
            self.refreshHoldTime()
            self.refresh()            
            self.commit()
        else:
            self.validate()
        
    # Get the current uptime in minutes from the system
    def getCurrentSystemUptime(self):
        
        uptime_minutes = -1
        
        if (True == Config().isDebugEnabled()):
            try:
                uptime_minutes = int(Config().getDebugSystemUptime())
                print("DEBUG: Assuming system uptime : " + str(uptime_minutes))
            except:
                pass
        
        if (-1 == uptime_minutes):
            with open('/proc/uptime', 'r') as f:
                uptime_minutes = int(round(float(f.readline().split()[0]) / 60))

        return uptime_minutes
    
    # Get the current GMTime from the system
    def getCurrentSystemGMTime(self):
        
        system_time = -1
        
        if (True == Config().isDebugEnabled()):
            try:
                system_time = time.strptime(Config().getDebugSystemGMTimeStr(), self.STR__HOLDIE_COOKIE__TIME_FORMAT)
                print("DEBUG: Assuming system time : " + time.strftime(self.STR__HOLDIE_COOKIE__TIME_FORMAT, system_time) + " (real is : " + time.strftime(self.STR__HOLDIE_COOKIE__TIME_FORMAT, time.gmtime()) + ")")
            except:
                pass
        
        if (-1 == system_time):
            system_time = time.gmtime()

        return system_time
    
    # Write to disk    
    def commit(self):
        with open(Config().getPath2Cookie(), 'w') as cookiefile:
            self.inifile.write(cookiefile)
        
    # Update the timestamps
    def refresh(self):
        self.inifile.set(self.STR__HOLDIE_COOKIE_INI__COOKIE, self.STR__HOLDIE_COOKIE_INI__COOKIE__LAST_UPTIME, str(self.getCurrentSystemUptime()))
        self.inifile.set(self.STR__HOLDIE_COOKIE_INI__COOKIE, self.STR__HOLDIE_COOKIE_INI__COOKIE__LAST_CHECK, time.strftime(self.STR__HOLDIE_COOKIE__TIME_FORMAT, self.getCurrentSystemGMTime()))

    # Update the hold time
    def refreshHoldTime(self):
        self.inifile.set(self.STR__HOLDIE_COOKIE_INI__COOKIE, self.STR__HOLDIE_COOKIE_INI__COOKIE__LAST_HOLD, str(self.getCurrentSystemUptime()))

    # Get the last uptime from the cookie
    def getLastCheckUptime(self):
        return int(self.inifile.get(self.STR__HOLDIE_COOKIE_INI__COOKIE, self.STR__HOLDIE_COOKIE_INI__COOKIE__LAST_UPTIME))

    # Get the last uptime from the cookie
    def getLastHoldTime(self):
        return int(self.inifile.get(self.STR__HOLDIE_COOKIE_INI__COOKIE, self.STR__HOLDIE_COOKIE_INI__COOKIE__LAST_HOLD))
    
    # Get the last check time from the cookie
    def getLastCheckGMTime(self):
        return time.strptime(self.inifile.get(self.STR__HOLDIE_COOKIE_INI__COOKIE, self.STR__HOLDIE_COOKIE_INI__COOKIE__LAST_CHECK), self.STR__HOLDIE_COOKIE__TIME_FORMAT)
    
    # Checks and eventually dismisses the cookie if it is not valid
    def validate(self):
        
        stale = False
        
        # If the uptime or the hold time in the cookie is bigger than the system one, then the system has rebooted
        if ((self.getLastCheckUptime() > self.getCurrentSystemUptime()) | ((self.getLastHoldTime() > self.getCurrentSystemUptime()))):
            # The system has rebooted, refresh the cookie
            # TODO make an info
            print("The system seems to have rebooted, the cookie is stale.")
            stale = True
        elif (self.getCurrentSystemGMTime() < self.getLastCheckGMTime()):
            # If the time in the cookie is later than the current time, something has
            # happened with the clock and we can't trust the cookie
            # TODO make a warning
            print("The system seems to have gone back in time. I'll consider the cookie stale.")
            stale = True

        if (True == stale):
            self.refreshHoldTime()
            self.refresh()
