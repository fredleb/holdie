from holdie.database.Config import Config
from holdie.database.Cookie import Cookie

import time
import subprocess
from subprocess import CalledProcessError
from _csv import Error

def main():
    if (True == Config().isDebugEnabled()):
        print("++++++++++++++++++++++++ START ++++++++++++++++++++++++")
        print("-------- config --------")
        Config().dump()
        print("-------- cookie --------")
        Cookie().dump()
        print("++++++++++++++++++++++++ END START ++++++++++++++++++++++++")
    
    if (True == Config().isDebugEnabled()):
        print("Cookie().getCurrentSystemUptime() = " + str(Cookie().getCurrentSystemUptime()))
        print("Cookie().getLastCheckUptime() = " + str(Cookie().getLastCheckUptime()))
        print("Cookie().getLastHoldTime() = " + str(Cookie().getLastHoldTime()))
        print("last check delta: " + str(Cookie().getCurrentSystemUptime() - Cookie().getLastCheckUptime()))
        print("last check time: " + str(Cookie().getLastCheckGMTime()))
        print("delta hold min: " + str(Cookie().getCurrentSystemUptime() - Cookie().getLastHoldTime()))
    
    
    # State machine
    sysUpTime = Cookie().getCurrentSystemUptime()
    
    if (sysUpTime <= Config().getStartupGrace()):
        if (Config().isDebugEnabled() == True):
            print("Startup grace time is not over yet.")
    else:
        if (Config().isDebugEnabled() == True):
            print("Startup grace time is over.")
        
        # By default we check to find a holder every time we run
        bCheckForHolder = True
        
        # By default don't initiate shutdown
        bShutDown = False
    
        # let's check if last hold time is further away than a loop time
        deltaHold = Cookie().getCurrentSystemUptime() - Cookie().getLastHoldTime()
        
        if (deltaHold > Config().getShutdownGrace()):
            if (Config().isDebugEnabled() == True):
                print("deltaHold is longer than shutdown grace, allow shutdown.")
            # Shut down can be initiated
            bShutDown = True
            
        elif (deltaHold % Config().getNormalLoop()):
            # Last time we found a holder was less than normal_loop minutes ago
            if (True == Config().isDebugEnabled()):
                print("Not checking. deltaHold = " + str(deltaHold))
            
            bCheckForHolder = False
            
        if (True == bCheckForHolder):
            from holdie.holder.HolderGroup import HolderGroup
            
            # Let's try to find a group holding a process
            holder = HolderGroup()
            
            holder.addToMatchList(Config().getHolderGroup())
            
            if (0 == holder.getFirstHolderPID()):
                print("No holder found for " + str(deltaHold) + " minutes.")
            else:
                # Holder was found so we update the hold time in the cookie
                Cookie().refreshHoldTime()
                # And we prevent shutdown
                bShutDown = False
            
            Cookie().refresh()
            Cookie().commit()
    
        if (True == bShutDown):
            # Proceed to shut down
            if (True == Config().isShutdownEnabled()):
                print("!!! No holder found after shutdown grace period, the system will shutdown !!!")
                
                output = ""
                try:
                    output = subprocess.check_output("shutdown", stderr=subprocess.STDOUT)
                except CalledProcessError as Err:
                    print("!!! ERROR \"" + Err.output.decode(encoding='UTF-8').strip() + "\" while executing shutdown command !!!")
            else:
                print("!!! No holder found after shutdown grace period, the system would shut down if shutdown was not disabled in config file... !!!")
        
    
    if (True == Config().isDebugEnabled()):
        print("++++++++++++++++++++++++ STOP ++++++++++++++++++++++++")
        print("-------- cookie --------")
        Cookie().dump()
        print("++++++++++++++++++++++++ END STOP ++++++++++++++++++++++++")

