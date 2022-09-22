# Go through source project test case - destination project test case pairs and copy desciptions
# pair list is provided (constructed from CopyTestJiraData log file(s))
# mika.nokka1@gmail.com 15.9.2021



#from __future__ import unicode_literals

import sys, logging
import argparse
#import re
from collections import defaultdict
from Authorization import Authenticate  # no need to use as external command
from Authorization import DoJIRAStuff

import glob
import re
import os
import time
import unidecode
from jira import JIRA, JIRAError
from collections import defaultdict
from time import sleep
import keyboard
import math


__version__ = u"0.1"



logging.basicConfig(level=logging.DEBUG) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
  
    #hardcoded Jira source (of the epics) and target project (place where epics are copied) IDs
    TARGETPROJECT="GRA12"  
    SOURCEJIRAPROJECT="GRAP"
  
    logging.debug (u"--Created date field copier starting --") 
    start = time.perf_counter()
 
    parser = argparse.ArgumentParser(description=" Copy test case normal jira data to target project (and matching test case)",
    
    
    epilog="""
    
    EXAMPLE:
    
    CopyTestJiraData.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ """

    
    )
    
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA password>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-r', help='<DryRun - do nothing but emulate. On by default>',metavar="on|off",default="on")
 

    args = parser.parse_args()
       
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''

    if (args.r=="on"):
        SKIP=1
    else:
        SKIP=0    

    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER==''):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    #print ("FORCE EXIT..!!")
    #sys.exit(5)
   
    if (SKIP==1):
        print("DRY RUN MODE ON")
    else:
        print ("REAL OPERATION MODE. DRY RUN MODE OFF") 
   
   

    GetSourceTests(SOURCEJIRAPROJECT,jira,SKIP,TARGETPROJECT)


    end = time.perf_counter()
    totaltime=end-start
    #seconds=totaltime.total_seconds()
    print ("Operation time taken:{0} seconds".format(totaltime))



#################################################
# Get source project Zephyr Squa Test cases, hardcoded JQL
#
# Check every Test case if there exists Epic (requirements) linked to it
#

def GetSourceTests(SOURCEJIRAPROJECT,jira,SKIP,TARGETPROJECT):
    
    COPIEDCOUNTER=0
    COUNTER=0

    #SOURCE="GRAP-10244"
    #TARGET="GRA12-7597"
    
    #open text file defining source test - target test pairs
    pairsfile=open("1-7pairs.txt")
    
    for line in pairsfile:
        print ("Operation number:{0}".format(COUNTER))
        print ("Read pair line:{0}".format(line))
        REGEXPR=r"(.*)(:)(.*)(-->)(.*)"   # Target-Source pair: GRAP-10244 --> GRA12-7597
        x = re.search(str(REGEXPR), str(line))  
        g2=x.group(3)
        g4=x.group(5)     
        #print ("group(3), group(5):{0} , {1}".format(g2,g4))
    
        g2=g2.replace(" ","")
        g4=g4.replace(" ","")       
        SOURCEISSUE=jira.issue(g2)  
        TARGETISSUE=jira.issue(g4)      
    
        print ("Source issue:{0}".format(SOURCEISSUE)) 
        print ("target issue:{0}".format(TARGETISSUE)) 
    
        SOURCEDESCRIPTION=SOURCEISSUE.fields.description
        TARGETDESCRIPTION=TARGETISSUE.fields.description
    
    
        if (TARGETDESCRIPTION!=None):
                print("Target description:")
                FILTEREDT=TARGETDESCRIPTION.encode("utf-8")
                print("{0}".format(FILTEREDT))           
        else:
            print("No target description")
    
        if (SOURCEDESCRIPTION!=None):
                print("Source description:")
                FILTEREDS=SOURCEDESCRIPTION.encode("utf-8")
                print("{0}".format(FILTEREDS))
                print("")
                print ("Copy operation defined:{0} --> {1}".format(SOURCEISSUE,TARGETISSUE))
                if (SKIP==1):
                    print("DRY RUN MODE ON. NOT DOING ANYTHING")
                else:
                    print ("REAL OPERATION MODE. DRY RUN MODE OFF. Doing copy operation")   
                    CopyData (SOURCEISSUE,TARGETISSUE,TARGETDESCRIPTION,SOURCEDESCRIPTION,jira,COPIEDCOUNTER)
        else:
            print("No source description. No operations done")            
                
        COUNTER=COUNTER+1
        print ("--------------------------------------------------------------------------------------")
    
    print ("****************************************************************************************************************")

                
                
    print ("xxxxxxxxxx END OF ISSUE HANDLING xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print ("")
            
            

 
############################################################################################
# copy source project test case normal Jira data to target project found matching test case    
# TBD: data in dictionary , this is POC    
        
def CopyData (SOURCEISSUE,TARGETISSUE,TARGETDESCRIPTION,SOURCEDESCRIPTION,jira,COPIEDCOUNTER):     
        print("")   
        print ("Copy operation number:{0}".format(COPIEDCOUNTER))
        print ("Data copy operations {0} --> {1}".format(SOURCEISSUE,TARGETISSUE))
        print ("..............................................")
        
        if (SOURCEDESCRIPTION != None):
            print ("SOURCEDESCRIPTION available. Doing copy operation")
            TARGETISSUE.update(notify=False, description=SOURCEDESCRIPTION)
            time.sleep(0.3) 
    
    
            COPIEDCOUNTER=COPIEDCOUNTER+1
      
            
            

#########################################################################

if __name__ == "__main__":
    main(sys.argv[1:]) 
 