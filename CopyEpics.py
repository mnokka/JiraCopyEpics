# Copy given Jira project Epics to another Jira project (summary + description)  
# 
# mika.nokka1@gmail.com 1.9.2021



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
 
    parser = argparse.ArgumentParser(description=" Copy Jira JQL result issues attachments to given directory",
    
    
    epilog="""
    
    EXAMPLE:
    
    CopyEpics.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ """

    
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
   
   
    #print ("Creating test Epic")
    #SUMMARY="TEST SUMMARY"
    #DESCRIPTION="TEST DESCRIPTION"
    #CreateEpic(jira,SUMMARY,DESCRIPTION,TARGETPROJECT)

    GetSourceEpics(SOURCEJIRAPROJECT,jira,SKIP,TARGETPROJECT)


    end = time.perf_counter()
    totaltime=end-start
    #seconds=totaltime.total_seconds()
    print ("Operation time taken:{0} seconds".format(totaltime))

############################################################################################################################################
# Create Epic issue. Using fixed task issuetype
#
# https://zzzzz.atlassian.net/rest/api/2/field to fiend Epic name custom field ID
# in used example Jira, it was customfield_10004
# In server check Issues/Epic ID using UI
#

def CreateEpic(jira,SUMMARY,DESCRIPTION,TARGETPROJECT):

    start = time.perf_counter()

    try:    

            newissue=jira.create_issue(fields={
            'project': {'key': TARGETPROJECT},
            'issuetype': {
                "name": "Epic"
            },
            'summary': SUMMARY,
            'description': DESCRIPTION,
            'customfield_10005': SUMMARY   # only needed for Epic issuetype, "Epic Name", check your own Jira ID
            })
    
    except JIRAError as e: 
            logging.error(" ********** JIRA ERROR DETECTED: ***********")
            #logging.error("Tried create issue:{0}".format(newissue))
            
            logging.error(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
            if (e.status_code==400):
                logging.error("400 error dedected") 
    else:
        logging.info("All OK")
        logging.info("Issue created:{0}".format(newissue))
  
        
    end = time.perf_counter()
    totaltime=end-start
    print ("Operation time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")
    
logging.debug ("--Python exiting--")

#################################################
#Get source project Epics, hardcoded JQL
#

def GetSourceEpics(SOURCEJIRAPROJECT,jira,SKIP,TARGETPROJECT):

    jql_query="Project = \'{0}\' and issuetype =\'Epic\' ".format(SOURCEJIRAPROJECT) 
    print ("Used query:{0}".format(jql_query))
                        
    issue_list=jira.search_issues(jql_query, maxResults=4000)
    
       
                     
    nbr=len(issue_list)                    
    if nbr >= 1:
        COUNTER=1
        print ("Found:{0} Epics".format(nbr))
        for issue in issue_list:
            SUMMARY=issue.fields.summary
            DESCRIPTION=issue.fields.description
            print ("ISSUE:{0}-->{1}".format(COUNTER,issue))
            print("SUMMARY:{0}".format(SUMMARY))
            print("DESCRIPTION:{0}".format(DESCRIPTION))

            COUNTER=COUNTER+1
            if (SKIP==1):
                print("DRY RUN MODE ON. Not creating the Epic")
            else:
                print ("REAL OPERATION MODE. DRY RUN MODE OFF. Creating the Epic")    
                CreateEpic(jira,SUMMARY,DESCRIPTION,TARGETPROJECT)
            
            time.sleep(0.5) # prevent jira crash when creating issues in a row
            print ("---------------------------------------------------------")
            
    else:
        print ("NO Epics found")


#########################################################################

if __name__ == "__main__":
    main(sys.argv[1:]) 
 