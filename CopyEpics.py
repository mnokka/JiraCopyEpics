# Copy given Jira project Epics to another Jira project (summary + description)  
# 
# mika.nokka1@gmail.com 1.9.2021





# Used to get given Jira project issue data 
#
# 17.8.2020 mika.nokka1@gmail.com 
# 
# NOTES:
# 1) For this POC removed .netrc authetication, using pure arguments
#
# Traps worng JQL query and possible corrupted attachment case (not downloading corrupted fileS) 
# 
#
# Python V2
#
#from __future__ import unicode_literals

#import openpyxl 
#!/usr/bin/python3

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

start = time.perf_counter()
__version__ = u"0.1"

# should pass via  parameters
#ENV="demo"
ENV=u"PROD"

logging.basicConfig(level=logging.DEBUG) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
  
    logging.debug (u"--Created date field copier starting --") 

 
    parser = argparse.ArgumentParser(description=" Copy Jira JQL result issues attachments to given directory",
    
    
    epilog="""
    
    EXAMPLE:
    
    TODO  GetData.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -i JIRAISSUE-ID"""

    
    )
    
   

    #parser = argparse.ArgumentParser(description="Copy Jira JQL result issues' attachments to given directory")
    
    #parser = argparse.ArgumentParser(epilog=" not displayed ") # TODO: not working
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA password>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-i', help='<JIRA IssueKey>',metavar="IssueKey")
    parser.add_argument('-r', help='<DryRun - do nothing but emulate. Off by default>',metavar="on|off",default="off")
 

    args = parser.parse_args()
       
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''
    #ISSUE=args.i or ''
    if (args.r=="on"):
        SKIP=1
    else:
        SKIP=0    

    logging.info("PSWD:{0}".format(PSWD))
    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER==''):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    print ("FORCE EXIT..!!")
    sys.exit(5)
    Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,ISSUE)



############################################################################################################################################
# Parse attachment files and add to matching Jira issue
#

#NOTE: Uses hardcoded sheet/column value

def Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,ISSUE):


    try:    
       issue = jira.issue(ISSUE)
    
       logging.debug ("Issue Data: {0}".format(issue.fields))
       
       for field_name in issue.raw['fields']:
               print ("Field:{0}  Value:{1}".format(field_name,issue.raw['fields'][field_name]))
    
    except JIRAError as e: 
            logging.error(" ********** JIRA ERROR DETECTED: ***********")
            logging.error(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
            if (e.status_code==400):
                logging.error("400 error dedected") 
    else:
        logging.info("All OK")
  
        
    end = time.perf_counter()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")
    
logging.debug ("--Python exiting--")



#############################################
# Generate timestamp 
#
def GetStamp():
    from datetime import datetime,date
    
    hours=str(datetime.today().hour)
    minutes=str(datetime.today().minute)
    seconds=str(datetime.today().second)
    milliseconds=str(datetime.today().microsecond)

    stamp=hours+"_"+minutes+"_"+seconds+"_"+milliseconds

    return stamp


if __name__ == "__main__":
    main(sys.argv[1:]) 
 