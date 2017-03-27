'''
Created on Feb 2, 2016

@author: fidji
'''
from holdie.holder.BaseHolder import BaseHolder
from holdie.database.Config import Config

class HolderGroup(BaseHolder):
    '''
    classdocs
    '''
    matchList = dict()

    def __init__(self):
        '''
        Constructor
        '''
        super(HolderGroup,self).__init__()
    
    # Add a string of matches to the match list
    def addToMatchList(self, strMatch):

        # split the line and strip it using list comprehension
        strMatches = [strSingle.strip() for strSingle in strMatch.split(",")]

        # Now resolve each to a GID
        # TODO exception if the group does not exist
        for strGroup in strMatches:
            import grp
            
            #print("GID " + str(grp.getgrnam(strGroup).gr_gid) + " " + strGroup)
            self.matchList[grp.getgrnam(strGroup).gr_gid] = strGroup
            
        if (Config().isDebugEnabled() == True): print(self.matchList)
    
    def getFirstHolderPID(self):
        import os
        
        matchPID = 0
        matchGrp = 0
        
        # Get list of pids
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        
        # process gathered pids
        for pid in pids:
            try:
                statinfo = os.stat(os.path.join('/proc', pid))
                
                for match in self.matchList:
                    if (statinfo.st_gid == match):
                        matchPID = pid
                        matchGrp = match
                
            except IOError: # proc has already terminated
                continue

        if (0 != matchPID):
            msg = "Process " + matchPID + " is owned by group \"" + self.matchList[matchGrp] + "\" (" + str(matchGrp) + ")"
            
            if (Config().isDebugEnabled() == True):
                msg += " command line is: " + open(os.path.join('/proc', matchPID, 'cmdline'), 'rb').read().decode("utf-8")
                
            print(msg)
        
        return matchPID
            